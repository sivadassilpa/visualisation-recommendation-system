import pandas as pd
from enum import Enum


# Define the enum class for type categories
class DataTypeCategory(Enum):
    NUMBERS = "numbers"
    CATEGORIES = "categories"
    DATES = "dates"
    BOOLEAN = "boolean"
    UNKNOWN = "unknown"
    WORDS = "words"


# Define a mapping of specific data types to general categories using the enum
type_mapping = {
    DataTypeCategory.NUMBERS: ["int64", "float64"],
    DataTypeCategory.CATEGORIES: ["object"],
    DataTypeCategory.DATES: ["datetime64[ns]"],
    DataTypeCategory.BOOLEAN: ["bool"],
    DataTypeCategory.WORDS: ["words"],
    DataTypeCategory.UNKNOWN: [],
}

heatmapColorOptions = [
    "Turbo",
    "Viridis",
    "Magma",
    "Inferno",
    "Plasma",
    "Cividis",
    "DarkBlue",
    "DarkGold",
    "DarkGreen",
    "DarkMulti",
    "DarkRed",
    "LightGreyRed",
    "LightGreyTeal",
    "LightMulti",
    "LightOrange",
    "LightTealBlue",
    "Blues",
    "Browns",
    "Greens",
    "Greys",
    "Oranges",
    "Purples",
    "Reds",
    "TealBlues",
    "Teals",
    "WarmGreys",
    "BlueOrange",
    "BrownBlueGreen",
    "PurpleGreen",
    "PinkYellowGreen",
    "PurpleOrange",
    "RedBlue",
    "RedGrey",
    "RedYellowBlue",
    "RedYellowGreen",
    "BlueGreen",
    "BluePurple",
    "GoldGreen",
    "GoldOrange",
    "GoldRed",
    "GreenBlue",
    "OrangeRed",
    "PurpleBlueGreen",
    "PurpleBlue",
    "PurpleRed",
    "RedPurple",
    "YellowGreenBlue",
    "YellowGreen",
    "YellowOrangeBrown",
    "YellowOrangeRed",
]
