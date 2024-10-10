from repository.inputs import InputRepository
from models.models import Input
from service.supplier import SupplierService
from typing import Optional, List


class InputService:
    """
    Service for managing input operations, including creating, updating,
    deleting, and retrieving input records.
    """

    def __init__(self, repository: InputRepository, supplier_service: SupplierService):
        """
        Initializes the InputService with the given repository and supplier service.

        :param repository: Repository for managing input records.
        :param supplier_service: Service for managing supplier-related operations.
        """
        self.repository = repository
        self.supplier_service = supplier_service

    def create_input(self, name: str, category: str, quantity: int, expiration_date, supplier_id: int) -> Optional[Input]:
        """
        Creates a new input if the supplier exists.

        :param name: Name of the input.
        :param category: Category of the input.
        :param quantity: Quantity of the input.
        :param expiration_date: Expiration date of the input.
        :param supplier_id: ID of the supplier associated with the input.
        :return: The created Input object if successful, or None if the supplier does not exist.
        """
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

    def get_input(self, input_id: int) -> Optional[Input]:
        """
        Retrieves an input by its ID.

        :param input_id: ID of the input to be retrieved.
        :return: Input object if found, or None if not found.
        """
        return self.repository.get_input_by_id(input_id)

    def update_input(self, input_id: int, name: str, category: str, quantity: int, expiration_date, supplier_id: int) -> Optional[Input]:
        """
        Updates an existing input.

        :param input_id: ID of the input to be updated.
        :param name: Updated name of the input.
        :param category: Updated category of the input.
        :param quantity: Updated quantity of the input.
        :param expiration_date: Updated expiration date of the input.
        :param supplier_id: Updated supplier ID associated with the input.
        :return: Updated Input object if successful, or None if the input is not found.
        """
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

    def delete_input(self, input_id: int) -> bool:
        """
        Deletes an input by its ID.

        :param input_id: ID of the input to be deleted.
        :return: True if the input was successfully deleted, or False if the input was not found.
        """
        input_item = self.repository.get_input_by_id(input_id)
        if input_item:
            self.repository.delete_input(input_item)
            return True
        return False

    def get_all_inputs(self) -> List[Input]:
        """
        Retrieves all input records.

        :return: List of all Input objects.
        """
        return self.repository.get_all_inputs()

    def supplier_exists(self, supplier_id: int) -> bool:
        """
        Checks if a supplier exists by its ID.

        :param supplier_id: ID of the supplier.
        :return: True if the supplier exists, or False otherwise.
        """
        supplier = self.supplier_service.fetch_supplier(supplier_id)
        return supplier is not None
