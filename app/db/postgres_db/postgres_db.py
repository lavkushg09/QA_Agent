from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..config import settings

if settings.db_type == 'sqlite':
    DATABASE_URL = f"sqlite:///{settings.sqlite_path}"
    connect_args = {"check_same_thread": False}
elif settings.db_type == 'postgres':
    DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    connect_args = {}
else:
    raise ValueError(f"Unsupported db type: {settings.db_type}")

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


