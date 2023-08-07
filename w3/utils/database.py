
# import the sqlite3 package
import sqlite3
from datetime import datetime
import os
from typing import List, Dict
from global_utils import make_dir


class DB:
    def __init__(self, db_name: str = "database.sqlite") -> None:
        self._db_save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'database')
        make_dir(self._db_save_path)
        self._connection = sqlite3.connect(os.path.join(self._db_save_path, db_name),
                                           check_same_thread=False)
        self._table_name = 'processes'
        self._col_order = ['process_id', 'file_name', 'file_path', 'description', 'start_time', 'end_time', 'percentage']

        self.create_table()

    @staticmethod
    def calculate_time_taken(start_time: str, end_time: str, datetime_fmt: str) -> float:
        if isinstance(start_time, str) and isinstance(end_time, str):
            start_time = datetime.strptime(start_time, datetime_fmt)
            end_time = datetime.strptime(end_time, datetime_fmt)

            return (end_time - start_time).total_seconds()

        return 0

    def create_table(self) -> None:
        """
        Create a table if it doesn't exist with the below schema

        Table name : self._table_name
        Column names:

        - process_id : TEXT (not null)
        - file_name : TEXT (default is null)
        - description : TEXT (default is null)
        - start_time : TEXT (not null)
        - end_time : TEXT (default is null)
        - percentage : REAL (default is null)

        Read more about datatypes in Sqlite here -> https://www.sqlite.org/datatype3.html
        """
    ######################################## YOUR CODE HERE ##################################################

    ######################################## YOUR CODE HERE ##################################################

    def insert(self, process_id, start_time, file_name=None, file_path=None,
               description=None, end_time=None, percentage=None) -> None:
        """
        Insert a record into the table

        :param process_id: Assign an id to the process
        :param start_time: Start time for the process
        :param file_name: File being process
        :param file_path: Path to the file being processed
        :param description: Description of the file/process
        :param end_time: End time for the process
        :param percentage: Percentage of process completed
        :return: None
        """
    ######################################## YOUR CODE HERE ##################################################

    ######################################## YOUR CODE HERE ##################################################

    def read_all(self) -> List[Dict]:
        data = []
        cursor = self._connection.execute(f'''SELECT {",".join(self._col_order)}
                                              FROM {self._table_name}''')
        for row in cursor.fetchall():
            row_dict = {col_name: row[ind] for ind, col_name in enumerate(self._col_order)}
            time_taken = self.calculate_time_taken(start_time=row_dict['start_time'], end_time=row_dict['end_time'],
                                                   datetime_fmt='%Y-%m-%d %H:%M:%S')
            row_dict['time_taken'] = time_taken

            data.append(row_dict)

        return data

    def update_end_time(self, process_id, end_time):
        self._connection.execute(f'''UPDATE {self._table_name} SET end_time='{end_time}'
                                     WHERE process_id='{process_id}';''')

        self._connection.commit()

    def update_percentage(self, process_id, percentage):
        """
        Update percentage in a record

        :param process_id: Assign an id to the process
        :param percentage: Percentage of process completed
        :return: None
        """
    ######################################## YOUR CODE HERE ##################################################

    ######################################## YOUR CODE HERE ##################################################


