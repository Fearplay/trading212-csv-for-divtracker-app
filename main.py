import pandas as pd
import os

path_to_csv = input("Path to your csv file (without .csv): ")
path_to_output_csv = input("Path for your output csv file (without .csv): ")

path = f"{path_to_csv}.csv"

if os.path.exists(path):
    data_from_trading = pd.read_csv(path, usecols=["Action", "Ticker", "No. of shares", "Price / share", "Time",
                                                   "Currency (Price / share)"])
    new_columns = ["Ticker", "No. of shares", "Price / share", "Time"]

    data_to_app = data_from_trading.copy()

    data_to_app = data_to_app.reindex(columns=new_columns)
    data_to_app.drop(data_to_app.loc[data_from_trading['Currency (Price / share)'] != "USD"].index, inplace=True)
    data_to_app.columns = ["Ticker", "Quantity", "Cost Per Share", "Date"]
    data_to_app["Date"] = data_to_app["Date"].str.split(" ").str[0]
    data_to_app.loc[data_from_trading["Action"] == "Market buy", "Quantity"] = data_to_app["Quantity"]
    data_to_app.loc[data_from_trading["Action"] == "Market sell", "Quantity"] = -abs(data_to_app["Quantity"])
    data_to_app.to_csv(f"{path_to_output_csv}.csv")
else:
    print("File does not exist")
