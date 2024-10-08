CREATE TABLE IF NOT EXISTS APP.suppliers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100),
    address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS APP.inputs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    expiration_date DATE NOT NULL,
    supplier_id INTEGER,
    addition_date DATE NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES APP.suppliers(id)
);

CREATE TABLE IF NOT EXISTS APP.stock_movements (
    id INTEGER PRIMARY KEY,
    input_id INTEGER,
    quantity INTEGER NOT NULL,
    movement_type VARCHAR(10) NOT NULL,
    movement_date DATE NOT NULL,
    FOREIGN KEY (input_id) REFERENCES APP.inputs(id)
);
CREATE USER APP IDENTIFIED BY 123456;

ALTER USER APP QUOTA UNLIMITED ON USERS;
ALTER USER APP QUOTA 500M ON USERS;