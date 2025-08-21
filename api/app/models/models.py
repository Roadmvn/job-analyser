from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index
from .base import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    external_id = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    title = Column(String(512), nullable=False, index=True)
    location = Column(String(255), nullable=True, index=True)
    sector = Column(String(255), nullable=True, index=True)
    contract_type = Column(String(100), nullable=True, index=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String(10), nullable=True)
    url = Column(String(1024), nullable=False)
    posted_at = Column(DateTime, nullable=True, index=True)
    raw_description = Column(Text, nullable=False)
    hash = Column(String(64), nullable=False, unique=True)
    __table_args__ = (
        Index(
            "ix_jobs_fulltext_title_desc",
            "title",
            "raw_description",
            mysql_prefix="FULLTEXT",
        ),
    )


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class JobSkill(Base):
    __tablename__ = "job_skills"
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    plan = Column(String(20), nullable=False, default="free")


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=True)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    notes = Column(Text, nullable=False)


