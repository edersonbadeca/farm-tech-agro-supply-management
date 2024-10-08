import os


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base
from repository.repository import Repository
from service.supplier_service import SupplierService


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

    Base.metadata.create_all(engine)

    repository = Repository(session)
    supplier_service = SupplierService(repository)

    new_supplier = supplier_service.create_supplier(
        name="Fornecedor B",
        contact_info="contato@fornecedorb.com",
        address="Rua do Fornecedor B"
    )
    print(f"Fornecedor criado: {new_supplier.name}")

if __name__ == '__main__':
    main()