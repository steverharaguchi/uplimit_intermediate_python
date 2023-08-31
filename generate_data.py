import json
import random
from tqdm import tqdm

from global_utils import make_dir, human_readable
from datetime import timedelta, datetime
import os
import inspect
import constants
import argparse

import uuid

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
random.seed(42)


class DataGenerator:
    def __init__(self):
        self._seed_data = None
        self.read_seed_data()

    @staticmethod
    def can_typecast_to_float(val):
        try:
            return float(val)
        except:
            return None

    @staticmethod
    def random_date(start, end):
        """
        This function will return a random datetime between two dates
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def get_seed_data(self):
        return self._seed_data

    def read_seed_data(self):
        with open(os.path.join(CURRENT_FOLDER, constants.DATA_FOLDER_NAME,
                               constants.SEED_FOLDER_NAME, constants.SEED_FILE_NAME)) as f:
            items = json.loads(f.read())

        modified_items = []
        for stock_no, seed_data in items.items():
            seed_data[constants.SeedDataColNames.STOCK_NO] = stock_no
            if all([(isinstance(seed_data[constants.SeedDataColNames.DESCRIPTION], str) and
                    len(seed_data[constants.SeedDataColNames.DESCRIPTION]) > 0),
                    (self.can_typecast_to_float(seed_data[constants.SeedDataColNames.UNIT_PRICE]) and
                     float(seed_data[constants.SeedDataColNames.UNIT_PRICE]) > 0)]):
                modified_items.append(seed_data)

        self._seed_data = modified_items

    def generate_data(self, start_date, end_date):
        n_row = random.randint(0, len(self._seed_data) - 1)
        n_units = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                 [0.2, 0.2, 0.25, 0.11, 0.08, 0.07, 0.03, 0.03, 0.02, 0.01])
        country = random.choices(['United States', 'China', 'Japan', 'Germany', 'India',
                                  'United Kingdom', 'France', 'Canada', 'Russia', 'Italy'],
                                 [0.2, 0.05, 0.05, 0.1, 0.1, 0.2, 0.1, 0.1, 0.05, 0.05])
        row = self._seed_data[n_row]

        data = {
            constants.SeedDataColNames.DESCRIPTION: row[constants.SeedDataColNames.DESCRIPTION],
            constants.SeedDataColNames.UNIT_PRICE: row[constants.SeedDataColNames.UNIT_PRICE],
            constants.SeedDataColNames.UNITS: n_units[0],
            constants.SeedDataColNames.TOTAL: row[constants.SeedDataColNames.UNIT_PRICE] * n_units[0],
            constants.SeedDataColNames.STOCK_NO: row[constants.SeedDataColNames.STOCK_NO],
            constants.SeedDataColNames.COUNTRY: country[0],
            constants.SeedDataColNames.INVOICE_NO: str(uuid.uuid1()),
            constants.SeedDataColNames.DATE: self.random_date(start_date, end_date).strftime(constants.DATE_FORMAT)
        }
        return data


def generate_file(data_gen_obj, file_details):
    total_units = 0
    total_price = 0

    file_path = os.path.join(CURRENT_FOLDER, constants.DATA_FOLDER_NAME, file_details['folder_name'],
                             file_details['file_name'])
    make_dir(directory=os.path.join(CURRENT_FOLDER, constants.DATA_FOLDER_NAME, file_details['folder_name']))

    with open(file_path, 'w') as f:
        f.write(",".join([constants.OutDataColNames.STOCK_CODE, constants.OutDataColNames.DESCRIPTION,
                          constants.OutDataColNames.UNIT_PRICE, constants.OutDataColNames.QUANTITY,
                          constants.OutDataColNames.TOTAL_PRICE, constants.OutDataColNames.COUNTRY,
                          constants.OutDataColNames.INVOICE_NO, constants.OutDataColNames.DATE]))
        f.write("\n")

    with open(file_path, 'a') as f:
        for n_row in tqdm(range(file_details['n_datapoints'])):
            row = data_gen_obj.generate_data(start_date=file_details['start_date'],
                                             end_date=file_details['end_date'])
            f.write(",".join([str(row[constants.SeedDataColNames.STOCK_NO]),
                              str(row[constants.SeedDataColNames.DESCRIPTION]).replace(',', ''),
                              str(row[constants.SeedDataColNames.UNIT_PRICE]),
                              str(row[constants.SeedDataColNames.UNITS]),
                              str(row[constants.SeedDataColNames.TOTAL]), str(row[constants.SeedDataColNames.COUNTRY]),
                              str(row[constants.SeedDataColNames.INVOICE_NO]),
                              str(row[constants.SeedDataColNames.DATE])]))

            total_units += row[constants.SeedDataColNames.UNITS]
            total_price += row[constants.SeedDataColNames.TOTAL]

            if n_row % 10000 == 0:
                tqdm.write(f"Total units : {human_readable(int(total_units))}, "
                           f"Total price : ${human_readable(int(total_price))}")

            f.write("\n")

    tqdm.write(f"File Name : {file_details['file_name']}, Total units : {int(total_units)}, "
               f"Total price : ${int(total_price)}")


def tst():
    data_gen = DataGenerator()

    files_to_generate = [{
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 60000,
        'file_name': '2015.csv',
        'start_date': datetime.strptime(f'2015/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2015/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 65000,
        'file_name': '2016.csv',
        'start_date': datetime.strptime(f'2016/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2016/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 70000,
        'file_name': '2017.csv',
        'start_date': datetime.strptime(f'2017/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2017/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 75000,
        'file_name': '2018.csv',
        'start_date': datetime.strptime(f'2018/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2018/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 80000,
        'file_name': '2019.csv',
        'start_date': datetime.strptime(f'2019/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2019/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 85000,
        'file_name': '2020.csv',
        'start_date': datetime.strptime(f'2020/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2020/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 90000,
        'file_name': '2021.csv',
        'start_date': datetime.strptime(f'2021/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2021/12/31', constants.DATE_FORMAT),
    }]

    for file_to_generate in files_to_generate:
        generate_file(data_gen_obj=data_gen, file_details=file_to_generate)


def sml():
    data_gen = DataGenerator()

    files_to_generate = [{
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 600000,
        'file_name': '2015.csv',
        'start_date': datetime.strptime(f'2015/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2015/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 650000,
        'file_name': '2016.csv',
        'start_date': datetime.strptime(f'2016/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2016/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 700000,
        'file_name': '2017.csv',
        'start_date': datetime.strptime(f'2017/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2017/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 750000,
        'file_name': '2018.csv',
        'start_date': datetime.strptime(f'2018/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2018/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 800000,
        'file_name': '2019.csv',
        'start_date': datetime.strptime(f'2019/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2019/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 850000,
        'file_name': '2020.csv',
        'start_date': datetime.strptime(f'2020/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2020/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 900000,
        'file_name': '2021.csv',
        'start_date': datetime.strptime(f'2021/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2021/12/31', constants.DATE_FORMAT),
    }]

    for file_to_generate in files_to_generate:
        generate_file(data_gen_obj=data_gen, file_details=file_to_generate)


def bg():
    data_gen = DataGenerator()

    files_to_generate = [{
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 3000000,
        'file_name': '2015.csv',
        'start_date': datetime.strptime(f'2015/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2015/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 4000000,
        'file_name': '2016.csv',
        'start_date': datetime.strptime(f'2016/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2016/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 5000000,
        'file_name': '2017.csv',
        'start_date': datetime.strptime(f'2017/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2017/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 5100000,
        'file_name': '2018.csv',
        'start_date': datetime.strptime(f'2018/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2018/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 6300000,
        'file_name': '2019.csv',
        'start_date': datetime.strptime(f'2019/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2019/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 7000000,
        'file_name': '2020.csv',
        'start_date': datetime.strptime(f'2020/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2020/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 5800000,
        'file_name': '2021.csv',
        'start_date': datetime.strptime(f'2021/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2021/12/31', constants.DATE_FORMAT),
    }]

    for file_to_generate in files_to_generate:
        generate_file(data_gen_obj=data_gen, file_details=file_to_generate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    parser.add_argument('--type',
                        default='tst',
                        choices=['tst', 'sml', 'bg'],
                        help='Type of data to generate')
    args = parser.parse_args()

    if args.type == 'tst':
        tqdm.write("Generating `test` data")
        tst()

    elif args.type == 'sml':
        tqdm.write("Generating `small` data")
        sml()

    elif args.type == 'bg':
        tqdm.write("Generating `big` data")
        bg()
