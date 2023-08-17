import json  # used for reading JSON files
import random # used for generating random values
from tqdm import tqdm # used for showing progress bars

from global_utils import make_dir, human_readable # custom functions 
from datetime import timedelta, datetime # handling dates
import os  # handling file paths
import inspect # get information about the current stack
import constants # contains constant values used throughout the code
import argparse # handling command line arguments

import uuid # generating unique identifiers

# gets the current directory of the file where this code is running.
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# sets the seed value for the random number generator, 
# which ensures that the same sequence of random values will 
# be generated every time the code is run with the same seed value.
random.seed(42)

# defines a class DataGenerator which initializes the _seed_data attribute 
# to None and calls the read_seed_data method.
class DataGenerator:
    def __init__(self):
        self._seed_data = None
        self.read_seed_data()

    
    # defines a static method can_typecast_to_float which attempts to cast 
    # the input value val to a float type. If successful, it returns 
    # the float value, otherwise it returns None.
    @staticmethod
    def can_typecast_to_float(val):
        try:
            return float(val)
        except:
            return None

    # defines a static method random_date which takes two date objects 
    # start and end and returns a random datetime between them. 
    # The number of seconds between start and end is calculated and 
    # a random value within that range is generated. This random value is used 
    # to calculate a datetime relative to start using the timedelta function.
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

    # reads seed data from a JSON file and processes it. 
    # It uses the json module to read the contents of the JSON file into 
    # a Python object, and then it processes each item in the object, 
    # filtering out items with invalid data. 
    # The seed data is stored in the _seed_data attribute.
    def read_seed_data(self):
        with open(os.path.join(CURRENT_FOLDER, constants.DATA_FOLDER_NAME,
                               constants.SEED_FOLDER_NAME, constants.SEED_FILE_NAME)) as f:
            items = json.loads(f.read())

        modified_items = []
        # input json file with key as 'stock_no', value as 'seed_data'
        for stock_no, seed_data in items.items():
            # 'seed_data' is a dictionary with only two keys: 'description' and 'unit_price'
            # we need to add more keys to the data
            
            # assign 'stock_no' to seed_data column
            seed_data[constants.SeedDataColNames.STOCK_NO] = stock_no
            
            # check some filter conditions before adding to 'modified_items'
            if all(
                    [  # check if 'description' column in seed_data is a string
                        (isinstance(seed_data[constants.SeedDataColNames.DESCRIPTION], str) and
                       # check if 'description' column in seed_data is a non-empty string
                    len(seed_data[constants.SeedDataColNames.DESCRIPTION]) > 0),
                       # check if 'unit_price' column in seed_data can be converted to float, and is larger than 0 
                    (self.can_typecast_to_float(seed_data[constants.SeedDataColNames.UNIT_PRICE]) and
                     float(seed_data[constants.SeedDataColNames.UNIT_PRICE]) > 0)
                    ]
                ):
                modified_items.append(seed_data)

        self._seed_data = modified_items

    # this method generates a single row of synthetic sales data based on 
    # the seed data. It randomly selects a row of seed data from _seed_data 
    # and generates random values for the units, country, invoice_no, and 
    # date fields. The total field is calculated based on the unit_price 
    # and units fields.
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

