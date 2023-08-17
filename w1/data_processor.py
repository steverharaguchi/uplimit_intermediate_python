from typing import List
from pprint import pprint
from w1.utils import Stats, DataReader
from tqdm import tqdm
import os

"""
This is a class definition of `DataProcessor`. 
The class takes a file path as input when initializing an object of this class. 
The object then reads data from the file using a `DataReader` object and 
stores the column names and separator used in the file. 
The class also contains two methods, `describe` and `aggregate`.

The `describe` method takes a list of column names as input and calculates 
summary statistics (mean, standard deviation, minimum, maximum) for each of 
these columns in the file. The method uses a generator to iterate through the 
file row by row, skipping the first row (column names). For each row, it updates 
the summary statistics for each column specified in the input list. 
The summary statistics are stored in a `Stats` object for each column, 
which is then stored in a dictionary with the column name as the key.

The `aggregate` method takes a column name as input and calculates the sum of 
all values in that column in the file. The method also uses a generator to 
iterate through the file row by row, skipping the first row (column names). 
For each row, it adds the value in the specified column to a running total. 
The final total is returned as output.

The code is incomplete as the implementation of the `aggregate` method is missing.

"""
class DataProcessor:
    def __init__(self, file_path: str) -> None:
        self._fp = file_path
        self._col_names = []
        self._sep = ","
        self._stats = None
        self._file_name = os.path.basename(file_path)
        self._n_rows = 0

        self._set_col_names()
        self.data_reader = DataReader(fp=file_path, sep=self._sep, col_names=self._col_names)
        self._set_n_rows()

    @staticmethod
    def to_float(val):
        try:
            return float(val)
        except:
            return None

    def _set_n_rows(self) -> None:
        # get generator from data_reader
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name
        _ = next(data_reader_gen)

        for _ in tqdm(data_reader_gen):
            self._n_rows += 1

    def _set_col_names(self) -> None:
        with open(self._fp) as f:
            first_row = f.readline().strip('\n')

        col_names = first_row.split(self._sep)
        self._col_names = col_names

    """
    The describe method takes a list of column names as input and calculates 
    summary statistics (mean, standard deviation, minimum, maximum) for each 
    of these columns in the file. The method uses a generator to iterate through 
    the file row by row, skipping the first row (column names). For each row, 
    it updates the summary statistics for each column specified in the input list. 
    The summary statistics are stored in a Stats object for each column, which is 
    then stored in a dictionary with the column name as the key.
    """
    def describe(self, column_names: List[str]):
        # get generator from data_reader --- generator comprehension
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name
        _ = next(data_reader_gen)

        
        # This line of code creates a dictionary called stats where the keys are 
        # the column names provided in the column_names list, and the values are 
        # instances of the Stats class.

        # Specifically, it uses a dictionary comprehension to create the dictionary. 
        # For each column name in column_names, it creates a key-value pair where 
        # the key is the column name and the value is an instance of the Stats class 
        # created by calling the class constructor Stats().
        
        # In summary, this line of code initializes a dictionary where the keys are 
        # the column names and the values are empty Stats objects. These Stats objects 
        # will later be updated with statistical information for each column using 
        # the update_stats method.
        stats = {name: Stats() for name in column_names}

        # update stats as we iterate through the file
        for row in tqdm(data_reader_gen):
            for column_name in column_names:
                stats[column_name].update_stats(val=row[column_name])

        self._stats = stats
        for column_name, value in self._stats.items():
            pprint(column_name)
            pprint(value.get_stats())

    """
    The aggregate method takes a column name as input and calculates the sum 
    of all values in that column in the file. The method also uses a generator 
    to iterate through the file row by row, skipping the first row (column names). 
    For each row, it adds the value in the specified column to a running total. 
    The final total is returned as output.

    """
    def aggregate(self, column_name: str) -> float:
        """
        Input : List[str]
        Output : Dict

        This method should use the generator method assigned to seld.data_reader and return aggregate
        of the column mentioned in the `column_name` variable

        For example if the `column_name` -> 'TotalPrice' and the file format is as below:

        StockCode    , Description    , UnitPrice  , Quantity, TotalPrice , Country
        22180        , RETROSPOT LAMP , 19.96      , 4       , 79.84      , Russia
        23017        , APOTHECARY JAR , 24.96      , 1       , 24.96      , Germany
        84732D       , IVORY CLOCK    , 0.39       , 2       , 0.78       ,India

        aggregate should be 105.58
        """
        # get generator from data_reader
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name
        _ = next(data_reader_gen)

        aggregate = 0

        for row in tqdm(data_reader_gen):
            if self.to_float(row[column_name]):
                aggregate += self.to_float(row[column_name])

        return aggregate
