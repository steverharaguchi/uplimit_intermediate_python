import os
import math
import sys
import matplotlib.pyplot as plt


def get_file_name(file_path):
    if not isinstance(file_path, str):
        return None

    # file name with extension
    file_name_ext = os.path.basename(file_path)

    # file name without extension
    file_name = os.path.splitext(file_name_ext)[0]

    return file_name


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def human_readable(number):
    units = ['', ' Thousand', ' Million', ' Billion', ' Trillion']

    n = float(number)
    millidx = max(0 , min(len(units)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), units[millidx])


def plot_sales_data(yearly_revenue, year, plot_save_path):

    yearly_revenue = [(country, revenue) for country, revenue in yearly_revenue.items()]
    countries = [str(country) for country, _ in yearly_revenue]
    revenue = [int(revenue) for _, revenue in yearly_revenue]

    plt.bar(countries, revenue, align='edge', width=0.5)
    plt.title(f'Revenue Per Country {year}', fontsize=14)
    plt.xlabel('Country', fontsize=14)
    plt.ylabel('Revenue (Dollars)', fontsize=14)

    plt.savefig(plot_save_path, bbox_inches='tight')

    plt.close()


