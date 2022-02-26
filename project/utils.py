import logging
import sqlite3


class DatabaseUtility:
    def __init__(self, database):
        self.db = database
        self.cur = database.cursor()
        # self.execute_sql = lambda code: self.cur.execute(code)


    def execute_sql(self, code:str):
        logging.info(f'Excecuting SQLite code: {code}')
        try:
            self.cur.execute(code)
        except sqlite3.OperationalError as error:
            logging.error(f'Operational Error while executing SQLite code: {error}')
            raise Exception(error)

        self.db.commit()


    def create_table(self, table_name:str, columns:tuple[str]) -> None:
        """ Create a table in the database
        :param table_name: Name of the new table (must be unique)
        :param columns: a tuple of strings containing column name data type and other
        """
        self.execute_sql(
            f"CREATE TABLE IF NOT EXISTS {table_name} {columns};"
        )


    def insert_row(self, table_name:str, values:tuple[str]) -> None:
        """ Insert row into the database
        :param table_name: Name of the new table (table must exist)
        :param values: tuple of strings containing values to insert
        """ 
        self.execute_sql(
            f"INSERT INTO  {table_name} VALUES {values};"
        )
        
    def update_row(self, table_name:str, values:tuple|str, where:tuple|str) -> None:
        """
        """
        self.execute_sql(
            f"UPDATE {table_name} SET {values} WHERE {where};"
        )
        

    def get_row(self, table_name:str, values:tuple, additional_arg:str=""):
        """ Gets and returns a row from the database
        :param table_name: Name of the new table (table must exist)
        :param values: tuple of strings containing values to get
        :param additional_arg: place for more sqlite code like WHERE
        """
        self.execute_sql(
            f"SELECT {values} FROM {table_name} {additional_arg};"
        )
        return self.cur.fetchall()


    def delete_table(self, table_name:str) -> None:
        """ Deletes a table from the database
        :param table_name: Name of the new table (table must exist)
        """
        self.execute_sql(
            f"DROP TABLE {table_name};"
        )


    def delete_row(self, table_name:str, where:str) -> None:
        """ Deletes a row from the database
        :param table_name: Name of the new table (table must exist)
        :param where: decides what row to delete
        """
        self.execute_sql(
            f"DELETE FROM {table_name} WHERE {where}"
        )

