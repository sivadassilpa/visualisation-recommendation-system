from flask import jsonify
import pandas as pd
import numpy as np


def profile_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Get dataset shape

    df = identify_data_type(df)
    df = df.infer_objects()
    shape = df.shape
    # Get data types
    data_types = df.dtypes.apply(lambda x: str(x)).to_dict()

    # Get summary statistics
    summary_stats = df.describe(include="all").to_dict()

    # Get number of missing values
    missing_values = df.isnull().sum().to_dict()

    # Unique values for categorical data
    unique_values = df.select_dtypes(include=["object"]).nunique().to_dict()
    categorical_vars = identify_categorical_variables(df)
    profile = {
        "shape": shape,
        "data_types": data_types,
        "summary_stats": summary_stats,
        "missing_values": missing_values,
        "unique_values": unique_values,
        "categorical_vars": categorical_vars,
    }

    return profile


def identify_data_type(df):
    for column in df.columns:
        if df[column].dtype == "object":
            # Try to convert the column to datetime
            try:
                df[column] = pd.to_datetime(df[column])
                print(f"{column} was converted to datetime.")
            except ValueError:
                # If the column wasn't converted to datetime, check if it's numeric
                if df[column].dtype == "object":
                    try:
                        df[column] = pd.to_numeric(df[column])
                        print(f"{column} was converted to numeric.")
                    except ValueError:
                        print(f"{column} is a non-numeric object.")

    return df


def identify_categorical_variables(df):
    categorical_vars = {}
    for column in df.columns:
        if df[column].dtype == "object":
            unique_values = df[column].value_counts()
            if (
                len(unique_values) >= 2 and len(unique_values) < 5
            ):  # Adjust the threshold as needed
                categorical_vars[column] = unique_values.to_dict()
    return categorical_vars


# # Example usage:
# profile = profile_data()
# print(profile)
