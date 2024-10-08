# services/service_stock_movements.py
from repository.stock_movements import StockMovementRepository
from models.models import StockMovement

class StockMovementService:
    def __init__(self, repository: StockMovementRepository):
        self.repository = repository

    def create_stock_movement(self, input_id: int, quantity: int, movement_type: str):
        new_movement = StockMovement(input_id=input_id, quantity=quantity, movement_type=movement_type)
        self.repository.add_stock_movement(new_movement)
        return new_movement

    def get_stock_movement(self, movement_id: int):
        return self.repository.get_stock_movement_by_id(movement_id)

    def update_stock_movement(self, movement_id: int, input_id: int, quantity: int, movement_type: str):
        stock_movement = self.repository.get_stock_movement_by_id(movement_id)
        if stock_movement:
            stock_movement.input_id = input_id
            stock_movement.quantity = quantity
            stock_movement.movement_type = movement_type
            self.repository.update_stock_movement(stock_movement)
            return stock_movement
        return None

    def delete_stock_movement(self, movement_id: int):
        stock_movement = self.repository.get_stock_movement_by_id(movement_id)
        if stock_movement:
            self.repository.delete_stock_movement(stock_movement)
            return True
        return False

    def get_all_stock_movements(self):
        return self.repository.get_all_stock_movements()
