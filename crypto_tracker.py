#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import csv
from prettytable import PrettyTable

def print_banner():
    banner = """
    Cryptocurrency Price Tracker
    Created By : Python 2.7
    """
    print(banner)

def fetch_crypto_price(crypto):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto, "vs_currencies": "usd", "include_24hr_change": "true"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if crypto in data:
            return data[crypto]["usd"], data[crypto].get("usd_24h_change", 0)
        else:
            return None, None
    else:
        return None, None

def log_data(crypto, price):
    with open("%s_price_log.csv" % crypto, mode="a") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S "), price])

def display_data(crypto, price, change):
    table = PrettyTable()
    table.field_names = ["Cryptocurrency", "Price (USD)", "24H Change (%)"]
    table.add_row([crypto.capitalize(), "${:.2f}".format(price), "{:.2f}%".format(change)])
    print(table)

def get_valid_crypto():
    while True:
        crypto = raw_input("Enter the cryptocurrency name (e.g., bitcoin, ethereum): ").lower()
        print("Fetching data...\n")
        price, change = fetch_crypto_price(crypto)
        if price is not None:
            return crypto, price, change
        else:
            print("Error fetching data. Please check the cryptocurrency name and try again.\n")

def main():
    print_banner()
    crypto, price, change = get_valid_crypto()

    while True:
        price, change = fetch_crypto_price(crypto)
        if price is not None:
            display_data(crypto, price, change)
            log_data(crypto, price)
        else:
            print("Error fetching data. Please check the cryptocurrency name.")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
