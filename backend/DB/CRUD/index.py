import pathlib, json
import sqlite3 as DB
from os.path import exists


class SQLite():
    def __init__(self, layout_filename:str):
        self.layout_filename = layout_filename

    def Init_main(self):
        try:
            absolute_path = str(pathlib.Path(__file__).parent.absolute())
            path = f'{absolute_path.replace('CRUD', 'db.sqlite3')}' # C:/.../BACKEND/DB/db.sqlite3
            self.conn = DB.connect(database=path)
            self.cursor = self.conn.cursor()
            DB_table = self.Read("sqlite_master", "name", " WHERE type = 'table'")
            if DB_table == None:
                DB_table = []

            with open(f'{absolute_path.replace('DB\\CRUD', '')}{self.layout_filename}', "r", encoding="utf-8") as arquivo:
                layout_table = json.load(arquivo)

            # ================
            # tables = layout_table['tables']

            # for table in tables:
            #     self.cursor.execute(f"DROP TABLE IF EXISTS '{table['name']}'")
            # ================

            # verify the layout in tables of layout.json
            self._Verify_layout(layout_table['tables'], DB_table)

            # verify the names of columns or tables

            # verify the table permissions items
            DB_table = self.Read("sqlite_master", "name", " WHERE type='table'")
            self._Verify_permissions_table(DB_table, layout_table['config'])

            # verify if the log folder exists
            if exists(f'{absolute_path.replace('DB\\CRUD', 'logs\\09-2025.log')}') == False:
                pass

            # verify the table of groups
            self._Verify_groups(layout_table['config'])

        except Exception as err:
            print(err, "\n")

    def _Verify_permissions_table(self, DB_table: list, layout_config: object):
        table_exists = False

        for DB_table_name in DB_table:
            if DB_table_name[0] == self._Format_string(layout_config['permissions_table_name']):
                table_exists = True
                break

        if table_exists == False:
            Exception("bad layout")

        db_permissions = self.Read(layout_config['permissions_table_name'], "ID, Permission_name, Permission_type, Details, ID_user_created_by")
        if db_permissions == None:
            db_permissions = []

        # verificar as permissoes
        for DB_table_name in DB_table:
            found_table = False
            found_permission_type = False

            for permission in db_permissions:
                if permission[1] == DB_table_name[0]:
                    found_table = True

                    for permissions_type in layout_config['permissions_type']:
                        if permissions_type == permission[2]:
                            found_permission_type = True

                        break

                    if found_permission_type == False:
                        self.Create_item("Permissions", "Permission_name, Permission_type, Details, ID_user_created_by", 
                                         [DB_table_name[0], permission[2], 'permissions to table', 0])

                    break

            if found_table == False:
                for permissions_type in layout_config['permissions_type']:
                    id_permission = self.Create_item("Permissions", "Permission_name, Permission_type, Details, ID_user_created_by", 
                                                     [DB_table_name[0], permissions_type, 'permissions to table', 0])

            # depois de cada loop posso retirar o item do db_permissions para diminuir o processamento

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
                                # falta adicionar uns logs
                                #print(f"Column {column_object['name']} from {json_table['name']} added")
                                self.Create_Column(
                                        self._Format_string(str(json_table['name'])),
                                        self._Format_string(str(column_object['name'])),
                                        f"{'INTEGER' if column_object['type'] == 'number' else (
                                        'BLOB' if column_object['type'] == 'bytes' else 'TEXT')}")

                        break

                if found == False:
                    # falta adicionar uns logs
                    #print(f"table {json_table['name']} not found")
                    columns_formated = ""
                    for column_object in json_table['fields']:
                        if columns_formated != "":
                            columns_formated += ', '

                        columns_formated = columns_formated + f"{self._Format_string(str(column_object['name']))} {
                            'INTEGER' if column_object['type'] == 'number' else (
                            'BLOB' if column_object['type'] == 'bytes' else 'TEXT')}{
                                ' PRIMARY KEY AUTOINCREMENT' if column_object['name'] == 'ID' else ''}"

                    self.Create_Table(self._Format_string(str(json_table['name'])), columns_formated)

    def _Verify_groups(self, layout_config: object):
        table_group_name = self._Format_string(layout_config['permissions_group_table_name'])
        groups = self.Read(table_group_name, "ID, Group_name, Group_description, ID_user_created_by")
        if groups == None:
            groups = []
        found = False

        if len(groups) > 0:
            for group in groups:
                if group[1] == layout_config['default_groups'][0]['Group_name']:
                    found = True

        if found == False:
            self.Create_item(table_group_name, "Group_name, Group_description, ID_user_created_by", 
                             [layout_config['default_groups'][0]['Group_name'], layout_config['default_groups'][0]['Group_description'], 
                              layout_config['default_groups'][0]['ID_user_created_by']])

        permissions_groups = self.Read(layout_config['permissions_meta_table_name'], 
                                       "ID, ID_permission, ID_group, Permission_type, Permission_name, ID_user_created_by", 
                                       f" WHERE ID_group = 1")

        if permissions_groups == None:
            permissions_groups = []

        permissions_table = self.Read(layout_config['permissions_table_name'], "ID, Permission_name, Permission_type, Details, ID_user_created_by")

        if permissions_table == None:
            permissions_table = []

        if len(permissions_groups) == 0:
            for permission in permissions_table:
                self.Create_item("Meta_permissions", "ID_permission, ID_group, Permission_type, Permission_name, ID_user_created_by",
                                 [permission[0], 1, permission[2], permission[1], 0])

    def _Format_string(self, word:str):
        # the replace() function evitate command SQL inside the string
        return word.replace(" ", "_").replace("-", "_").replace("/", "_").replace("*", "_").replace("?", "_").replace(")", "_").replace("(", "_").replace("\n", "_").replace("'", "_")

    def Read(self, table: str, column: str, filter: str = "") -> None | list:
        try:
            self.cursor.execute(f'select {column} from {table}{filter};')
            # self.cursor.execute("SELECT ? FROM ? ?;", (column, table, filter))
            items = []
            for row in self.cursor.fetchall():
                items.append(row)

            if items != None:
                if len(items) > 0:
                    return items

            return None
        except Exception as err:
            print('\n')
            print("Error Read")
            print(err)
            print('\n')
            return None

    def Update(self, table: str, column:list, value: list, filter: str = ""):
        """exemple: UPDATE "Table1" SET (column1 = 'a', column2 = 2, column3 = 'b', ...) WHERE ID = 1"""
        try:
            # self.cursor.execute(f"UPDATE {table} SET {value}{filter};")

            formated = tuple(value)
            placeholders = f"{column[0]} = ?"

            for i in range(len(column) - 1):
                placeholders += f", {column[i + 1]} = ?"

            self.cursor.execute(f"UPDATE {table} SET {placeholders} {filter};", formated)
            self.Commit()
        except Exception as err:
            print("Update error")
            print(err)

    def Create_item(self, table:str, column:str, value:list, filter: str = ""):
        """exemple: INSERT INTO "Table1" (x, y, z, ...) VALUES ('a', 2, 'b', ...)"""
        try:
            # self.cursor.execute(f"INSERT INTO {table} ({column}) VALUES ({value}){filter};")

            formated = tuple(value)
            placeholders = "?"

            for i in range(len(formated)-1):
                placeholders += f", ?" 

            self.cursor.execute(f"INSERT INTO {table} ({column}) VALUES ({placeholders}) {filter};", formated)

            self.Commit()
            return self.cursor.lastrowid
        except Exception as err:
            print(table, column, value)
            print("Create error")
            print(err)

    def Create_Table(self, table_name:str, columns:str):
        """exemple: CREATE TABLE "Table1" (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, ...)"""
        try:
            self.cursor.execute(f"CREATE TABLE '{table_name}' ({columns});")

            # formated = [(n,) for n in columns.split(', ')]

            # self.cursor.execute(f"CREATE TABLE '{table_name}' (?);", formated)
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

    def Delete(self, table: str, filter: str = "") -> bool:
        """exemple: DELETE FROM "Table1" WHERE ID = 1"""
        try:
            self.cursor.execute(f"DELETE FROM {table}{filter};")
            self.Commit()
            return True
        except Exception as err:
            print("Update error")
            print(err)
            return False

    def Commit(self):
        try:
            self.conn.commit()
        except Exception as err:
            print(err)

db = SQLite('layout.json')
