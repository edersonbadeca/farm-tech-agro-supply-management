import os
from datetime import datetime

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from service.supplier import SupplierService
from service.supplier_inputs import InputService
from service.stock_movements import StockMovementService, MovementType
from repository.supplier import SupplierRepository
from repository.inputs import InputRepository
from repository.stock_movements import StockMovementRepository

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
    supplier = supplier_service.fetch_supplier(supplier_id)
    if supplier:
        click.echo(
            f'Fornecedor encontrado: {supplier.name}, Contato: {supplier.contact_info}, Endereço: {supplier.address}')
    else:
        click.echo('Fornecedor não encontrado!')


@click.command()
def list_suppliers():
    """Lista todos os fornecedores."""
    suppliers = supplier_service.fetch_all_suppliers()
    for supplier in suppliers:
        click.echo(f'{supplier.id}: {supplier.name}, Contato: {supplier.contact_info}, Endereço: {supplier.address}')


@click.command()
@click.option('--name', prompt='Nome do insumo', help='Nome do insumo.')
@click.option('--category', prompt='Categoria', help='Categoria do insumo.')
@click.option('--quantity', prompt='Quantidade', help='Quantidade disponível do insumo.', type=int)
@click.option('--expiration_date', prompt='Data de expiração', help='Data de expiração (YYYY-MM-DD).',  callback=validate_date)
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor do insumo.', type=int)
def create_input(name, category, quantity, expiration_date, supplier_id):
    """Adiciona um novo insumo agrícola."""
    converted_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    new_input = input_service.create_input(name, category, quantity, converted_date, supplier_id)
    if new_input is None:
        click.echo('Fornecedor não encontrado!')
        return
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
@click.option('--movement_type', '-t', prompt='Tipo de movimentação', help="Tipo de movimentação ('IN' ou 'OUT').",
              type=click.Choice(['IN', 'OUT'], case_sensitive=False))
@click.option('--when', prompt='Data da movimentação', help="Data da  movimentação (YYYY-MM-DD).",  callback=validate_date)
def create_stock_movement(input_id, quantity, type, when):
    """Adiciona uma movimentação de estoque."""
    movement_date = datetime.now()
    if when is not None:
        movement_date = datetime.strptime(when, '%Y-%m-%d')
    movement = stock_movement_service.create_stock_movement(input_id, quantity, type, movement_date)
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
        click.echo('Insumo ou fornecedor não encontrado!')
        return
    click.echo(f'Insumo {updated_input.name} atualizado com sucesso!')

@click.command()
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo.', type=int)
def delete_input(input_id):
    """Deleta um insumo por ID."""
    if input_service.delete_input(input_id):
        click.echo('Insumo deletado com sucesso!')
    else:
        click.echo('Insumo não encontrado!')


@click.command()
@click.option('--id', default=None, prompt='ID do fornecedor', help='ID do fornecedor.', type=int)
@click.option('--name', '-n', default=None, help='Nome do fornecedor.')
@click.option('--contact_info', '-c', default=None, help='Informações de contato do fornecedor.')
@click.option('--address', '-a', default=None, help='Endereço do fornecedor.')
def update_supplier(id, name, contact_info, address):
    """Atualiza um fornecedor existente."""
    supplier = supplier_service.fetch_supplier(id)
    if supplier is None:
        click.echo('Fornecedor não encontrado!')
        return
    if name is None:
        name = supplier.name
    if contact_info is None:
        contact_info = supplier.contact_info
    if address is None:
        address = supplier.address

    updated_supplier = supplier_service.update_supplier(id, name, contact_info, address)

    click.echo(f'Fornecedor {updated_supplier.name} atualizado com sucesso!')

@click.command()
@click.option('--supplier_id', prompt='ID do fornecedor', help='ID do fornecedor.', type=int)
def delete_supplier(supplier_id):
    """Deleta um fornecedor por ID."""
    if supplier_service.delete_supplier(supplier_id):
        click.echo('Fornecedor deletado com sucesso!')
    else:
        click.echo('Fornecedor não encontrado!')

@click.command()
@click.option('--movement_id', prompt='ID da movimentação', help='ID da movimentação.', type=int)
@click.option('--input_id', prompt='ID do insumo', help='ID do insumo associado à movimentação.', type=int)
@click.option('--quantity', prompt='Quantidade', help='Quantidade movimentada.', type=int)
@click.option('--type', '-t', prompt='Tipo de movimentação', help="Tipo de movimentação ('IN' ou 'OUT').",
              type=click.Choice(['IN', 'OUT'], case_sensitive=False))
def update_stock_movement(movement_id, input_id, quantity, movement_type):
    """Atualiza uma movimentação de estoque existente."""
    if movement_type not in [MovementType.IN.value, MovementType.OUT.value]:
        click.echo('Tipo de movimentação inválido! Use "IN" ou "OUT".')
        return

    updated_movement = stock_movement_service.update_stock_movement(movement_id, input_id, quantity, movement_type)
    if updated_movement is None:
        click.echo('Movimentação de estoque não encontrada!')
        return

    click.echo(f'Movimentação {updated_movement.id} atualizada com sucesso!')

@click.command()
@click.option('--movement_id', prompt='ID da movimentação', help='ID da movimentação.', type=int)
def delete_stock_movement(movement_id):
    """Deleta uma movimentação de estoque por ID."""
    if stock_movement_service.delete_stock_movement(movement_id):
        click.echo('Movimentação de estoque deletada com sucesso!')
    else:
        click.echo('Movimentação de estoque não encontrada!')


cli.add_command(update_stock_movement)
cli.add_command(delete_stock_movement)

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
cli.add_command(update_supplier)
cli.add_command(delete_supplier)


if __name__ == '__main__':
    cli()
