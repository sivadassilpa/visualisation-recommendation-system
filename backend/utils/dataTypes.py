import pandas as pd
from enum import Enum


# Define the enum class for type categories
class DataTypeCategory(Enum):
    NUMBERS = "numbers"
    CATEGORIES = "categories"
    DATES = "dates"
    BOOLEAN = "boolean"
    UNKNOWN = "unknown"


# Define a mapping of specific data types to general categories using the enum
type_mapping = {
    DataTypeCategory.NUMBERS: ["int64", "float64"],
    DataTypeCategory.CATEGORIES: ["object"],
    DataTypeCategory.DATES: ["datetime64[ns]"],
    DataTypeCategory.BOOLEAN: ["bool"],
    DataTypeCategory.UNKNOWN: [],
}
