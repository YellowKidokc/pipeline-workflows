from scripts.resolve_preferences import resolve

def test_resolve_defaults():
    prefs = resolve("PaperGrading")
    assert isinstance(prefs, dict)
    assert "threshold_pass" in prefs
