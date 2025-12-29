from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
# Avoid DetachedInstanceError after commit when returning ORM objects to API
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
# Create tables on startup if not present. Import Base here to avoid circular imports.
try:
	from models.tables import Base

	Base.metadata.create_all(engine)
except Exception:
	# Avoid crashing at import time if DB is unreachable; the app/worker should handle connection errors.
	pass
