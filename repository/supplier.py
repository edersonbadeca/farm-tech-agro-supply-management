from sqlalchemy.orm import Session
from models.models import Supplier, Input, StockMovement

class Repository:
    def __init__(self, session: Session):
        self.session = session

    def add_supplier(self, supplier: Supplier):
        self.session.add(supplier)
        self.session.commit()

    def fetch_supplier_by_id(self, supplier_id: int):
        return (self
                .session
                .query(Supplier)
                .filter(Supplier.id == supplier_id)
                .first()
        )

    def fetch_all_suppliers(self):
        return (self
                .session
                .query(Supplier)
                .all()
        )

    def update_supplier(self, supplier: Supplier):
        self.session.merge(supplier)
        self.session.commit()

    def delete_supplier(self, supplier: Supplier):
        self.session.delete(supplier)
        self.session.commit()

