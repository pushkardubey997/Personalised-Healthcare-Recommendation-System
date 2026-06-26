from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    precautions = relationship("Precaution", back_populates="disease", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="disease", cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="disease", cascade="all, delete-orphan")
    diets = relationship("Diet", back_populates="disease", cascade="all, delete-orphan")


class Precaution(Base):
    __tablename__ = "precautions"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    text = Column(String, nullable=False)

    disease = relationship("Disease", back_populates="precautions")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    name = Column(String, nullable=False)

    disease = relationship("Disease", back_populates="medications")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    activity = Column(String, nullable=False)

    disease = relationship("Disease", back_populates="workouts")


class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    item = Column(String, nullable=False)

    disease = relationship("Disease", back_populates="diets")
