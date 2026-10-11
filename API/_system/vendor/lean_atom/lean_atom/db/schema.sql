-- Normalized SQLite Schema for lean-atom-extractor

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    root_path TEXT NOT NULL,
    config_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_files (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    relative_path TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    last_scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    UNIQUE(project_id, relative_path)
);

CREATE TABLE IF NOT EXISTS declarations (
    id TEXT PRIMARY KEY, -- Stable identity: project:relative_path:fq_name
    file_id TEXT NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    declaration_kind TEXT NOT NULL, -- axiom, def, theorem, lemma, etc.
    declaration_name TEXT NOT NULL,
    namespace TEXT,
    fully_qualified_name TEXT NOT NULL,
    formal_statement TEXT NOT NULL,
    proof_script TEXT,
    variables_json TEXT, -- JSON array
    types_json TEXT,     -- JSON array
    imports_json TEXT,   -- JSON array
    start_line INTEGER,
    end_line INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_id, fully_qualified_name)
);

CREATE TABLE IF NOT EXISTS dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL REFERENCES declarations(id) ON DELETE CASCADE,
    dependency_type TEXT NOT NULL, -- import, definition_used, premise, custom_axiom, upstream
    target_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS builds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL REFERENCES declarations(id) ON DELETE CASCADE,
    lean_version TEXT,
    toolchain_version TEXT,
    build_command TEXT,
    build_result TEXT NOT NULL, -- NOT_RUN, PASSED, FAILED, TIMEOUT, TOOLCHAIN_MISMATCH
    stdout TEXT,
    stderr TEXT,
    exit_code INTEGER,
    receipt_hash TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trust_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL REFERENCES declarations(id) ON DELETE CASCADE,
    trust_status TEXT NOT NULL, -- CLEAN, CONTAINS_SORRY, CONTAINS_ADMIT, CUSTOM_AXIOMS, etc.
    sorry_count INTEGER DEFAULT 0,
    admit_count INTEGER DEFAULT 0,
    custom_axioms_json TEXT,
    proof_escapes_json TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS classifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL UNIQUE REFERENCES declarations(id) ON DELETE CASCADE,
    applicability TEXT DEFAULT 'UNKNOWN',
    formalization_status TEXT DEFAULT 'NONE',
    logical_roles_json TEXT,      -- JSON array
    reasoning_regimes_json TEXT,  -- JSON array
    statement_form TEXT DEFAULT 'UNCONDITIONAL',
    formal_result TEXT DEFAULT 'NO_RESULT',
    trust_statuses_json TEXT,     -- JSON array
    correspondence_status TEXT DEFAULT 'UNASSESSED',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL REFERENCES declarations(id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    output_hash TEXT NOT NULL,
    raw_response TEXT NOT NULL,
    parsed_json TEXT,
    is_quarantined INTEGER DEFAULT 0,
    quarantine_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL REFERENCES declarations(id) ON DELETE CASCADE,
    export_path TEXT NOT NULL,
    schema_version TEXT DEFAULT '1.0',
    json_hash TEXT NOT NULL,
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    declaration_id TEXT NOT NULL REFERENCES declarations(id) ON DELETE CASCADE,
    receipt_type TEXT NOT NULL,
    receipt_body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_decl_fqn ON declarations(fully_qualified_name);
CREATE INDEX IF NOT EXISTS idx_decl_file ON declarations(file_id);
CREATE INDEX IF NOT EXISTS idx_source_hash ON source_files(source_hash);
CREATE INDEX IF NOT EXISTS idx_class_status ON classifications(formalization_status);
