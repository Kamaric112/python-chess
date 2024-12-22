import mysql.connector
import logging

logging.basicConfig(filename='chess/chess_game_event.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config.db_host,
                user=self.config.db_user,
                password=self.config.db_password,
                database=self.config.db_name
            )
            self.cursor = self.connection.cursor()
            logging.info("Database connection successful.")
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to database: {err}")
            raise

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            logging.info("Database connection closed.")

    def save_match(self, winner_name):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            query = "INSERT INTO matches (winner_name) VALUES (%s)"
            self.cursor.execute(query, (winner_name,))
            self.connection.commit()
            logging.info(f"Match saved to database. Winner: {winner_name}")
        except mysql.connector.Error as err:
            logging.error(f"Error saving match to database: {err}")
            self.connection.rollback()
        finally:
            self.close()
