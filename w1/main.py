import constants
from w1.data_processor import DataProcessor
from pprint import pprint
from typing import Dict
from tqdm import tqdm
import os
import argparse
from global_utils import get_file_name, make_dir, plot_sales_data
from datetime import datetime
import json
import logging

CURRENT_FOLDER_NAME = os.path.dirname(os.path.abspath(__file__))

"""
The revenue_per_region function takes an instance of the DataProcessor class 
as input, reads the data using the data_reader method of DataProcessor, 
and calculates the aggregate revenue per region. It returns a dictionary 
with the aggregate revenue per region.
"""
def revenue_per_region(dp: DataProcessor) -> Dict:
    """
    Input : object of instance type Class DataProcessor
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

    data_reader = dp.data_reader
    data_reader_gen = (row for row in data_reader)

    # skip first row as it is the column name
    _ = next(data_reader_gen)

    aggregate = dict()

    for row in tqdm(data_reader_gen):
        if row[constants.OutDataColNames.COUNTRY] not in aggregate:
            aggregate[row[constants.OutDataColNames.COUNTRY]] = 0
        aggregate[row[constants.OutDataColNames.COUNTRY]] += dp.to_float(row[constants.OutDataColNames.TOTAL_PRICE])

    return aggregate


def get_sales_information(file_path: str) -> Dict:
    # Initialize
    dp = DataProcessor(file_path=file_path)

    # print stats
    dp.describe(column_names=[constants.OutDataColNames.UNIT_PRICE, constants.OutDataColNames.TOTAL_PRICE])

    # return total revenue and revenue per region
    print("########################################################")
    print("This is the output of get_sales_information:")
    print({
        'total_revenue': dp.aggregate(column_name=constants.OutDataColNames.TOTAL_PRICE),
        'revenue_per_region': revenue_per_region(dp),
        'file_name': get_file_name(file_path)
    })
    print("########################################################")
    
    return {
        'total_revenue': dp.aggregate(column_name=constants.OutDataColNames.TOTAL_PRICE),
        'revenue_per_region': revenue_per_region(dp),
        'file_name': get_file_name(file_path)
    }


"""
The main function parses the command-line arguments using argparse, gets the 
list of files in the data directory specified by the argument, calls the 
get_sales_information function on each file, and saves the output as a JSON file 
in the output directory. It also calls the plot_sales_data function to plot 
the revenue per region for each file and save the plot as a PNG file in the output directory.
"""
def main():
    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    parser.add_argument('--type',
                        default='tst',
                        choices=['tst', 'sml', 'bg'],
                        help='Type of data to generate')
    args = parser.parse_args()

    data_folder_path = os.path.join(CURRENT_FOLDER_NAME, '..', constants.DATA_FOLDER_NAME, args.type)
    # list comprehension to get all the csv files in the path
    files = [str(file) for file in os.listdir(data_folder_path) if str(file).endswith('csv')]

    output_save_folder = os.path.join(CURRENT_FOLDER_NAME, '..', 'output', args.type,
                                      datetime.now().strftime("%B %d %Y %H-%M-%S"))
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
