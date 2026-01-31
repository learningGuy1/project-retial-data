import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    '''Cleaning the retail transaction dataset. Returns a cleaned copy of the input dataframe '''
    df = df.copy()

    #1   Parse dates
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"],errors="coerce")
    
    #2 remove exact duplicates

    df = df.drop_duplicates()

    #3 handling missing values
    # Description: small missing values so filled with unknown
    df["Description"] = df["Description"].fillna("Unknown").astype(str)

    #Customerid : keep transactions and label them unknown
    df["CustomerID"] = df["CustomerID"].fillna("unknown").astype(str)
    #4Create a new useful field for returned products
    df["is_returned"] = df["Quantity"] < 0

    #5 Fixing impossible values
    # UnitPrice shouldn't be negative in normal sales data
    df=df[df["UnitPrice"] > 0]

    #Quantity = 0 is meaningless
    df=df[df["Quantity"] != 0]

    #6 Outliers handling (clip using quantiles)
    # Keep product returns, but clip clip extreme values to reduce noise
    q_low_qty, q_high_qty = df["Quantity"].quantile([0.0009,0.99])    
    q_low_price, q_high_price = df["UnitPrice"].quantile([0.08,0.995])    

    df["Quantity"]=df["Quantity"].clip(q_low_qty,q_high_qty)
    df["UnitPrice"]=df["UnitPrice"].clip(q_low_price,q_high_price)

    #Final datatypes
    df["Country"]=df["Country"].astype("category")
    df["StockCode"] = df["StockCode"].astype(str)
    return df