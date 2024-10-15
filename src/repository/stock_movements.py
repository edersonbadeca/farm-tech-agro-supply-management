from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Type
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

    def generate_movement_report(self):
        sql = text("""
            SELECT 
                sm.id AS movement_id,
                sm.quantity AS movement_quantity,
                sm.movement_type AS movement_type,
                sm.movement_date AS movement_date,
                i.name AS input_name,
                s.name AS supplier_name
            FROM 
                stock_movements sm
            JOIN 
                inputs i ON sm.input_id = i.id
            JOIN 
                suppliers s ON i.supplier_id = s.id
        """)
        result = self.session.execute(sql).mappings().all()
        print(result)
        return [{
            'movement_id': row['movement_id'],
            'movement_quantity': row['movement_quantity'],
            'movement_type': row['movement_type'],
            'movement_date': row['movement_date'],
            'input_name': row['input_name'],
            'supplier_name': row['supplier_name'],
        } for row in result]
