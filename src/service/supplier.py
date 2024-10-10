from typing import Optional, Type

from models.models import Supplier
from repository.supplier import SupplierRepository


class SupplierService:
    """
    Service for managing supplier operations, including creating, updating,
    deleting, and retrieving supplier records.
    """

    def __init__(self, repository: SupplierRepository):
        """
        Initializes the SupplierService with the given repository.

        :param repository: Repository for managing supplier records.
        """
        self.repository = repository

    def create_supplier(self, name: str, contact_info: str, address: str) -> Supplier:
        """
        Creates a new supplier.

        :param name: Name of the supplier.
        :param contact_info: Contact information of the supplier.
        :param address: Address of the supplier.
        :return: The created Supplier object.
        """
        new_supplier = Supplier(name=name, contact_info=contact_info, address=address)
        self.repository.add_supplier(new_supplier)
        return new_supplier

    def fetch_supplier(self, supplier_id: int) -> Optional[Supplier]:
        """
        Retrieves a supplier by its ID.

        :param supplier_id: ID of the supplier to be retrieved.
        :return: Supplier object if found, or None if not found.
        """
        return self.repository.fetch_supplier_by_id(supplier_id)

    def fetch_all_suppliers(self) -> list[Type[Supplier]]:
        """
        Retrieves all supplier records.

        :return: List of all Supplier objects.
        """
        return self.repository.fetch_all_suppliers()

    def update_supplier(self, supplier_id: int, name: str, contact_info: str, address: str) -> Optional[Supplier]:
        """
        Updates an existing supplier.

        :param supplier_id: ID of the supplier to be updated.
        :param name: Updated name of the supplier.
        :param contact_info: Updated contact information of the supplier.
        :param address: Updated address of the supplier.
        :return: Updated Supplier object if successful, or None if the supplier is not found.
        """
        supplier = self.repository.fetch_supplier_by_id(supplier_id)
        if supplier:
            supplier.name = name
            supplier.contact_info = contact_info
            supplier.address = address
            self.repository.update_supplier(supplier)
            return supplier
        return None

    def delete_supplier(self, supplier_id: int) -> bool:
        """
        Deletes a supplier by its ID.

        :param supplier_id: ID of the supplier to be deleted.
        :return: True if the supplier was successfully deleted, or False if the supplier was not found.
        """
        supplier = self.repository.fetch_supplier_by_id(supplier_id)
        if supplier:
            self.repository.delete_supplier(supplier)
            return True
        return False
