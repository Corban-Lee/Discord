class DatabaseUtility:
    def __init__(self, database):
        self.db = database
        self.cur = database.cursor()
        self.execute_sql = lambda code: self.cur.execute(code)


    def create_table(self, table_name:str, columns:tuple):
        self.execute_sql(f'CREATE TABLE {table_name} {columns}')


    def insert(self, table_name:str, values:tuple):
        self.execute_sql(f'INSERT INTO {table_name} VALUES {values}')


    def get(self, table_name:str, values:tuple, orderby:tuple=None) -> tuple:
        code = f'SELECT {values} FROM {table_name}' + f' ORDER BY {orderby}' if orderby else ''
        return self.execute_sql(code)
        
        