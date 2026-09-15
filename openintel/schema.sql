PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS id_sequences (kind TEXT NOT NULL, collection TEXT NOT NULL, next_value INTEGER NOT NULL DEFAULT 1, PRIMARY KEY(kind, collection));
CREATE TABLE IF NOT EXISTS case_types (code TEXT PRIMARY KEY, label TEXT NOT NULL, description TEXT, example_case TEXT, template_modules TEXT);
CREATE TABLE IF NOT EXISTS evidence_types (type_id INTEGER PRIMARY KEY, tier TEXT NOT NULL CHECK(tier IN ('T1','T2','T3','T4','T5','NEGATIVE')), tier_label TEXT NOT NULL, name TEXT NOT NULL, description TEXT, weight REAL DEFAULT .5 CHECK(weight BETWEEN 0 AND 1));

CREATE TABLE IF NOT EXISTS cases (
 id TEXT PRIMARY KEY CHECK(id GLOB 'CASE-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', short_code TEXT, case_type TEXT REFERENCES case_types(code), title TEXT NOT NULL, slug TEXT,
 verdict TEXT, rating TEXT NOT NULL DEFAULT 'UNRATED' CHECK(rating IN ('T1','T1-T2','T2','T2-T3','T3','T3-T4','T4','T4-T5','T5','Mixed','UNRATED')),
 ocs_score REAL, status TEXT NOT NULL DEFAULT 'CANDIDATE' CHECK(status IN ('CANDIDATE','REVIEW','ACCEPTED','REJECTED')), rejection_reason TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 CHECK(status != 'REJECTED' OR rejection_reason IS NOT NULL)
);
CREATE TABLE IF NOT EXISTS hunches (
 id TEXT PRIMARY KEY CHECK(id GLOB 'HNCH-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), written_by TEXT NOT NULL, written_at TEXT NOT NULL,
 gut_statement TEXT NOT NULL, what_triggered_it TEXT, what_would_make_it_real TEXT, what_would_kill_it TEXT,
 hunch_status TEXT NOT NULL DEFAULT 'OPEN' CHECK(hunch_status IN ('OPEN','PROMOTED','PARKED','DROPPED')), promoted_to TEXT NOT NULL DEFAULT '[]', drop_reason TEXT,
 lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE' CHECK(lifecycle IN ('CANDIDATE','REVIEW','ACCEPTED','REJECTED')), rejection_reason TEXT,
 sensitive INTEGER NOT NULL DEFAULT 0 CHECK(sensitive IN (0,1)), public_projection INTEGER NOT NULL DEFAULT 0 CHECK(public_projection IN (0,1)),
 CHECK(hunch_status != 'DROPPED' OR drop_reason IS NOT NULL), CHECK(lifecycle != 'REJECTED' OR rejection_reason IS NOT NULL), CHECK(sensitive = 0 OR public_projection = 0)
);
CREATE TABLE IF NOT EXISTS sources (
 id TEXT PRIMARY KEY CHECK(id GLOB 'SRC-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), title TEXT, source_type TEXT, url TEXT, publisher TEXT,
 published_at TEXT, acquired_at TEXT, content_hash TEXT, parent_source_id TEXT REFERENCES sources(id), lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE' CHECK(lifecycle IN ('CANDIDATE','REVIEW','ACCEPTED','REJECTED')), rejection_reason TEXT,
 CHECK(lifecycle != 'REJECTED' OR rejection_reason IS NOT NULL)
);
CREATE TABLE IF NOT EXISTS statements (
 id TEXT PRIMARY KEY CHECK(id GLOB 'STMT-*-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), source_id TEXT NOT NULL REFERENCES sources(id), speaker_entity_id TEXT,
 statement_text TEXT NOT NULL, statement_hash TEXT NOT NULL UNIQUE, made_at TEXT, context TEXT, locator TEXT, attribution_confidence TEXT CHECK(attribution_confidence IN ('HIGH','MED','LOW') OR attribution_confidence IS NULL),
 lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE' CHECK(lifecycle IN ('CANDIDATE','REVIEW','ACCEPTED','REJECTED')), rejection_reason TEXT, sensitive INTEGER NOT NULL DEFAULT 0 CHECK(sensitive IN (0,1)), public_projection INTEGER NOT NULL DEFAULT 0 CHECK(public_projection IN (0,1)),
 CHECK(lifecycle != 'REJECTED' OR rejection_reason IS NOT NULL), CHECK(sensitive = 0 OR public_projection = 0)
);
CREATE TABLE IF NOT EXISTS claims (
 id TEXT PRIMARY KEY CHECK(id GLOB 'CLM-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), statement_id TEXT REFERENCES statements(id), claim_text TEXT NOT NULL, claim_type TEXT, claimed_evidence TEXT, counterclaim TEXT,
 rating TEXT NOT NULL DEFAULT 'UNRATED' CHECK(rating IN ('T1','T1-T2','T2','T2-T3','T3','T3-T4','T4','T4-T5','T5','Mixed','UNRATED')),
 lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE' CHECK(lifecycle IN ('CANDIDATE','REVIEW','ACCEPTED','REJECTED')), rejection_reason TEXT, sensitive INTEGER NOT NULL DEFAULT 0, public_projection INTEGER NOT NULL DEFAULT 0,
 CHECK(lifecycle != 'REJECTED' OR rejection_reason IS NOT NULL), CHECK(sensitive = 0 OR public_projection = 0)
);
CREATE TABLE IF NOT EXISTS entities (id TEXT PRIMARY KEY CHECK(id GLOB 'ENT-*-?????'), entity_type TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', name TEXT NOT NULL, role TEXT, description TEXT, lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE', rejection_reason TEXT);
CREATE TABLE IF NOT EXISTS evidence (id TEXT PRIMARY KEY CHECK(id GLOB 'EVID-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), evidence_type INTEGER REFERENCES evidence_types(type_id), tier TEXT NOT NULL DEFAULT 'UNRATED', title TEXT, description TEXT, source_id TEXT REFERENCES sources(id), independence_score REAL DEFAULT .5, provenance_score REAL DEFAULT .5, is_negative INTEGER DEFAULT 0, lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE', rejection_reason TEXT);
CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY CHECK(id GLOB 'EVT-*-????'), collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), event_date TEXT, event_date_precision TEXT, sort_date TEXT, title TEXT NOT NULL, description TEXT, evidence_id TEXT REFERENCES evidence(id), disputed INTEGER DEFAULT 0, lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE', rejection_reason TEXT);
CREATE TABLE IF NOT EXISTS signals (id TEXT PRIMARY KEY, collection TEXT NOT NULL, legacy_ids TEXT NOT NULL DEFAULT '[]', case_id TEXT REFERENCES cases(id), signal_kind TEXT NOT NULL CHECK(signal_kind IN ('ANOM','SIG','CONTRA','FIN')), description TEXT NOT NULL, score REAL, confidence REAL, source_record_id TEXT, lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE', rejection_reason TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY AUTOINCREMENT, from_id TEXT NOT NULL, to_id TEXT NOT NULL, link_type TEXT NOT NULL, strength REAL DEFAULT .5, source TEXT, created_at TEXT NOT NULL, UNIQUE(from_id,to_id,link_type));
CREATE TABLE IF NOT EXISTS claim_evidence (claim_id TEXT REFERENCES claims(id), evidence_id TEXT REFERENCES evidence(id), relationship TEXT NOT NULL CHECK(relationship IN ('SUPPORTS','REFUTES','NEUTRAL','AMBIGUOUS')), PRIMARY KEY(claim_id,evidence_id));
CREATE TABLE IF NOT EXISTS contradictions (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', claim_a_id TEXT REFERENCES claims(id), claim_b_id TEXT REFERENCES claims(id), contradiction_type TEXT, description TEXT, resolution TEXT, severity TEXT, lifecycle TEXT DEFAULT 'CANDIDATE', rejection_reason TEXT);
CREATE TABLE IF NOT EXISTS claim_contradictions (id TEXT PRIMARY KEY, statement_a_id TEXT REFERENCES statements(id), statement_b_id TEXT REFERENCES statements(id), contradiction_type TEXT, severity_score REAL, auto_detected INTEGER DEFAULT 0, human_verified INTEGER DEFAULT 0, lifecycle TEXT DEFAULT 'CANDIDATE', rejection_reason TEXT);
CREATE TABLE IF NOT EXISTS case_entities (case_id TEXT REFERENCES cases(id), entity_id TEXT REFERENCES entities(id), relationship TEXT, strength REAL DEFAULT .5, PRIMARY KEY(case_id,entity_id));
CREATE TABLE IF NOT EXISTS entity_relationships (entity_a TEXT REFERENCES entities(id), entity_b TEXT REFERENCES entities(id), relationship_type TEXT NOT NULL, start_date TEXT, end_date TEXT, evidence_tier TEXT, source TEXT, PRIMARY KEY(entity_a,entity_b,relationship_type));
CREATE TABLE IF NOT EXISTS cross_links (case_a_id TEXT REFERENCES cases(id), case_b_id TEXT REFERENCES cases(id), link_type TEXT NOT NULL, strength REAL DEFAULT .5, PRIMARY KEY(case_a_id,case_b_id,link_type));
CREATE TABLE IF NOT EXISTS media_items (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', media_type TEXT, title TEXT, description TEXT, file_url TEXT, source_url TEXT, is_primary INTEGER DEFAULT 0, sort_order INTEGER, lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, category TEXT);
CREATE TABLE IF NOT EXISTS case_tags (case_id TEXT REFERENCES cases(id), tag_id INTEGER REFERENCES tags(id), PRIMARY KEY(case_id,tag_id));
CREATE TABLE IF NOT EXISTS testimony_records (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', source_designation TEXT NOT NULL, source_type TEXT, collection_method TEXT, collection_setting TEXT, event_date_claimed TEXT, statement_date TEXT, statement_hash TEXT UNIQUE, statement_text TEXT, credibility_tier TEXT DEFAULT 'UNASSESSED', collected_at TEXT, collected_by TEXT, lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS witness_testimony (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), entity_id TEXT REFERENCES entities(id), legacy_ids TEXT NOT NULL DEFAULT '[]', witness_name TEXT NOT NULL, role_capacity TEXT, testimony_date TEXT, testimony_context TEXT, key_claim TEXT, corroboration_status TEXT, credibility_score REAL DEFAULT .5, evidence_id TEXT REFERENCES evidence(id), is_hostile INTEGER DEFAULT 0, notes TEXT, lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS testimony_credibility_assessment (id TEXT PRIMARY KEY, testimony_id TEXT REFERENCES testimony_records(id), assessed_at TEXT NOT NULL, assessed_by TEXT NOT NULL, internal_consistency REAL, external_corroboration REAL, contextual_plausibility REAL, source_competence REAL, source_character_bias REAL, prior_statement_id TEXT REFERENCES testimony_records(id), drift_detected INTEGER DEFAULT 0, drift_type TEXT, reliability_score REAL, confidence_in_assessment REAL, critical_failure_mode TEXT);
CREATE TABLE IF NOT EXISTS wikipedia_cards (id TEXT PRIMARY KEY, case_id TEXT UNIQUE REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', wikipedia_url TEXT, wiki_summary TEXT, key_omissions TEXT, sources_cited TEXT, sources_ignored TEXT, last_edit_date TEXT, edit_war_flag INTEGER DEFAULT 0, protection_level TEXT, snapshot_date TEXT);
CREATE TABLE IF NOT EXISTS prophecy_fulfillment (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', prophecy_source TEXT NOT NULL, tradition TEXT, fulfillment_status TEXT, evidence_tier TEXT, lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS propaganda_indicators (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', indicator_type TEXT, scale TEXT, confidence TEXT, financial_amount REAL, actor TEXT, target TEXT, lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS suppression_log (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', platform TEXT, action_type TEXT, content_description TEXT, official_reason TEXT, evidence_url TEXT, lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS statistical_anomalies (id TEXT PRIMARY KEY, case_id TEXT REFERENCES cases(id), legacy_ids TEXT NOT NULL DEFAULT '[]', anomaly_type TEXT, observed_count INTEGER, expected_count REAL, sigma_deviation REAL, p_value REAL, rating TEXT DEFAULT 'UNRATED', lifecycle TEXT DEFAULT 'CANDIDATE');
CREATE TABLE IF NOT EXISTS ocs_audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT REFERENCES cases(id), old_score REAL, new_score REAL, old_rating TEXT, new_rating TEXT, reason TEXT, changed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS hunch_matches (hunch_id TEXT REFERENCES hunches(id), record_id TEXT NOT NULL, method TEXT NOT NULL, score REAL NOT NULL, checked_at TEXT NOT NULL, signal_id TEXT REFERENCES signals(id), PRIMARY KEY(hunch_id,record_id,method));
CREATE TABLE IF NOT EXISTS videos (id TEXT PRIMARY KEY, source_id TEXT UNIQUE REFERENCES sources(id), collection TEXT NOT NULL, channel TEXT NOT NULL, chapter INTEGER NOT NULL, title TEXT NOT NULL, url TEXT, published_at TEXT, duration TEXT, profile TEXT NOT NULL, raw_transcript TEXT, cleaned_transcript TEXT, status TEXT NOT NULL DEFAULT 'CANDIDATE', UNIQUE(channel,chapter));
CREATE TABLE IF NOT EXISTS transcript_chunks (id TEXT PRIMARY KEY, video_id TEXT REFERENCES videos(id), ordinal INTEGER NOT NULL, text TEXT NOT NULL, start_locator TEXT NOT NULL, end_locator TEXT NOT NULL, UNIQUE(video_id,ordinal));
CREATE TABLE IF NOT EXISTS entity_mentions (id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT REFERENCES videos(id), chunk_id TEXT REFERENCES transcript_chunks(id), statement_id TEXT REFERENCES statements(id), mention_text TEXT NOT NULL, entity_type TEXT NOT NULL, entity_id TEXT REFERENCES entities(id), confidence REAL, lifecycle TEXT NOT NULL DEFAULT 'CANDIDATE', UNIQUE(video_id,chunk_id,mention_text,entity_type));
CREATE TABLE IF NOT EXISTS entity_aliases (alias TEXT COLLATE NOCASE PRIMARY KEY, entity_id TEXT NOT NULL REFERENCES entities(id), confidence REAL NOT NULL DEFAULT 1.0, reviewed INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS theme_mentions (video_id TEXT REFERENCES videos(id), chunk_id TEXT REFERENCES transcript_chunks(id), theme TEXT NOT NULL, confidence REAL NOT NULL, PRIMARY KEY(video_id,chunk_id,theme));
CREATE TABLE IF NOT EXISTS scripture_refs (video_id TEXT REFERENCES videos(id), statement_id TEXT REFERENCES statements(id), reference TEXT NOT NULL, usage TEXT NOT NULL DEFAULT 'unclassified', PRIMARY KEY(video_id,reference,statement_id));
CREATE TABLE IF NOT EXISTS scholars_cited (video_id TEXT REFERENCES videos(id), name TEXT NOT NULL, work TEXT NOT NULL DEFAULT '', statement_id TEXT REFERENCES statements(id), PRIMARY KEY(video_id,name,work));
CREATE TABLE IF NOT EXISTS station_runs (video_id TEXT REFERENCES videos(id), station TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('RUNNING','DONE','FAILED')), started_at TEXT NOT NULL, finished_at TEXT, detail TEXT, PRIMARY KEY(video_id,station));
CREATE INDEX IF NOT EXISTS idx_hunch_status ON hunches(hunch_status, lifecycle);
CREATE INDEX IF NOT EXISTS idx_statements_case ON statements(case_id);
CREATE INDEX IF NOT EXISTS idx_claims_case ON claims(case_id);
CREATE INDEX IF NOT EXISTS idx_evidence_case ON evidence(case_id);
CREATE INDEX IF NOT EXISTS idx_links_to ON links(to_id);

CREATE TRIGGER IF NOT EXISTS hunch_written_at_immutable BEFORE UPDATE OF written_at ON hunches
WHEN NEW.written_at != OLD.written_at BEGIN SELECT RAISE(ABORT, 'hunch written_at is immutable'); END;
CREATE TRIGGER IF NOT EXISTS hunch_no_delete BEFORE DELETE ON hunches
BEGIN SELECT RAISE(ABORT, 'hunches are retained; use DROPPED or REJECTED'); END;

CREATE VIEW IF NOT EXISTS public_hunches AS SELECT * FROM hunches WHERE sensitive=0 AND public_projection=1 AND lifecycle='ACCEPTED';
CREATE VIEW IF NOT EXISTS public_statements AS SELECT * FROM statements WHERE sensitive=0 AND public_projection=1 AND lifecycle='ACCEPTED';
CREATE VIEW IF NOT EXISTS case_tier_distribution AS SELECT case_id, rating, count(*) claim_count FROM claims WHERE lifecycle='ACCEPTED' GROUP BY case_id,rating;
