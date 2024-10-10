from sqlalchemy.orm import Session
from typing import List, Optional, Type
from models.models import StockMovement

class StockMovementRepository:
    """
    Repository for managing stock movement operations in the database.
    """

    def __init__(self, session: Session):
        """
        Initializes the repository with a database session.

        :param session: SQLAlchemy session for interacting with the database.
        """
        self.session = session

    def add_stock_movement(self, stock_movement: StockMovement) -> None:
        """
        Adds a new stock movement to the database.

        :param stock_movement: StockMovement object to be added.
        """
        self.session.add(stock_movement)
        self.session.commit()

    def get_stock_movement_by_id(self, movement_id: int) -> Optional[StockMovement]:
        """
        Retrieves a stock movement by its ID.

        :param movement_id: ID of the stock movement to be retrieved.
        :return: StockMovement object corresponding to the provided ID, or None if not found.
        """
        return self.session.query(StockMovement).filter(StockMovement.id == movement_id).first()

    def update_stock_movement(self, stock_movement: StockMovement) -> None:
        """
        Updates the information of an existing stock movement.

        :param stock_movement: StockMovement object with the updated data.
        """
        self.session.merge(stock_movement)
        self.session.commit()

    def delete_stock_movement(self, stock_movement: StockMovement) -> None:
        """
        Removes a stock movement from the database.

        :param stock_movement: StockMovement object to be removed.
        """
        self.session.delete(stock_movement)
        self.session.commit()

    def get_all_stock_movements(self) -> list[Type[StockMovement]]:
        """
        Retrieves all stock movements from the database.

        :return: List of StockMovement objects.
        """
        return self.session.query(StockMovement).all()
