CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS cv_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    target_sector VARCHAR(100) NOT NULL,
    overall_score INTEGER DEFAULT 0,
    ats_score INTEGER DEFAULT 0,
    keyword_score INTEGER DEFAULT 0,
    semantic_score INTEGER DEFAULT 0,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'processing'
);

CREATE TABLE IF NOT EXISTS cv_sections_extracted (
    section_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    section_name VARCHAR(100) NOT NULL,
    raw_text TEXT NOT NULL,
    clean_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    FOREIGN KEY (session_id) REFERENCES cv_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ai_corrections (
    correction_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    original_text TEXT NOT NULL,
    suggested_text TEXT NOT NULL,
    explanation TEXT,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES cv_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS operational_logs (
    log_id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    module_name VARCHAR(100) NOT NULL,
    input_payload JSONB,
    output_payload JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (session_id) REFERENCES cv_sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS faqs (
    faq_id BIGSERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cv_sessions_status ON cv_sessions(status);
CREATE INDEX IF NOT EXISTS idx_sections_session_id ON cv_sections_extracted(session_id);
CREATE INDEX IF NOT EXISTS idx_corrections_session_id ON ai_corrections(session_id);
CREATE INDEX IF NOT EXISTS idx_logs_module ON operational_logs(module_name);
CREATE INDEX IF NOT EXISTS idx_faqs_question ON faqs(question);
CREATE UNIQUE INDEX IF NOT EXISTS uq_faqs_question ON faqs(question);
