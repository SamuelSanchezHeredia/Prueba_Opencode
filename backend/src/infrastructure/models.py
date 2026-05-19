import uuid

from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Integer, String, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class CvSession(Base):
    __tablename__ = "cv_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    target_sector = Column(String(100), nullable=False)
    overall_score = Column(Integer, default=0)
    ats_score = Column(Integer, default=0)
    keyword_score = Column(Integer, default=0)
    semantic_score = Column(Integer, default=0)
    started_at = Column(TIMESTAMP, nullable=False)
    ended_at = Column(TIMESTAMP, nullable=True)
    status = Column(String(50), nullable=False, default="processing")


class CvSectionExtracted(Base):
    __tablename__ = "cv_sections_extracted"

    section_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("cv_sessions.session_id", ondelete="CASCADE"), nullable=False)
    section_name = Column(String(100), nullable=False)
    raw_text = Column(Text, nullable=False)
    clean_json = Column(JSON, nullable=False, default={})


class AiCorrection(Base):
    __tablename__ = "ai_corrections"

    correction_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("cv_sessions.session_id", ondelete="CASCADE"), nullable=False)
    original_text = Column(Text, nullable=False)
    suggested_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)


class OperationalLog(Base):
    __tablename__ = "operational_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("cv_sessions.session_id", ondelete="CASCADE"), nullable=False)
    module_name = Column(String(100), nullable=False)
    input_payload = Column(JSON, nullable=True)
    output_payload = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)


class Faq(Base):
    __tablename__ = "faqs"

    faq_id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)


class FaqEmbedding(Base):
    __tablename__ = "faq_embeddings"

    faq_id = Column(Integer, ForeignKey("faqs.faq_id", ondelete="CASCADE"), primary_key=True)
    embedding = Column(Vector(384), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("cv_sessions.session_id", ondelete="SET NULL"), nullable=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
