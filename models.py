from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Инициализация базы данных
DATABASE_URL = "sqlite:///bot_data.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Модель для хранения данных пользователя
class UserData(Base):
    __tablename__ = "user_data"

    user_id = Column(Integer, primary_key=True, index=True)
    transcription = Column(Text, nullable=True)


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)
