import datetime
from typing import List, Dict
from pprint import pprint
from w1.utils import Stats
from tqdm import tqdm
import os
from w2.utils.database import DB
import uuid
import inspect
from w1.data_processor import DataProcessor
import argparse
from global_utils import make_dir,  plot_sales_data, get_file_name
import json
import constants

CURRENT_FOLDER_NAME = os.path.dirname(os.path.abspath(__file__))


class DP(DataProcessor):
    def __init__(self, file_path):
        super().__init__(file_path)
        self._db = DB()

    def get_db(self) -> DB:
        return self._db

    def get_file_path(self) -> str:
        return self._fp

    def get_file_name(self) -> str:
        return self._file_name

    def get_n_rows(self) -> int:
        return self._n_rows

    def aggregate(self, column_name: str) -> float:
        """
        Input : List[str]
        Output : Dict

        This method should use the generator function (`file_reader`) created above and return aggregate
        of the column mentioned in the `column_name` variable

        For example if the `column_name` -> 'TotalPrice' and the file format is as below:

        StockCode    , Description    , UnitPrice  , Quantity, TotalPrice , Country
        22180        , RETROSPOT LAMP , 19.96      , 4       , 79.84      , Russia
        23017        , APOTHECARY JAR , 24.96      , 1       , 24.96      , Germany
        84732D       , IVORY CLOCK    , 0.39       , 2       , 0.78       ,India

        aggregate should be 105.58
        """
        process_id = str(uuid.uuid4())
        self._db.insert(process_id, start_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        file_name=self._file_name, file_path=self._fp, description=inspect.stack()[0][3])

        # get generator from data_reader
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name
        _ = next(data_reader_gen)

        aggregate = 0

        for row_num, row in enumerate(tqdm(data_reader_gen)):
            if isinstance(self._n_rows, int) and isinstance(row_num, int) and row_num % 10000 == 0:
                self._db.update_percentage(process_id=process_id, percentage=100 * row_num/self._n_rows)

            if self.to_float(row[column_name]):
                aggregate += self.to_float(row[column_name])

        self._db.update_percentage(process_id=process_id, percentage=100)
        self._db.update_end_time(process_id=process_id, end_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        return aggregate

    def describe(self, column_names: List[str]):
        # get generator from data_reader
        data_reader_gen = (row for row in self.data_reader)

        # skip first row as it is the column name
        _ = next(data_reader_gen)

        stats = {name: Stats() for name in column_names}

        process_id = str(uuid.uuid4())
        self._db.insert(process_id, start_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        file_name=self._file_name, file_path=self._fp, description=inspect.stack()[0][3])

        for row_num, row in enumerate(tqdm(data_reader_gen)):
            if isinstance(self._n_rows, int) and isinstance(row_num, int) and row_num % 10000 == 0:
                self._db.update_percentage(process_id=process_id, percentage=100 * row_num/self._n_rows)

            for column_name in column_names:
                stats[column_name].update_stats(val=row[column_name])

        self._stats = stats
        for column_name, value in self._stats.items():
            pprint(column_name)
            pprint(value.get_stats())

        self._db.update_percentage(process_id=process_id, percentage=100)
        self._db.update_end_time(process_id=process_id, end_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))


def revenue_per_region(dp: DP) -> Dict:
    """
    Input : object of instance type Class Koala
    Output : Dict

    The method should find the aggregate revenue per region

    For example if the file format is as below:

    StockCode    , Description    , UnitPrice  , Quantity, TotalPrice , Country
    22180        , RETROSPOT LAMP , 19.96      , 4       , 79.84      , Russia
    23017        , APOTHECARY JAR , 24.96      , 1       , 24.96      , Germany
    84732D       , IVORY CLOCK    , 0.39       , 2       , 0.78       ,India
    ...
    ...
    ...

    expected output format is:
    {
        'China': 1.66,
        'France': 17.14,
        'Germany': 53.699999999999996,
        'India': 55.78,
        'Italy': 90.45,
        'Japan': 76.10000000000001,
        'Russia': 87.31,
        'United Kingdom': 29.05,
        'United States': 121.499
    }
    """
    # get generator from data_reader
    data_reader_gen = (row for row in dp.data_reader)

    # skip first row as it is the column name
    _ = next(data_reader_gen)

    aggregate = dict()

    process_id = str(uuid.uuid4())
    dp.get_db().insert(process_id=process_id, start_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                       file_name=dp.get_file_name(), file_path=dp.get_file_path(), description=inspect.stack()[0][3])

    for n_row, row in enumerate(tqdm(data_reader_gen)):
        if isinstance(dp.get_n_rows(), int) and isinstance(n_row, int) and n_row % 10000 == 0:
            dp.get_db().update_percentage(process_id=process_id, percentage=100 * n_row / dp.get_n_rows())

        if row[constants.OutDataColNames.COUNTRY] not in aggregate:
            aggregate[row[constants.OutDataColNames.COUNTRY]] = 0
        aggregate[row[constants.OutDataColNames.COUNTRY]] += dp.to_float(row[constants.OutDataColNames.TOTAL_PRICE])

    dp.get_db().update_percentage(process_id=process_id, percentage=100)
    dp.get_db().update_end_time(process_id=process_id, end_time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    return aggregate


def get_sales_information(file_path: str) -> Dict:
    # Initialize
    dp = DP(file_path=file_path)

    # print stats
    dp.describe(column_names=[constants.OutDataColNames.UNIT_PRICE, constants.OutDataColNames.TOTAL_PRICE])

    # return total revenue and revenue per region
    return {
        'total_revenue': dp.aggregate(column_name=constants.OutDataColNames.TOTAL_PRICE),
        'revenue_per_region': revenue_per_region(dp),
        'file_name': get_file_name(file_path)
    }


def main():
    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    parser.add_argument('--type',
                        default='tst',
                        choices=['tst', 'sml', 'bg'],
                        help='Type of data to generate')
    args = parser.parse_args()

    data_folder_path = os.path.join(CURRENT_FOLDER_NAME, '..', constants.DATA_FOLDER_NAME, args.type)
    files = [str(file) for file in os.listdir(data_folder_path) if str(file).endswith('csv')]

    output_save_folder = os.path.join(CURRENT_FOLDER_NAME, '..', 'output', args.type,
                                      datetime.datetime.now().strftime("%B %d %Y %H-%M-%S"))
    make_dir(output_save_folder)

    file_paths = [os.path.join(data_folder_path, file_name) for file_name in files]
    revenue_data = [get_sales_information(file_path)
                    for file_path in file_paths]

    pprint(revenue_data)

    for yearly_data in revenue_data:
        with open(os.path.join(output_save_folder, f'{yearly_data["file_name"]}.json'), 'w') as f:
            f.write(json.dumps(yearly_data))

        plot_sales_data(yearly_revenue=yearly_data['revenue_per_region'], year=yearly_data["file_name"],
                        plot_save_path=os.path.join(output_save_folder, f'{yearly_data["file_name"]}.png'))


if __name__ == '__main__':
    main()
