from datetime import datetime
from enum import Enum
from typing import Optional, Type

from repository.stock_movements import StockMovementRepository
from models.models import StockMovement


class MovementType(Enum):
    """
    Enum for representing movement types in stock movements.
    """
    IN = 'IN'
    OUT = 'OUT'


class StockMovementService:
    """
    Service for managing stock movement operations, including creating, updating,
    deleting, and retrieving stock movement records.
    """

    def __init__(self, repository: StockMovementRepository):
        """
        Initializes the StockMovementService with the given repository.

        :param repository: Repository for managing stock movement records.
        """
        self.repository = repository

    def create_stock_movement(self, input_id: int, quantity: int, movement_type: str,
                              movement_date: datetime.date = datetime.now().date()) -> StockMovement:
        """
        Creates a new stock movement.

        :param input_id: ID of the input associated with the stock movement.
        :param quantity: Quantity of the stock movement.
        :param movement_type: Type of the stock movement (IN or OUT).
        :param movement_date: Date of the stock movement. Defaults to today's date.
        :return: The created StockMovement object.
        """
        new_movement = StockMovement(
            input_id=input_id,
            quantity=quantity,
            movement_type=movement_type,
            movement_date=movement_date
        )
        self.repository.add_stock_movement(new_movement)
        return new_movement

    def get_stock_movement(self, movement_id: int) -> Optional[StockMovement]:
        """
        Retrieves a stock movement by its ID.

        :param movement_id: ID of the stock movement to be retrieved.
        :return: StockMovement object if found, or None if not found.
        """
        return self.repository.get_stock_movement_by_id(movement_id)

    def update_stock_movement(self, movement_id: int, input_id: int, quantity: int, movement_type: str) -> Optional[
        StockMovement]:
        """
        Updates an existing stock movement.

        :param movement_id: ID of the stock movement to be updated.
        :param input_id: Updated ID of the input associated with the stock movement.
        :param quantity: Updated quantity of the stock movement.
        :param movement_type: Updated type of the stock movement.
        :return: Updated StockMovement object if successful, or None if the stock movement is not found.
        """
        stock_movement = self.repository.get_stock_movement_by_id(movement_id)
        if stock_movement:
            stock_movement.input_id = input_id
            stock_movement.quantity = quantity
            stock_movement.movement_type = movement_type
            self.repository.update_stock_movement(stock_movement)
            return stock_movement
        return None

    def delete_stock_movement(self, movement_id: int) -> bool:
        """
        Deletes a stock movement by its ID.

        :param movement_id: ID of the stock movement to be deleted.
        :return: True if the stock movement was successfully deleted, or False if the stock movement was not found.
        """
        stock_movement = self.repository.get_stock_movement_by_id(movement_id)
        if stock_movement:
            self.repository.delete_stock_movement(stock_movement)
            return True
        return False

    def get_all_stock_movements(self) -> list[Type[StockMovement]]:
        """
        Retrieves all stock movements from the database.

        :return: List of all StockMovement objects.
        """
        return self.repository.get_all_stock_movements()
