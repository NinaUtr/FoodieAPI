from typing import Generator
from app.db.session import session


def get_db() -> Generator:
    db = session()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
