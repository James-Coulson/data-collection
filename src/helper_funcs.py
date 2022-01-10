"""
General functions used by various programs
"""

from csv import writer
from os.path import isfile
from pandas import DataFrame


def append_list_as_row(file_name, list_of_elem):
    """
    Appends row to the end of csv file.

    :param file_name: The path of the file
    :param list_of_elem: The row to be appended in the form of a list
    """
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def create_csv_file(filepath, headers: list = None):
    """
    Checks if a file exists and creates the file if it does not.

    :param filepath: The path of the file
    :param headers: The headers of the csv
    """
    # Check if csv file exists
    if isfile(filepath):
        return

    # Make and save csv file
    DataFrame(columns=headers).to_csv(path_or_buf=filepath)
