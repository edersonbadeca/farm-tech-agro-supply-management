from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(100))
    address = Column(String(255))

    # Relacionamento com a tabela Input
    inputs = relationship('Input', back_populates='supplier')


class Input(Base):
    __tablename__ = 'inputs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    quantity = Column(Numeric, nullable=False)
    expiration_date = Column(Date, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    addition_date = Column(Date, nullable=False)

    # Relacionamento com a tabela Supplier
    supplier = relationship('Supplier', back_populates='inputs')

    # Relacionamento com a tabela StockMovement
    stock_movements = relationship('StockMovement', back_populates='input')


class StockMovement(Base):
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_id = Column(Integer, ForeignKey('inputs.id'), nullable=False)
    quantity = Column(Numeric, nullable=False)
    movement_type = Column(String(10), nullable=False)
    movement_date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("movement_type IN ('in', 'out')", name='check_movement_type'),
    )

    # Relacionamento com a tabela Input
    input = relationship('Input', back_populates='stock_movements')
