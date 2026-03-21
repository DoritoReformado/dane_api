from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    

class InformationTopic(Base):
    __tablename__ = "information_topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    subtopics = relationship("InformationSubtopic", back_populates="topic")
    
class InformationSubtopic(Base):
    __tablename__ = "information_subtopics"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("information_topics.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)

    topic = relationship("InformationTopic", back_populates="subtopics")
    datasets = relationship("Dataset", back_populates="subtopic")
    
class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    subtopic_id = Column(Integer, ForeignKey("information_subtopics.id"), nullable=False)

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Ejemplo: metadata sobre el dataset (años, variables, etc.)
    metadata = Column(JSON, nullable=True)

    # Ejemplo: si lo que tienes es un link a una tabla externa/archivo
    source_type = Column(String, nullable=False, default="table")
    source_ref = Column(String, nullable=False)

    subtopic = relationship("InformationSubtopic", back_populates="datasets")