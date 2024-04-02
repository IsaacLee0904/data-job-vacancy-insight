import toml
import psycopg2
import psycopg2.extras

class DatabaseConnector:
    def __init__(self, logger):
        """
        Initialize the DatabaseConnector class with the path to the configuration file and a logger.

        Parameters:
        - config_path (str): The file path to the TOML configuration file.
        - logger (logging.Logger): A Logger object for logging information and errors.
        """
        self.config = toml.load('config/database_config.toml')
        self.logger = logger

    def connect_to_db(self, db_name):
        """
        Establish a connection to the database specified in the configuration file.

        Parameters:
        - db_name (str): The database name to connect to, as defined in the TOML file.

        Returns:
        - A connection object if successful, None otherwise.
        """
        db_config = self.config[db_name]
        try:
            connection = psycopg2.connect(
                dbname=db_config['db'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
            self.logger.info(f"Successfully connected to {db_name}")
            return connection
        except Exception as e:
            self.logger.error(f"Error connecting to {db_name}: {e}")
            return None

class DatabaseOperation:
    def __init__(self, connection, logger):
        """
        Initialize the DatabaseOperation with a database connection and a logger.

        Parameters:
        - connection: The connection object to the database.
        - logger (logging.Logger): A Logger object for logging information and errors.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.logger = logger

    def create_table(self, create_table_query):
        """
        Create a table in the database based on the provided SQL query.

        Parameters:
        - create_table_query (str): The SQL query to create a table.
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            self.logger.info("Table created successfully.")
        except psycopg2.Error as e:
            self.logger.error(f"An error occurred while creating the table: {e}")
            self.connection.rollback()

    def create_schema(self, schema_name):
        """
        Create a schema in the database if it doesn't already exist.

        Parameters:
        - schema_name (str): The name of the schema to be created.
        """
        create_schema_query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        try:
            self.cursor.execute(create_schema_query)
            self.connection.commit()
            self.logger.info(f"Schema '{schema_name}' created successfully.")
        except psycopg2.Error as e:
            self.logger.error(f"An error occurred while creating the schema '{schema_name}': {e}")
            self.connection.rollback()

    def insert_data(self, table_name, df):
        """
        Insert data from a pandas DataFrame into the specified table.

        Parameters:
        - table_name (str): The name of the table to insert data into.
        - df (pd.DataFrame): The DataFrame containing the data to be inserted.
        """
        cols = ','.join(list(df.columns))
        values = ','.join(['%s'] * len(df.columns))
        insert_stmt = f"INSERT INTO {table_name} ({cols}) VALUES ({values})"

        records = [tuple(x) for x in df.to_numpy()]

        try:
            psycopg2.extras.execute_batch(self.cursor, insert_stmt, records)
            self.connection.commit()
            self.logger.info(f"Successfully inserted data into {table_name}.")
        except Exception as e:
            self.logger.error(f"Error inserting data into {table_name}: {e}")
            self.connection.rollback()

# craete function 
def create_rawdata_table(logger):
    """
    Create a specified schema and a table within that schema in the 'datawarehouse' database.

    This function first establishes a connection to the 'datawarehouse' database, then creates a 
    schema named 'my_schema'. After the schema is successfully created, it creates a 'job_listings' 
    table within this schema if it does not already exist.

    Parameters:
    - logger (logging.Logger): A Logger object for logging information and errors.

    The table 'job_listings' will have various fields such as id, job_title, company_name, etc.,
    with appropriate data types assigned to each field.
    """
    # Establish a connection to the 'datawarehouse' database.
    connector = DatabaseConnector(logger)
    connection = connector.connect_to_db('datawarehouse')
    db_operation = DatabaseOperation(connection, logger)

    # Create a new schema named 'datawarehouse'.
    schema_name = "source_data"  # Define the schema name to be created.
    db_operation.create_schema(schema_name)

    # Create the 'job_listings' table within the newly created schema.
    job_listings_104_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.job_listings_104 (
        id SERIAL PRIMARY KEY,
        job_title VARCHAR(255) NOT NULL,
        company_name VARCHAR(255) NOT NULL,
        salary VARCHAR(255),
        location VARCHAR(255),
        job_description TEXT,
        job_type VARCHAR(50),
        degree_required VARCHAR(255),
        major_required VARCHAR(255),
        experience VARCHAR(255),
        skill TEXT,
        tools TEXT,
        others TEXT,
        url TEXT,
        crawl_date DATE
    );
    """
    # Execute the SQL query to create the table.
    db_operation.create_table(job_listings_104_table_query)

    # Close the database connection.
    connection.close()