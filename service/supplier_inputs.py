from repository.inputs import InputRepository
from models.models import Input


class InputService:
    def __init__(self, repository: InputRepository):
        self.repository = repository

    def create_input(self, name: str, category: str, quantity: int, expiration_date, supplier_id: int):
        if not self.supplier_exists(supplier_id):
            return None
        new_input = Input(
            name=name,
            category=category,
            quantity=quantity,
            expiration_date=expiration_date,
            supplier_id=supplier_id
        )
        self.repository.add_input(new_input)
        return new_input

    def get_input(self, input_id: int):
        return self.repository.get_input_by_id(input_id)

    def update_input(self, input_id: int, name: str, category: str, quantity: int, expiration_date, supplier_id: int):
        input_item = self.repository.get_input_by_id(input_id)
        if input_item:
            input_item.name = name
            input_item.category = category
            input_item.quantity = quantity
            input_item.expiration_date = expiration_date
            input_item.supplier_id = supplier_id
            self.repository.update_input(input_item)
            return input_item
        return None

    def delete_input(self, input_id: int):
        input_item = self.repository.get_input_by_id(input_id)
        if input_item:
            self.repository.delete_input(input_item)
            return True
        return False

    def get_all_inputs(self):
        return self.repository.get_all_inputs()

    def supplier_exists(self, supplier_id: int):
        supplier = self.repository.get_input_by_id(supplier_id)
        return supplier is not None

