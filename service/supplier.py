from repository.supplier import Supplier, SupplierRepository
from models.models import Supplier

class SupplierService:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def create_supplier(self, name: str, contact_info: str, address: str):
        new_supplier = Supplier(name=name, contact_info=contact_info, address=address)
        self.repository.add_supplier(new_supplier)
        return new_supplier

    def fetch_supplier(self, supplier_id: int):
        return self.repository.fetch_supplier_by_id(supplier_id)

    def fetch_all_suppliers(self):
        return self.repository.fetch_all_suppliers()

    def update_supplier(self, supplier_id: int, name: str, contact_info: str, address: str):
        supplier = self.repository.fetch_supplier_by_id(supplier_id)
        if supplier:
            supplier.name = name
            supplier.contact_info = contact_info
            supplier.address = address
            self.repository.update_supplier(supplier)
            return supplier
        return None

    def delete_supplier(self, supplier_id: int):
        supplier = self.repository.fetch_supplier_by_id(supplier_id)
        if supplier:
            self.repository.delete_supplier(supplier)
            return True
        return False
