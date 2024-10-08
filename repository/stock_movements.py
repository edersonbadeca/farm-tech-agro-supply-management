from sqlalchemy.orm import Session
from models.models import StockMovement

class StockMovementRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_stock_movement(self, stock_movement: StockMovement):
        self.session.add(stock_movement)
        self.session.commit()

    def get_stock_movement_by_id(self, movement_id: int):
        return self.session.query(StockMovement).filter(StockMovement.id == movement_id).first()

    def update_stock_movement(self, stock_movement: StockMovement):
        self.session.merge(stock_movement)
        self.session.commit()

    def delete_stock_movement(self, stock_movement: StockMovement):
        self.session.delete(stock_movement)
        self.session.commit()

    def get_all_stock_movements(self):
        return self.session.query(StockMovement).all()
