import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from service.supplier import SupplierService
from service.supplier_inputs import InputService
from service.stock_movements import StockMovementService, MovementType
from repository.supplier import SupplierRepository
from repository.inputs import InputRepository
from repository.stock_movements import StockMovementRepository


def main():

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_hostname = os.getenv('DB_HOSTNAME')
    db_echo = bool(os.getenv('DB_ECHO'))
    db_port = os.getenv('DB_PORT')
    db_service_name = os.getenv('DB_SERVICE_NAME')

    connection_string = f'oracle+oracledb://{db_user}:{db_password}@{db_hostname}:{db_port}/?service_name={db_service_name}'
    engine = create_engine(connection_string, echo=db_echo)

    Session = sessionmaker(bind=engine)
    session = Session()

    input_repository = InputRepository(session)
    stock_movement_repository = StockMovementRepository(session)

    stock_movement_service = StockMovementService(stock_movement_repository)
    supplier_repository = SupplierRepository(session)
    supplier_service = SupplierService(supplier_repository)
    input_service = InputService(input_repository, supplier_service)

    #supplier_service.create_supplier('test', 'contact_info', 'address')
    expiration_date = datetime.strptime('2021-01-01', '%Y-%m-%d')
    c = input_service.create_input('test', 'category', 10, expiration_date, 1)
    print(c)
    # moviment_date = datetime.strptime('2021-01-01', '%Y-%m-%d')

    # Create a enum for movement_type with the values 'in' and 'out' on upper case


    stock_movement_service.create_stock_movement(2, 1, MovementType.IN)

if __name__ == '__main__':
    main()
