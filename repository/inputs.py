from sqlalchemy.orm import Session
from models.models import Input

class InputRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_input(self, input_item: Input):
        self.session.add(input_item)
        self.session.commit()

    def get_input_by_id(self, input_id: int):
        return self.session.query(Input).filter(Input.id == input_id).first()

    def update_input(self, input_item: Input):
        self.session.merge(input_item)
        self.session.commit()

    def delete_input(self, input_item: Input):
        self.session.delete(input_item)
        self.session.commit()

    def get_all_inputs(self):
        return self.session.query(Input).all()
