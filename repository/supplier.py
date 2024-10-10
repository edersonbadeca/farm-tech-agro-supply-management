from sqlalchemy.orm import Session
from typing import List, Optional, Type
from models.models import Supplier, Input, StockMovement

class SupplierRepository:
    """
    Repository for managing supplier operations in the database.
    """

    def __init__(self, session: Session):
        """
        Initializes the repository with a database session.

        :param session: SQLAlchemy session for interacting with the database.
        """
        self.session = session

    def add_supplier(self, supplier: Supplier) -> None:
        """
        Adds a new supplier to the database.

        :param supplier: Supplier object to be added.
        """
        self.session.add(supplier)
        self.session.commit()

    def fetch_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        """
        Retrieves a supplier by its ID.

        :param supplier_id: ID of the supplier to be retrieved.
        :return: Supplier object corresponding to the provided ID, or None if not found.
        """
        return (
            self.session
                .query(Supplier)
                .filter(Supplier.id == supplier_id)
                .first()
        )

    def fetch_all_suppliers(self) -> list[Type[Supplier]]:
        """
        Retrieves all suppliers from the database.

        :return: List of Supplier objects.
        """
        return (
            self.session
                .query(Supplier)
                .all()
        )

    def update_supplier(self, supplier: Supplier) -> None:
        """
        Updates the information of an existing supplier.

        :param supplier: Supplier object with the updated data.
        """
        self.session.merge(supplier)
        self.session.commit()

    def delete_supplier(self, supplier: Supplier) -> None:
        """
        Removes a supplier from the database.

        :param supplier: Supplier object to be removed.
        """
        self.session.delete(supplier)
        self.session.commit()
