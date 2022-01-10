"""
Used to collect order book data from Binance cryptocurrency exchange
"""

# Internal imports
from constants import *
from helper_funcs import append_list_as_row, create_csv_file

# External imports
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import os
from datetime import date
from time import time

# Constants
depth = 10                                  # The market depth to be recorded
symbols = ['ETHBTC', 'BTCUSDT', 'ETHUSDT', 'MATICUSDT', 'BCHUSDT', 'BUSDUSDT']             # The symbols to be recorded


def handle_socket_message(data):
    """
    Placeholder method to be used for kline callback

    :param data: Data received
    """
    print("Setting up temporary kline socket")


def log_depth_cache(depth_cache):
    """
    Method used to store market date from the given depth cache

    :param depth_cache: Depth cache given
    """
    # Create new row
    row = [int(depth_cache.update_time)*1000, depth_cache.get_asks()[:depth], depth_cache.get_bids()[:depth]]

    # Get filepath for csv file
    csv_filepath = "{}/binance/orderbook/daily/{}/{}-OB-{}.csv".format(os.getcwd(), depth_cache.symbol,
                                                                       depth_cache.symbol,
                                                                       date.today().strftime("%Y-%m-%d"))

    # Create/check csv file
    create_csv_file(filepath=csv_filepath, headers=["time", "asks", "bids"])

    # Append row to the end of csv file
    append_list_as_row(csv_filepath, row)

    # Print update to console
    print("{}: updated {}".format(int(time()), csv_filepath))


if __name__ == '__main__':
    # Making directory
    cwd = os.getcwd()
    directory = "/binance/orderbook/daily/{}/"
    path = "{}/{}".format(cwd, directory)

    # Iterate through symbols making directories
    for symbol in symbols:
        try:
            os.makedirs(path.format(symbol), 0o666)
        except:
            print("{} already exists".format(path.format(symbol)))

    # Check if file exists
    current_date = date.today().strftime("%Y-%m-%d")
    for symbol in symbols:
        filepath = os.path.join(path.format(symbol), "{}-OB-{}.csv".format(symbol, current_date))
        create_csv_file(filepath=filepath, headers=["time", "asks", "bids"])

    # Creating client
    client = Client(binance_api_key, binance_api_secret)

    # Start socket manager using threads
    twm = ThreadedWebsocketManager()
    twm.start()

    # Start depth cache manager using threads
    dcm = ThreadedDepthCacheManager()
    dcm.start()

    # Starting and closing kline socket (I have no clue why but it initalizes some variable in the client)
    name = twm.start_kline_socket(callback=handle_socket_message, symbol='BNBBTC')
    twm.stop_socket(name)

    # Iterate through symbols
    for symbol in symbols:
        # Starting socket
        dcm.start_depth_cache(callback=log_depth_cache, symbol=symbol)

    # Join the threaded managers to the main thread
    twm.join()
    dcm.join()
