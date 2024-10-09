import os
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from service.supplier import SupplierService
from service.supplier_inputs import InputService
from service.stock_movements import StockMovementService
from repository.supplier import SupplierRepository
from repository.inputs import InputRepository
from repository.stock_movements import StockMovementRepository

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
input_service = InputService(input_repository)
stock_movement_service = StockMovementService(stock_movement_repository)
supplier_repository = SupplierRepository(session)
supplier_service = SupplierService(supplier_repository)


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
    click.echo(f'Fornecedor {supplier.name} criado com sucesso!')


@click.command()
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor.')
def get_supplier(supplier_id):
    """Consulta um fornecedor por ID."""
    supplier = supplier_service.get_supplier(supplier_id)
    if supplier:
        click.echo(
            f'Fornecedor encontrado: {supplier.name}, Contato: {supplier.contact_info}, Endereço: {supplier.address}')
    else:
        click.echo('Fornecedor não encontrado!')


@click.command()
def list_suppliers():
    """Lista todos os fornecedores."""
    suppliers = supplier_service.get_all_suppliers()
    for supplier in suppliers:
        click.echo(f'{supplier.id}: {supplier.name}, Contato: {supplier.contact_info}, Endereço: {supplier.address}')


@click.command()
@click.option('--name', prompt='Nome do insumo', help='Nome do insumo.')
@click.option('--category', prompt='Categoria', help='Categoria do insumo.')
@click.option('--quantity', prompt='Quantidade', help='Quantidade disponível do insumo.', type=int)
@click.option('--expiration_date', prompt='Data de expiração', help='Data de expiração (YYYY-MM-DD).')
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor do insumo.', type=int)
def create_input(name, category, quantity, expiration_date, supplier_id):
    """Adiciona um novo insumo agrícola."""
    new_input = input_service.create_input(name, category, quantity, expiration_date, supplier_id)
    click.echo(f'Insumo {new_input.name} criado com sucesso!')


@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.')
def get_input(input_id):
    """Consulta um insumo por ID."""
    input_item = input_service.get_input(input_id)
    if input_item:
        click.echo(
            f'Insumo encontrado: {input_item.name}, Categoria: {input_item.category}, Quantidade: {input_item.quantity}, Data de Expiração: {input_item.expiration_date}')
    else:
        click.echo('Insumo não encontrado!')


@click.command()
def list_inputs():
    """Lista todos os insumos."""
    inputs = input_service.get_all_inputs()
    for input_item in inputs:
        click.echo(
            f'{input_item.id}: {input_item.name}, Categoria: {input_item.category}, Quantidade: {input_item.quantity}, Expiração: {input_item.expiration_date}')


@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.', type=int)
@click.option('--quantity', prompt='Quantidade', help='Quantidade movimentada.', type=int)
@click.option('--movement_type', prompt='Tipo de movimentação', help="Tipo de movimentação ('in' ou 'out').")
def create_stock_movement(input_id, quantity, movement_type):
    """Adiciona uma movimentação de estoque."""
    movement = stock_movement_service.create_stock_movement(input_id, quantity, movement_type)
    click.echo(f'Movimentação de {movement.quantity} unidades criada com sucesso!')


@click.command()
@click.option('--movement_id', prompt='ID da movimentação', help='ID da movimentação.')
def get_stock_movement(movement_id):
    """Consulta uma movimentação por ID."""
    movement = stock_movement_service.get_stock_movement(movement_id)
    if movement:
        click.echo(
            f'Movimentação encontrada: {movement.id}, Tipo: {movement.movement_type}, Quantidade: {movement.quantity}')
    else:
        click.echo('Movimentação não encontrada!')


@click.command()
def list_stock_movements():
    """Lista todas as movimentações de estoque."""
    movements = stock_movement_service.get_all_stock_movements()
    for movement in movements:
        click.echo(
            f'{movement.id}: Tipo: {movement.movement_type}, Quantidade: {movement.quantity}, Data: {movement.movement_date}')


# Adicionando os comandos ao grupo CLI
cli.add_command(create_supplier)
cli.add_command(get_supplier)
cli.add_command(list_suppliers)

cli.add_command(create_input)
cli.add_command(get_input)
cli.add_command(list_inputs)

cli.add_command(create_stock_movement)
cli.add_command(get_stock_movement)
cli.add_command(list_stock_movements)

if __name__ == '__main__':
    cli()
