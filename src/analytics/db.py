from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(String(50))
    bio = Column(Text)

    works = relationship("Work", back_populates="author")


class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    first_publish_year = Column(Integer)
    subject_count = Column(Integer, default=0)

    author = relationship("Author", back_populates="works")
    subjects = relationship("Subject", back_populates="work")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False)
    subject_name = Column(String(255), nullable=False)

    work = relationship("Work", back_populates="subjects")


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Tables created successfully.")