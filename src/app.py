import os
import json
import sys
from datetime import datetime

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from service.supplier import SupplierService
from service.supplier_inputs import InputService
from service.stock_movements import StockMovementService
from repository.supplier import SupplierRepository
from repository.inputs import InputRepository
from repository.stock_movements import StockMovementRepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_hostname = os.getenv('DB_HOSTNAME')
db_echo = bool(os.getenv('DEBUG', False))
db_port = os.getenv('DB_PORT')
db_service_name = os.getenv('DB_SERVICE_NAME')

connection_string = f'oracle+oracledb://{db_user}:{db_password}@{db_hostname}:{db_port}/?service_name={db_service_name}'
engine = create_engine(connection_string, echo=False)

Session = sessionmaker(bind=engine)
session = Session()

input_repository = InputRepository(session)
stock_movement_repository = StockMovementRepository(session)
stock_movement_service = StockMovementService(stock_movement_repository)
supplier_repository = SupplierRepository(session)
supplier_service = SupplierService(supplier_repository)
input_service = InputService(input_repository, supplier_service)


def validate_date(ctx, self, value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise click.BadParameter(f"The date '{value}' is not in the correct format (YYYY-MM-DD).")


def validate_env() -> None:
    """Validates the required environment variables."""
    required_vars = [
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOSTNAME',
        'DB_PORT',
        'DB_SERVICE_NAME',
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Required environment variable {var} is missing")


def serialize_model(model):
    """Converts a SQLAlchemy object into a dictionary, excluding unwanted attributes."""
    return {key: value for key, value in model.__dict__.items() if not key.startswith('_')}


def output_json(data):
    """Converts data to JSON and displays it."""
    click.echo(json.dumps(data, default=str, indent=4))


@click.group()
def cli():
    """CLI application for managing agricultural supplies."""
    validate_env()


@click.command()
@click.option('--name', prompt='Supplier name', help='Name of the supplier.')
@click.option('--contact_info', prompt='Contact', help='Contact information of the supplier.')
@click.option('--address', prompt='Address', help='Address of the supplier.')
def create_supplier(name, contact_info, address):
    """Adds a new supplier."""
    supplier = supplier_service.create_supplier(name, contact_info, address)
    output_json({'message': f'Supplier {supplier.name} successfully created!', 'supplier': serialize_model(supplier)})


@click.command()
@click.option('--supplier_id', prompt='Supplier ID', help='ID of the supplier.')
def get_supplier(supplier_id):
    """Fetches a supplier by ID."""
    supplier = supplier_service.fetch_supplier(supplier_id)
    if supplier:
        output_json({'supplier': serialize_model(supplier)})
    else:
        output_json({'error': 'Supplier not found!'})


@click.command()
def list_suppliers():
    """Lists all suppliers."""
    suppliers = supplier_service.fetch_all_suppliers()
    output_json([serialize_model(supplier) for supplier in suppliers])


@click.command()
@click.option('--name', prompt='Input name', help='Name of the input.')
@click.option('--category', prompt='Category', help='Category of the input.')
@click.option('--quantity', prompt='Quantity', help='Available quantity of the input.', type=int)
@click.option('--expiration_date', prompt='Expiration date', help='Expiration date (YYYY-MM-DD).', callback=validate_date)
@click.option('--supplier_id', prompt='Supplier ID', help='ID of the supplier of the input.', type=int)
def create_input(name, category, quantity, expiration_date, supplier_id):
    """Adds a new agricultural input."""
    converted_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    new_input = input_service.create_input(name, category, quantity, converted_date, supplier_id)
    if new_input is None:
        output_json({'error': 'Supplier not found!'})
    else:
        output_json({'message': f'Input {new_input.name} successfully created!', 'input': serialize_model(new_input)})


@click.command()
@click.option('--input_id', prompt='Input ID', help='ID of the input.')
def get_input(input_id):
    """Fetches an input by ID."""
    input_item = input_service.get_input(input_id)
    if input_item:
        output_json({'input': serialize_model(input_item)})
    else:
        output_json({'error': 'Input not found!'})


@click.command()
def list_inputs():
    """Lists all inputs."""
    inputs = input_service.get_all_inputs()
    output_json([serialize_model(input_item) for input_item in inputs])


@click.command()
@click.option('--input_id', prompt='Input ID', help='ID of the input.', type=int)
@click.option('--quantity', prompt='Quantity', help='Quantity moved.', type=int)
@click.option('--movement_type', '-t', prompt='Movement type', help="Movement type ('IN' or 'OUT').",
              type=click.Choice(['IN', 'OUT'], case_sensitive=False))
@click.option('--when', prompt='Movement date', help="Movement date (YYYY-MM-DD).", callback=validate_date)
def create_stock_movement(input_id, quantity, movement_type, when):
    """Adds a stock movement."""
    movement_date = datetime.now()
    if when is not None:
        movement_date = datetime.strptime(when, '%Y-%m-%d')
    movement = stock_movement_service.create_stock_movement(input_id, quantity, movement_type, movement_date)
    output_json({'message': f'{movement.quantity} units of movement successfully created!', 'movement': serialize_model(movement)})


@click.command()
@click.option('--movement_id', prompt='Movement ID', help='ID of the movement.')
def get_stock_movement(movement_id):
    """Fetches a movement by ID."""
    movement = stock_movement_service.get_stock_movement(movement_id)
    if movement:
        output_json({'movement': serialize_model(movement)})
    else:
        output_json({'error': 'Movement not found!'})


@click.command()
def list_stock_movements():
    """Lists all stock movements."""
    movements = stock_movement_service.get_all_stock_movements()
    output_json([serialize_model(movement) for movement in movements])


@click.command()
@click.option('--input_id', prompt='Input ID', help='ID of the input.', type=int)
@click.option('--name', prompt='Input name', help='Name of the input.')
@click.option('--category', prompt='Category', help='Category of the input.')
@click.option('--quantity', prompt='Quantity', help='Available quantity of the input.', type=int)
@click.option('--expiration_date', prompt='Expiration date', help='Expiration date (YYYY-MM-DD).', callback=validate_date)
@click.option('--supplier_id', prompt='Supplier ID', help='ID of the supplier of the input.', type=int)
def update_input(input_id, name, category, quantity, expiration_date, supplier_id):
    """Updates an existing input."""
    converted_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    updated_input = input_service.update_input(input_id, name, category, quantity, converted_date, supplier_id)
    if updated_input is None:
        output_json({'error': 'Input or supplier not found!'})
    else:
        output_json({'message': f'Input {updated_input.name} successfully updated!', 'input': serialize_model(updated_input)})


@click.command()
@click.option('--input_id', prompt='Input ID', help='ID of the input.', type=int)
def delete_input(input_id):
    """Deletes an input by ID."""
    if input_service.delete_input(input_id):
        output_json({'message': 'Input successfully deleted!'})
    else:
        output_json({'error': 'Input not found!'})


cli.add_command(create_supplier)
cli.add_command(get_supplier)
cli.add_command(list_suppliers)
cli.add_command(create_input)
cli.add_command(get_input)
cli.add_command(list_inputs)
cli.add_command(create_stock_movement)
cli.add_command(get_stock_movement)
cli.add_command(list_stock_movements)
cli.add_command(update_input)
cli.add_command(delete_input)

if __name__ == '__main__':
    cli()
