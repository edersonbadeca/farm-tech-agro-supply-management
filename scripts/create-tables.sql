CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100),
    address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS inputs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    expiration_date DATE NOT NULL,
    supplier_id INTEGER,
    addition_date DATE NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY,
    input_id INTEGER,
    quantity INTEGER NOT NULL,
    movement_type VARCHAR(10) NOT NULL,  -- 'in' for stock additions, 'out' for stock deductions
    movement_date DATE NOT NULL,
    FOREIGN KEY (input_id) REFERENCES inputs(id)
);
