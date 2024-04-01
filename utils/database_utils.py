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