"""
generates a CSV file containing synthetic sales data. 

It takes:
    (1) a data_gen_obj parameter, which is an instance of the DataGenerator class, 
    (2) a file_details parameter, which contains details about the file to be generated, 
        including the number of datapoints to generate, the file name, and the start and end dates. 

The function first creates the output directory if it doesn't exist, 
and then creates the CSV file with the appropriate header. 

It then generates a number of datapoints, writing each row to the CSV file 
and updating the total_units and total_price variables. 

Finally, it prints out the total number of units and the total price.
"""
def generate_file(data_gen_obj, file_details):
    total_units = 0
    total_price = 0

    file_path = os.path.join(
        CURRENT_FOLDER, 
        constants.DATA_FOLDER_NAME, 
        file_details['folder_name'],
        file_details['file_name'])
    
    make_dir(directory=os.path.join(
            CURRENT_FOLDER, 
            constants.DATA_FOLDER_NAME, 
            file_details['folder_name'])
        )
    
    print("########################################################################")
    print("the file_path is:")
    print(file_path)    

    # The function then opens the output file in write mode and writes the header row. 
    # The header row contains the names of the columns that will be in the output file.
    with open(file_path, 'w') as f:
        f.write(",".join([constants.OutDataColNames.STOCK_CODE, constants.OutDataColNames.DESCRIPTION,
                          constants.OutDataColNames.UNIT_PRICE, constants.OutDataColNames.QUANTITY,
                          constants.OutDataColNames.TOTAL_PRICE, constants.OutDataColNames.COUNTRY,
                          constants.OutDataColNames.INVOICE_NO, constants.OutDataColNames.DATE]))
        f.write("\n")

    
    with open(file_path, 'a') as f:
        # 'tqdm': A progress bar is printed to the console to show that 
        # the function is currently running
        
        # A loop is then run to generate the required number of data points. 
        # The generate_data() method of the data_gen_obj instance is called to 
        # generate a single data point, and the details are written to the output file. 
        # The total_units and total_price variables are updated with the new values.
        for n_row in tqdm(range(file_details['n_datapoints'])):
            row = data_gen_obj.generate_data(start_date=file_details['start_date'],
                                             end_date=file_details['end_date'])
            f.write(",".join([str(row[constants.SeedDataColNames.STOCK_NO]),
                              str(row[constants.SeedDataColNames.DESCRIPTION]).replace(',', ''),
                              str(row[constants.SeedDataColNames.UNIT_PRICE]),
                              str(row[constants.SeedDataColNames.UNITS]),
                              str(row[constants.SeedDataColNames.TOTAL]), 
                              str(row[constants.SeedDataColNames.COUNTRY]),
                              str(row[constants.SeedDataColNames.INVOICE_NO]),
                              str(row[constants.SeedDataColNames.DATE])]))

            total_units += row[constants.SeedDataColNames.UNITS]
            total_price += row[constants.SeedDataColNames.TOTAL]

            # After every 10,000 rows, the function prints the total number of units 
            # and the total price processed so far. 
            if n_row % 10000 == 0:
                tqdm.write(f"Total units : {human_readable(int(total_units))}, "
                           f"Total price : ${human_readable(int(total_price))}")

            f.write("\n")

    # Once all the data points have been generated, the function prints 
    # the total number of units and the total price for the file.
    tqdm.write(f"File Name : {file_details['file_name']}, Total units : {int(total_units)}, "
               f"Total price : ${int(total_price)}")


"""
The tst(), sml(), and bg() functions generate output files with different numbers of data points. 
tst() function generates files with 60,000 to 90,000 data points, 
sml() generates files with 600,000 to 900,000 data points
bg() generates files with 10,000,000 to 25,000,000 data points.
"""
def tst():
    # create an instance of the DataGenerator class
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
        'n_datapoints': 10000000,
        'file_name': '2015.csv',
        'start_date': datetime.strptime(f'2015/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2015/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 12000000,
        'file_name': '2016.csv',
        'start_date': datetime.strptime(f'2016/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2016/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 15000000,
        'file_name': '2017.csv',
        'start_date': datetime.strptime(f'2017/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2017/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 16000000,
        'file_name': '2018.csv',
        'start_date': datetime.strptime(f'2018/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2018/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 19000000,
        'file_name': '2019.csv',
        'start_date': datetime.strptime(f'2019/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2019/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 21000000,
        'file_name': '2020.csv',
        'start_date': datetime.strptime(f'2020/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2020/12/31', constants.DATE_FORMAT),
    }, {
        'folder_name': inspect.stack()[0][3],
        'n_datapoints': 25000000,
        'file_name': '2021.csv',
        'start_date': datetime.strptime(f'2021/1/1', constants.DATE_FORMAT),
        'end_date': datetime.strptime(f'2021/12/31', constants.DATE_FORMAT),
    }]

    for file_to_generate in files_to_generate:
        generate_file(data_gen_obj=data_gen, file_details=file_to_generate)

"""
generates different types of data 
depending on a command-line argument passed to it
"""
# This line checks whether the script is being run as the main program. 
# This is a common pattern in Python to allow the script to be used as 
# both a standalone program and as a module that can be imported by other scripts.
if __name__ == '__main__':
    # This line creates an ArgumentParser object from the argparse module, 
    # which provides an easy way to define and handle command-line arguments. 
    # The description argument sets the description that will be displayed when 
    # the script is run with the --help flag.
    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    # This line adds a command-line argument --type to the ArgumentParser object, 
    # with a default value of tst. The choices argument restricts the possible 
    # values of this argument to 'tst', 'sml', or 'bg'. The help argument sets 
    # the help text that will be displayed when the script is run with the --help flag.
    parser.add_argument('--type',
                        default='tst',
                        choices=['tst', 'sml', 'bg'],
                        help='Type of data to generate')
    args = parser.parse_args()

    # This block of code checks the value of the args.type variable, 
    # which was set by the command-line argument. 
    if args.type == 'tst':
        tqdm.write("Generating `test` data")
        tst()

    elif args.type == 'sml':
        tqdm.write("Generating `small` data")
        sml()

    elif args.type == 'bg':
        tqdm.write("Generating `big` data")
        bg()
