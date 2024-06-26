from flask import jsonify
import pandas as pd
import numpy as np
from backend.factories.visualization_factory import ChartFactory


def profile_data(file_path):
    df = pd.read_csv(file_path)
    df = identify_data_type(df)
    df = df.infer_objects()
    shape = df.shape
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

            except ValueError:
                # If the column wasn't converted to datetime, check if it's numeric
                if df[column].dtype == "object":
                    try:
                        df[column] = pd.to_numeric(df[column])

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


def extract_profile(profile, selected_columns):
    # Initialize the new profile dictionary with filtered values
    new_profile = {
        "shape": (profile["shape"][0], len(selected_columns)),
        "data_types": {col: profile["data_types"][col] for col in selected_columns},
        "summary_stats": {
            col: profile["summary_stats"][col] for col in selected_columns
        },
        "missing_values": {
            col: profile["missing_values"][col] for col in selected_columns
        },
        "unique_values": {
            col: profile["unique_values"][col]
            for col in selected_columns
            if col in profile["unique_values"]
        },
        "categorical_vars": {
            col: profile["categorical_vars"][col]
            for col in selected_columns
            if col in profile["categorical_vars"]
        },
    }
    for column in new_profile["categorical_vars"]:
        new_profile["data_types"][column] = "bool"
    return new_profile


def create_vega_chart(chart_type, selectedData, selectedColumns):
    chart_ontology = ChartFactory.get_chart_ontology(
        chart_type, selectedData, selectedColumns
    )
    vega_spec = chart_ontology.define()
    return vega_spec


def dataForSelectedColumns(file_path, selectedColumns):
    df = pd.read_csv(file_path)
    column_keys = [list(col_dict.keys())[0] for col_dict in selectedColumns]
    return df[column_keys]
