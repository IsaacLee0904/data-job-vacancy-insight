import toml
import psycopg2

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

def create_rawdata_table(logger):
    connector = DatabaseConnector(logger)
    connection = connector.connect_to_db('datawarehouse')
    db_operation = DatabaseOperation(connection, logger)

    job_listings_table_query = """
    CREATE TABLE IF NOT EXISTS job_listings (
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
    db_operation.create_table(job_listings_table_query)
    connection.close()
