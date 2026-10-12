"""Tests for the ME pipeline Stage 2: span judgment validation and the canon
ledger's five-condition logic. No API calls."""

import importlib.util
import pathlib
import sys
import unittest

SCRIPTS = pathlib.Path(__file__).parents[1]


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


sj = load_module("span_judge")
cl = load_module("canon_ledger_pass")


def good_judgment():
    return {
        "role": "SLOT_CLAIM",
        "slot_signals": [{"slot_id": "slot.g", "polarity": 1,
                          "fit": "direct", "quote": "grace sustains coherence"}],
        "gate_flags": [], "kill_condition": "",
        "confidence": 0.8, "uncertainty_note": "",
    }


class SpanJudgmentTests(unittest.TestCase):
    def test_valid_judgment_passes(self):
        j = sj.validate_judgment(good_judgment())
        self.assertEqual(j["slot_signals"][0]["polarity"], 1)

    def test_bad_slot_id_rejected(self):
        j = good_judgment()
        j["slot_signals"][0]["slot_id"] = "slot.grace"
        with self.assertRaises(ValueError):
            sj.validate_judgment(j)

    def test_bad_fit_rejected(self):
        j = good_judgment()
        j["slot_signals"][0]["fit"] = "canonical"
        with self.assertRaises(ValueError):
            sj.validate_judgment(j)

    def test_bad_gate_flag_rejected(self):
        j = good_judgment()
        j["gate_flags"] = ["heresy"]
        with self.assertRaises(ValueError):
            sj.validate_judgment(j)

    def test_unverifiable_quote_dropped(self):
        span_sents = [{"idx": 0, "text": "Grace sustains coherence in open systems."}]
        sent_by_idx = {0: span_sents[0]}
        j = good_judgment()
        j["slot_signals"][0]["quote"] = "the moon is made of green cheese"
        verified, dropped, counts = sj.verify_signals(j, span_sents, sent_by_idx)
        self.assertEqual(verified, [])
        self.assertEqual(len(dropped), 1)
        self.assertEqual(counts["dropped"], 1)

    def test_exact_quote_verified(self):
        span_sents = [{"idx": 0, "text": "Grace sustains coherence in open systems."}]
        j = good_judgment()
        j["slot_signals"][0]["quote"] = "Grace sustains coherence"
        verified, dropped, counts = sj.verify_signals(j, span_sents, {})
        self.assertEqual(len(verified), 1)
        self.assertEqual(verified[0]["quote_status"], "exact")
        self.assertEqual(dropped, [])

    def test_corrected_quote_found_elsewhere(self):
        span_sents = [{"idx": 5, "text": "Nothing relevant here."}]
        sent_by_idx = {0: {"idx": 0, "text": "Grace sustains coherence."},
                       5: span_sents[0]}
        j = good_judgment()
        j["slot_signals"][0]["quote"] = "grace sustains coherence"
        verified, dropped, counts = sj.verify_signals(j, span_sents, sent_by_idx)
        self.assertEqual(counts["corrected"], 1)
        self.assertEqual(verified[0]["corrected_sent_range"], [0, 0])


def make_atom(**over):
    atom = {
        "id": "M001",
        "statement": "grace is the external negentropy influx that sustains coherence",
        "claim_type": "slot_claim",
        "slot_refs": ["slot.g"],
        "source_spans": [0],
        "source_sentences": [0],
        "kill_condition": "",
        "proposed_grade": "CANDIDATE",
    }
    atom.update(over)
    return atom


def receipts_matching(text):
    return [{"kind": "test", "path": "fixture.md", "sha256": "x",
             "tokens": sorted(cl.content_tokens(text))}]


SLOT_NAMES = {"slot.g": "External Negentropy Influx"}


