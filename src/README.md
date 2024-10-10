
# Farm Tech Agro Supply Management

Farm Tech Agro Supply Management is a command-line interface (CLI) application for managing agricultural supplies, including suppliers, inputs, and stock movements. It aims to streamline the management of agricultural resources by providing tools for tracking stock and managing supplier relationships.

## Features

- **Supplier Management**: Add, update, list, and delete suppliers.
- **Input Management**: Manage agricultural inputs (e.g., seeds, fertilizers) with features to add, update, list, and delete items.
- **Stock Movement Tracking**: Record stock movements for inputs, supporting 'IN' and 'OUT' movements.
- **Command-Line Interface**: The application is designed to be used from the terminal, offering various commands to interact with the system.

## Project Structure

```
farm-tech-agro-supply-management/
├── config/                      # Configuration files
│   ├── env-example              # Example environment variables file
│   └── requirements.txt         # Python dependencies
├── scripts/                     # Utility scripts
├── src/                         # Source code
│   ├── models/                  # Database models
│   ├── repository/              # Data access layer
│   ├── service/                 # Business logic layer
│   └── __init__.py
├── .env                         # Environment variables file (ignored in version control)
├── app.py                       # Main application file for running the CLI
├── README.md                    # Project documentation
├── todo.md                      # To-do list for the project
└── .gitignore                   # Git ignore file
```

## Prerequisites

- Python 3.12 or higher
- Docker (for running the Oracle database)
- Oracle Instant Client (for connecting to the Oracle database)

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd farm-tech-agro-supply-management
   ```

2. **Configure environment variables:**

   - Copy the `env-example` file from the `config` folder to `.env`:

     ```bash
     cp config/env-example .env
     ```

   - Edit the `.env` file to include your database credentials.

3. **Install dependencies:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # For Windows
   source .venv/bin/activate  # For Linux/MacOS

   pip install -r config/requirements.txt
   ```

4. **Set up the database:**

   - Use Docker to run an Oracle database:

     ```bash
     docker run -d -p 1521:1521 \
       -e ORACLE_PASSWORD=123456 \
       -v oracle-volume:/opt/oracle/oradata \
       --name oracle \
       gvenzl/oracle-free
     ```

   - Run the SQL scripts in the `scripts` directory to initialize the database.

5. **Run the application:**

   ```bash
   python app.py --help
   ```

   This command will show a list of available commands.
6. Every command supports the help flag `-h` or `--help` to display usage information.

   ```bash
   python app.py create-supplier --help
   ```

   This command will show the usage information for the `create-supplier` command.

## Usage

The CLI provides the following commands:

- **Supplier Management:**
  - `create-supplier`: Add a new supplier.
  - `get-supplier`: Fetch details of a supplier by ID.
  - `list-suppliers`: List all suppliers.

- **Input Management:**
  - `create-input`: Add a new agricultural input.
  - `get-input`: Fetch details of an input by ID.
  - `list-inputs`: List all inputs.
  - `update-input`: Update an existing input.
  - `delete-input`: Delete an input by ID.

- **Stock Movement:**
  - `create-stock-movement`: Add a stock movement (in or out).
  - `get-stock-movement`: Fetch details of a stock movement by ID.
  - `list-stock-movements`: List all stock movements.

## Configuration

The application uses environment variables for configuration. The following variables are required:

- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOSTNAME`: Database hostname
- `DB_PORT`: Database port (default is `1521`)
- `DB_SERVICE_NAME`: Oracle service name

These should be set in the `.env` file.

## Development

1. **Activate the virtual environment:**

   ```bash
   .venv\Scripts\activate   # For Windows
   source .venv/bin/activate  # For Linux/MacOS
   ```
