from sqlalchemy.orm import Session


class BaseCRUD:
    def __init__(self):
        self.model = None
        self.does_not_exist_exception = None

    def create(self, db: Session, item_create: dict):
        new_item = self.model(**item_create)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    def get(self, db: Session, item_id: int):
        if item := db.query(self.model).filter_by(id=item_id).first():
            return item
        else:
            raise self.does_not_exist_exception

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def update(self, db: Session, item_id: int, item_update: dict):
        if item := self.get(db, item_id):
            db.query(self.model).filter_by(id=item_id).update(item_update)
            db.commit()
            db.refresh(item)
            return item

    def delete(self, db: Session, item_id: int) -> None:
        if item := self.get(db, item_id):
            db.delete(item)
            db.commit()
