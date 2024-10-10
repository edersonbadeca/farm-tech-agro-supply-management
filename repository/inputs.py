from sqlalchemy.orm import Session
from typing import List, Optional
from models.models import Input

class InputRepository:
    """
    Repository for managing input operations in the database.
    """

    def __init__(self, session: Session):
        """
        Initializes the repository with a database session.

        :param session: SQLAlchemy session for interacting with the database.
        """
        self.session = session

    def add_input(self, input_item: Input) -> None:
        """
        Adds a new input to the database.

        :param input_item: Input object to be added.
        """
        self.session.add(input_item)
        self.session.commit()

    def get_input_by_id(self, input_id: int) -> Optional[Input]:
        """
        Retrieves an input by its ID.

        :param input_id: ID of the input to be retrieved.
        :return: Input object corresponding to the provided ID, or None if not found.
        """
        return self.session.query(Input).filter(Input.id == input_id).first()

    def update_input(self, input_item: Input) -> None:
        """
        Updates the information of an existing input.

        :param input_item: Input object with the updated data.
        """
        self.session.merge(input_item)
        self.session.commit()

    def delete_input(self, input_item: Input) -> None:
        """
        Removes an input from the database.

        :param input_item: Input object to be removed.
        """
        self.session.delete(input_item)
        self.session.commit()

    def get_all_inputs(self) -> List[Input]:
        """
        Retrieves all inputs from the database.

        :return: List of Input objects.
        """
        return self.session.query(Input).all()