class CanonConditionTests(unittest.TestCase):
    def all_pass_conditions(self, atom, **kw):
        receipts = kw.get("receipts",
                          receipts_matching("external negentropy influx grace sustains coherence"))
        return {
            "address": {"pass": True, "detail": "assigned M001"},
            "grade": cl.check_grade(atom.get("proposed_grade")),
            "receipt": cl.check_receipt(atom, receipts, SLOT_NAMES),
            "authority": kw.get("authority",
                                cl.check_authority(["This is canonical."], "", 1, 0)),
            "no_conflict": kw.get("no_conflict",
                                  cl.check_no_conflict(atom, {"slot.g": 1},
                                                       {"M001": {"slot.g": 1}}, [], [""])),
        }

    def test_no_receipt_is_hold(self):
        atom = make_atom()
        cond = self.all_pass_conditions(atom, receipts=[])
        self.assertEqual(cond["receipt"]["status"], "NOT_ATTEMPTED")
        self.assertEqual(cl.verdict(cond), "HOLD")

    def test_all_conditions_met_is_canon_ready(self):
        atom = make_atom()
        cond = self.all_pass_conditions(atom)
        for key, c in cond.items():
            self.assertTrue(c["pass"], f"{key} should pass: {c}")
        self.assertEqual(cond["receipt"]["status"], "LEAN_PROVEN")
        self.assertEqual(cl.verdict(cond), "CANON-READY")

    def test_authority_missing_is_needs_ruling(self):
        atom = make_atom()
        authority = cl.check_authority(["Some plain sentence about grace."], "", 0, 0)
        self.assertFalse(authority["pass"])
        self.assertEqual(authority["flag"], "authority_missing")
        cond = self.all_pass_conditions(atom, authority=authority)
        self.assertEqual(cl.verdict(cond), "NEEDS-RULING")

    def test_header_ruling_citation_satisfies_authority(self):
        header = "Canonical ruling: July 26, 2026 · Eponym dictionary ratified"
        authority = cl.check_authority(["Some plain sentence."], header, 0, 0)
        self.assertTrue(authority["pass"])
        self.assertEqual(authority["via"], "paper_header")

    def test_conflict_is_needs_ruling(self):
        atom = make_atom()
        conflict = cl.check_no_conflict(atom, {"slot.g": 1},
                                        {"M001": {"slot.g": 1},
                                         "M002": {"slot.g": -1}}, [], [""])
        self.assertFalse(conflict["pass"])
        self.assertEqual(conflict["flag"], "conflict_suspect")
        cond = self.all_pass_conditions(atom, no_conflict=conflict)
        self.assertEqual(cl.verdict(cond), "NEEDS-RULING")

    def test_protected_marker_collision_is_conflict(self):
        atom = make_atom(proposed_grade="LOCKED")
        conflict = cl.check_no_conflict(atom, {}, {"M001": {}},
                                        ["raw-fragment"],
                                        ["this is a raw-fragment excerpt"])
        self.assertFalse(conflict["pass"])

    def test_grade_outside_vocabulary_is_hold(self):
        atom = make_atom(proposed_grade="CANONIZED")
        grade = cl.check_grade(atom["proposed_grade"])
        self.assertFalse(grade["pass"])
        self.assertEqual(grade["flag"], "ungraded_vocabulary")
        cond = self.all_pass_conditions(atom)
        cond["grade"] = grade
        self.assertEqual(cl.verdict(cond), "HOLD")

    def test_grade_none_is_hold(self):
        atom = make_atom(proposed_grade=None)
        grade = cl.check_grade(None)
        self.assertFalse(grade["pass"])
        cond = self.all_pass_conditions(atom)
        cond["grade"] = grade
        self.assertEqual(cl.verdict(cond), "HOLD")

    def test_needs_ruling_precedence_over_hold(self):
        atom = make_atom(proposed_grade="CANONIZED")
        authority = cl.check_authority(["Plain text."], "", 0, 0)
        cond = self.all_pass_conditions(atom, receipts=[], authority=authority)
        cond["grade"] = cl.check_grade("CANONIZED")
        self.assertEqual(cl.verdict(cond), "NEEDS-RULING")


if __name__ == "__main__":
    unittest.main()
