import time
from typing import List, Dict
from tqdm import tqdm
import os
import multiprocessing
from w1.data_processor import DataProcessor
import constants
from global_utils import get_file_name, make_dir, plot_sales_data
import json
import argparse
from datetime import datetime
from pprint import pprint

CURRENT_FOLDER_NAME = os.path.dirname(os.path.abspath(__file__))


class DP(DataProcessor):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def get_file_path(self) -> str:
        return self._fp

    def get_file_name(self) -> str:
        return self._file_name

    def get_n_rows(self) -> int:
        return self._n_rows


def revenue_per_region(dp: DP) -> Dict:
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
    dp = DP(file_path=file_path)

    # print stats
    dp.describe(column_names=[constants.OutDataColNames.UNIT_PRICE, constants.OutDataColNames.TOTAL_PRICE])

    # return total revenue and revenue per region
    return {
        'total_revenue': dp.aggregate(column_name=constants.OutDataColNames.TOTAL_PRICE),
        'revenue_per_region': revenue_per_region(dp),
        'file_name': get_file_name(file_path)
    }


# batches the files based on the number of processes
def batch_files(file_paths: List[str], n_processes: int) -> List[set]:
    if n_processes > len(file_paths):
        return [{item} for item in file_paths]

    n_per_batch = len(file_paths) // n_processes

    first_set_len = n_processes * n_per_batch
    first_set = file_paths[0:first_set_len]
    second_set = file_paths[first_set_len:]

    batches = [set(file_paths[i:i + n_per_batch]) for i in range(0, len(first_set), n_per_batch)]
    for ind, each_file in enumerate(second_set):
        batches[ind].add(each_file)

    return batches


# Fetch the revenue data from a file
def run(file_names: List[str], n_process: int) -> List[Dict]:
    st = time.time()

    print("Process : {}".format(n_process))
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]
    revenue_data = [get_sales_information(file_path) for file_path in file_paths]

    en = time.time()

    print(f"Batch for process-{n_process} time taken {en - st}")
    return revenue_data


def flatten(lst: List[List]) -> List:
    return [item for sublist in lst for item in sublist]


def main() -> List[Dict]:
    """
    Use the `batch_files` method to create batches of files that needs to be run in each process
    Use the `run` method to fetch revenue data for a given batch of files

    Use multiprocessing module to process batches of data in parallel
    Check `multiprocessing.Pool` and `pool.starmap` methods to help you wit the task

    At the end check the overall time taken in this code vs the time taken in W1 code


    :return: Revenue data in the below format

    [{
        'total_revenue': float,
        'revenue_per_region': {
                                'China': float,
                                'France': float,
                                'Germany': float,
                                'India': float,
                                'Italy': float,
                                'Japan': float,
                                'Russia': float,
                                'United Kingdom': float,
                                'United States': float},
        'file_name': str
    },{
        'total_revenue': float,
        'revenue_per_region': {
                                'China': float,
                                'France': float,
                                'Germany': float,
                                'India': float,
                                'Italy': float,
                                'Japan': float,
                                'Russia': float,
                                'United Kingdom': float,
                                'United States': float},
        'file_name': str
    },
    ....
    ....
    ....
    ]
    """

    st = time.time()
    n_processes = 2 # you may modify this number - check out multiprocessing.cpu_count() as well

    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    parser.add_argument('--type',
                        default='tst',
                        choices=['tst', 'sml', 'bg'],
                        help='Type of data to generate')
    args = parser.parse_args()

    data_folder_path = os.path.join(CURRENT_FOLDER_NAME, '..', constants.DATA_FOLDER_NAME, args.type)
    files = [str(file) for file in os.listdir(data_folder_path) if str(file).endswith('csv')]

    output_save_folder = os.path.join(CURRENT_FOLDER_NAME, '..', 'output', args.type,
                                      datetime.now().strftime("%B %d %Y %H-%M-%S"))
    make_dir(output_save_folder)
    file_paths = [os.path.join(data_folder_path, file_name) for file_name in files]

    batches = batch_files(file_paths=file_paths, n_processes=n_processes)

    ######################################## YOUR CODE HERE ##################################################
    with multiprocessing.Pool(processes=n_processes) as pool:
        revenue_results = pool.starmap(run, [(batch, i) for i, batch in enumerate(batches)] )
        revenue_results = flatten(revenue_results)
        pool.close()
        pool.join()


    for yearly_data in revenue_results:
        with open(os.path.join(output_save_folder, f'{yearly_data["file_name"]}.json'), 'w') as f:
            f.write(json.dumps(yearly_data))
        plot_sales_data(yearly_revenue=yearly_data['revenue_per_region'], year=yearly_data["file_name"],
                     plot_save_path=os.path.join(output_save_folder, f'{yearly_data["file_name"]}.png'))
    ######################################## YOUR CODE HERE ##################################################

    en = time.time()
    print("Overall time taken : {}".format(en-st))

    # should return revenue data
    return revenue_results


if __name__ == '__main__':
    res = main()
    pprint(res)
