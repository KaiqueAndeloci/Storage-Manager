# import pyodbc as BD
import pathlib, json
import sqlite3 as DB
from os.path import exists


class SQLite():
    def __init__(self, layout_filename:str):
        self.layout_filename = layout_filename

    def Init_main(self):
        try:
            absolute_path = str(pathlib.Path(__file__).parent.absolute())
            path = f'{absolute_path.replace('CRUD', 'db.sqlite3')}'
            self.conn = DB.connect(database=path)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")

            DB_table = self.cursor.fetchall()
            # print('\n')
            # print(r''+ f'{absolute_path.replace('DB\\CRUD', '')}{self.layout_filename}')
            # print('\n')
            with open(f'{absolute_path.replace('DB\\CRUD', '')}{self.layout_filename}', "r", encoding="utf-8") as arquivo:
                layout_table = json.load(arquivo)


            self._Verify_layout(layout_table['tables'], DB_table)
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")

            DB_formated_table = self.cursor.fetchall()
            #self._Verify_permissions_table(DB_formated_table, layout_table['config']['permissions_table_name'])

            if exists(f'{absolute_path.replace('DB\\CRUD', 'logs\\09-2025.log')}') == False:
                pass

        except Exception as err:
            print(err)

    def _Verify_permissions_table(self, DB_table: list, permissions_table_name: str):
        #SELECT COUNT(*) FROM nome_da_tabela;
        table_exists = False
        formated_DB_table = []

        for DB_table_name in DB_table:
            if DB_table_name[0] == self._Format_string(permissions_table_name):
                table_exists = True
                break

        if table_exists == False:
            Exception("bad layout")

        self.cursor.execute(f"SELECT * FROM {permissions_table_name};")
        db_permissions = self.cursor.fetchall()

        # verificar as permissoes
        # for DB_table_name in DB_table:
        #     for line in db_permissions:
        #         permission_type = str(line['Permission_type'])
        #         if f'{line['Permission_name']}'


    def _Verify_layout(self, layout_table: list, DB_table: list):
        if len(DB_table) == 0:
            for index_table, table in enumerate(layout_table):
                columns_formated = ""

                for column in layout_table[index_table]["fields"]:
                    if columns_formated != "":
                        columns_formated += ', '

                    columns_formated = columns_formated + f"{self._Format_string(str(column['name']))} {
                        'INTEGER' if column['type'] == 'number' else (
                        'BLOB' if column['type'] == 'bytes' else 'TEXT')}{
                            ' PRIMARY KEY AUTOINCREMENT' if column['name'] == 'ID' else ''}"

                self.Create_Table(self._Format_string(str(table['name'])), columns_formated)
        else:
            for json_table in layout_table:
                found = False

                for DB_table_name in DB_table:
                    if DB_table_name[0] == self._Format_string(str(json_table['name'])):
                        found = True
                        self.cursor.execute(f"PRAGMA table_info({DB_table_name[0]});")
                        DB_table_columns = self.cursor.fetchall()

                        for column_object in json_table['fields']:
                            column_found = False

                            for DB_column_name in DB_table_columns:
                                if DB_column_name[1] == self._Format_string(column_object['name']):
                                    column_found = True

                                    break

                            if column_found == False:
                                #falta adicionar uns logs
                                #print(f"Column {column_object['name']} from {json_table['name']} added")
                                self.Create_Column(
                                        self._Format_string(str(json_table['name'])),
                                        self._Format_string(str(column_object['name'])),
                                        f"{'INTEGER' if column_object['type'] == 'number' else (
                                        'BLOB' if column_object['type'] == 'bytes' else 'TEXT')}")

                        break

                if found == False:
                    #falta adicionar uns logs
                    #print(f"table {json_table['name']} not found")
                    columns_formated = ""
                    for column_object in json_table['fields']:
                        if columns_formated != "":
                            columns_formated += ', '

                        columns_formated = columns_formated + f"{self._Format_string(str(column_object['name']))} {
                            'INTEGER' if column['type'] == 'number' else (
                            'BLOB' if column['type'] == 'bytes' else 'TEXT')}{
                                ' PRIMARY KEY AUTOINCREMENT' if column['name'] == 'ID' else ''}"

                    self.Create_Table(self._Format_string(str(json_table['name'])), columns_formated)

    def _Format_string(self, word:str):
        # the replace() function evitate command SQL inside the string
        return word.replace(" ", "_").replace("-", "_").replace("/", "_").replace("*", "_"
                        ).replace(")", "_").replace("(", "_").replace("\n", "_")

    def Read(self, table: str, column: str, filter: str = ""):
        try:
            self.cursor.execute(f'select {column} from {table}{filter};')
            items = []
            for row in self.cursor.fetchall():
                items.append(row)
            return items
        except Exception as err:
            print("Error Read")
            print(err)

    def Update(self, table: str, value: str, filter: str = ""):
        try:
            self.cursor.execute(f"UPDATE {table} SET {value}{filter};")
            self.Commit()
        except Exception as err:
            print("Update error")
            print(err)

    def Create_item(self, table:str, column:str, value:str, filter: str = ""):
        """exemple: INSERT INTO "Table1" (x, y, z, ...) VALUES ('a', 2, 'b', ...)"""
        try:
            self.cursor.execute(f"INSERT INTO {table} {column} VALUES {value}{filter};")
            self.Commit()
        except Exception as err:
            print(table, column, value)
            print("Create error")
            print(err)

    def Create_Table(self, table_name:str, columns:str):
        """exemple: CREATE TABLE "Table1" (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, ...)"""
        try:
            self.cursor.execute(f"CREATE TABLE '{table_name}' ({columns});")
            self.Commit()
        except Exception as err:
            print("Create table error")
            print(err)

    def Create_Column(self, table_name:str, column_name:str, type_column:str):
        try:
            """exemple: ALTER TABLE nome_da_tabela ADD COLUMN nome_da_coluna TIPO [options];"""
            self.cursor.execute(f"ALTER TABLE '{table_name}' ADD COLUMN {column_name} {type_column};")
            self.Commit()
        except Exception as err:
            print("Create table error")
            print(err)

    def Delete(self, data):
        try:
            pass
        except Exception as err:
            print(err)

    def Commit(self):
        try:
            self.conn.commit()
        except Exception as err:
            print(err)
