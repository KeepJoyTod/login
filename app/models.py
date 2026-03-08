from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    projects = relationship("ProjectMember", back_populates="user")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    members = relationship("ProjectMember", back_populates="project")
    interfaces = relationship("Interface", back_populates="project")
    environments = relationship("Environment", back_populates="project")
    jobs = relationship("Job", back_populates="project")

class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = Column(String, ForeignKey("projects.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    role = Column(String, default="viewer") # owner, admin, qa, dev, viewer

    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="projects")

class Interface(Base):
    __tablename__ = "interfaces"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    module_id = Column(String, nullable=True)
    method = Column(String)
    path = Column(String)
    title = Column(String)
    description = Column(Text, nullable=True)
    schema = Column(JSON, nullable=True) # InterfaceSchema
    tags = Column(JSON, nullable=True) # List[str]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="interfaces")
    testcases = relationship("TestCase", back_populates="interface")

class Environment(Base):
    __tablename__ = "environments"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String)
    base_url = Column(String)
    headers = Column(JSON, nullable=True)
    auth = Column(JSON, nullable=True)
    variables = Column(JSON, nullable=True)
    secret_variables = Column(JSON, nullable=True) # Encrypted in real app

    project = relationship("Project", back_populates="projects")

class TestCase(Base):
    __tablename__ = "testcases"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    interface_id = Column(String, ForeignKey("interfaces.id"))
    module_id = Column(String, nullable=True)
    name = Column(String)
    type = Column(String) # positive, negative, boundary
    priority = Column(String, default="medium")
    definition = Column(JSON, nullable=True) # TestCaseDefinition
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project")
    interface = relationship("Interface", back_populates="testcases")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    type = Column(String) # generate, run
    status = Column(String) # pending, running, success, fail, cancelled
    progress = Column(Integer, default=0)
    steps = Column(JSON, default=[]) # List[JobStep]
    result = Column(JSON, nullable=True) # JobResult
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="jobs")
    logs = relationship("RuntimeLog", back_populates="job")

class RuntimeLog(Base):
    __tablename__ = "runtime_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), index=True)
    seq = Column(Integer)
    level = Column(String)
    message = Column(Text)
    ts = Column(DateTime(timezone=True))

    job = relationship("Job", back_populates="logs")
