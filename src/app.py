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
engine = create_engine(connection_string, echo=db_echo)

Session = sessionmaker(bind=engine)
session = Session()

input_repository = InputRepository(session)
stock_movement_repository = StockMovementRepository(session)
stock_movement_service = StockMovementService(stock_movement_repository)
supplier_repository = SupplierRepository(session)
supplier_service = SupplierService(supplier_repository)
input_service = InputService(input_repository, supplier_service)


def validate_date(value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return value
    except ValueError:
        raise click.BadParameter(f"A data '{value}' não está no formato correto (YYYY-MM-DD).")


def validate_env() -> None:
    """Valida as variáveis de ambiente necessárias."""
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
    """Converte um objeto SQLAlchemy em um dicionário, excluindo atributos indesejados."""
    return {key: value for key, value in model.__dict__.items() if not key.startswith('_')}


def output_json(data):
    """Converte os dados para JSON e exibe."""
    click.echo(json.dumps(data, default=str, indent=4))


@click.group()
def cli():
    """Aplicação CLI para gestão de insumos agrícolas."""
    validate_env()


@click.command()
@click.option('--name', prompt='Nome do fornecedor', help='Nome do fornecedor.')
@click.option('--contact_info', prompt='Contato', help='Informações de contato do fornecedor.')
@click.option('--address', prompt='Endereço', help='Endereço do fornecedor.')
def create_supplier(name, contact_info, address):
    """Adiciona um novo fornecedor."""
    supplier = supplier_service.create_supplier(name, contact_info, address)
    output_json({'message': f'Fornecedor {supplier.name} criado com sucesso!', 'supplier': serialize_model(supplier)})


@click.command()
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor.')
def get_supplier(supplier_id):
    """Consulta um fornecedor por ID."""
    supplier = supplier_service.fetch_supplier(supplier_id)
    if supplier:
        output_json({'supplier': serialize_model(supplier)})
    else:
        output_json({'error': 'Fornecedor não encontrado!'})


@click.command()
def list_suppliers():
    """Lista todos os fornecedores."""
    suppliers = supplier_service.fetch_all_suppliers()
    output_json([serialize_model(supplier) for supplier in suppliers])


@click.command()
@click.option('--name', prompt='Nome do insumo', help='Nome do insumo.')
@click.option('--category', prompt='Categoria', help='Categoria do insumo.')
@click.option('--quantity', prompt='Quantidade', help='Quantidade disponível do insumo.', type=int)
@click.option('--expiration_date', prompt='Data de expiração', help='Data de expiração (YYYY-MM-DD).', callback=validate_date)
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor do insumo.', type=int)
def create_input(name, category, quantity, expiration_date, supplier_id):
    """Adiciona um novo insumo agrícola."""
    converted_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    new_input = input_service.create_input(name, category, quantity, converted_date, supplier_id)
    if new_input is None:
        output_json({'error': 'Fornecedor não encontrado!'})
    else:
        output_json({'message': f'Insumo {new_input.name} criado com sucesso!', 'input': serialize_model(new_input)})


@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.')
def get_input(input_id):
    """Consulta um insumo por ID."""
    input_item = input_service.get_input(input_id)
    if input_item:
        output_json({'input': serialize_model(input_item)})
    else:
        output_json({'error': 'Insumo não encontrado!'})


@click.command()
def list_inputs():
    """Lista todos os insumos."""
    inputs = input_service.get_all_inputs()
    output_json([serialize_model(input_item) for input_item in inputs])


@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.', type=int)
@click.option('--quantity', prompt='Quantidade', help='Quantidade movimentada.', type=int)
@click.option('--movement_type', '-t', prompt='Tipo de movimentação', help="Tipo de movimentação ('IN' ou 'OUT').",
              type=click.Choice(['IN', 'OUT'], case_sensitive=False))
@click.option('--when', prompt='Data da movimentação', help="Data da movimentação (YYYY-MM-DD).", callback=validate_date)
def create_stock_movement(input_id, quantity, movement_type, when):
    """Adiciona uma movimentação de estoque."""
    movement_date = datetime.now()
    if when is not None:
        movement_date = datetime.strptime(when, '%Y-%m-%d')
    movement = stock_movement_service.create_stock_movement(input_id, quantity, movement_type, movement_date)
    output_json({'message': f'Movimentação de {movement.quantity} unidades criada com sucesso!', 'movement': serialize_model(movement)})


@click.command()
@click.option('--movement_id', prompt='ID da movimentação', help='ID da movimentação.')
def get_stock_movement(movement_id):
    """Consulta uma movimentação por ID."""
    movement = stock_movement_service.get_stock_movement(movement_id)
    if movement:
        output_json({'movement': serialize_model(movement)})
    else:
        output_json({'error': 'Movimentação não encontrada!'})


@click.command()
def list_stock_movements():
    """Lista todas as movimentações de estoque."""
    movements = stock_movement_service.get_all_stock_movements()
    output_json([serialize_model(movement) for movement in movements])


@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.', type=int)
@click.option('--name', prompt='Nome do insumo', help='Nome do insumo.')
@click.option('--category', prompt='Categoria', help='Categoria do insumo.')
@click.option('--quantity', prompt='Quantidade', help='Quantidade disponível do insumo.', type=int)
@click.option('--expiration_date', prompt='Data de expiração', help='Data de expiração (YYYY-MM-DD).', callback=validate_date)
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor do insumo.', type=int)
def update_input(input_id, name, category, quantity, expiration_date, supplier_id):
    """Atualiza um insumo existente."""
    converted_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    updated_input = input_service.update_input(input_id, name, category, quantity, converted_date, supplier_id)
    if updated_input is None:
        output_json({'error': 'Insumo ou fornecedor não encontrado!'})
    else:
        output_json({'message': f'Insumo {updated_input.name} atualizado com sucesso!', 'input': serialize_model(updated_input)})


@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.', type=int)
def delete_input(input_id):
    """Deleta um insumo por ID."""
    if input_service.delete_input(input_id):
        output_json({'message': 'Insumo deletado com sucesso!'})
    else:
        output_json({'error': 'Insumo não encontrado!'})


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
