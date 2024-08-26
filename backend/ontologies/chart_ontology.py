from backend.ontologies.ontology import Ontology
import pandas as pd

from backend.utils.dataTypes import DataTypeCategory, heatmapColorOptions


class BarChartOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):

        # Convert data to the required format
        values = self.convert_data_to_vega_format(self.data)
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": values,
                    },
                ],
                "axes": [
                    {"orient": "bottom", "scale": "xscale"},
                    {"orient": "left", "scale": "yscale", "title": "Count"},
                ],
                "signals": [
                    {
                        "name": "tooltip",
                        "value": {},
                        "on": [
                            {"events": "rect:mouseover", "update": "datum"},
                            {"events": "rect:mouseout", "update": "{}"},
                        ],
                    },
                ],
                "scales": [
                    {
                        "name": "xscale",
                        "type": "band",
                        "domain": {"data": "table", "field": "category"},
                        "range": "width",
                        "padding": 0.05,
                        "round": True,
                    },
                    {
                        "name": "yscale",
                        "domain": {"data": "table", "field": "value"},
                        "nice": True,
                        "range": "height",
                    },
                ],
                "marks": [
                    {
                        "type": "rect",
                        "from": {"data": "table"},
                        "encode": {
                            "enter": {
                                "x": {"scale": "xscale", "field": "category"},
                                "width": {"scale": "xscale", "band": 1},
                                "y": {"scale": "yscale", "field": "value"},
                                "y2": {"scale": "yscale", "value": 0},
                            },
                            "update": {
                                "fill": {"value": "steelblue"},
                            },
                            "hover": {
                                "fill": {"value": "red"},
                            },
                        },
                    },
                    {
                        "type": "text",
                        "encode": {
                            "enter": {
                                "align": {"value": "center"},
                                "baseline": {"value": "bottom"},
                                "fill": {"value": "#333"},
                            },
                            "update": {
                                "x": {
                                    "scale": "xscale",
                                    "signal": "tooltip.category",
                                    "band": 0.5,
                                },
                                "y": {
                                    "scale": "yscale",
                                    "signal": "tooltip.value",
                                    "offset": -2,
                                },
                                "text": {"signal": "tooltip.value"},
                                "fillOpacity": [
                                    {"test": "isNaN(tooltip.value)", "value": 0},
                                    {"value": 1},
                                ],
                            },
                        },
                    },
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self, data):
        # Assuming data is a pandas DataFrame
        # Identify the boolean column from selectedColumns
        boolean_column = next(
            (
                col
                for col_dict in self.selectedColumns
                for col, dtype in col_dict.items()
                if dtype == DataTypeCategory.CATEGORIES.value
            ),
            None,
        )
        if boolean_column is None:
            try:
                boolean_column = next(
                    (
                        col
                        for col_dict in self.selectedColumns
                        for col, dtype in col_dict.items()
                        if dtype.value == DataTypeCategory.CATEGORIES.value
                    ),
                    None,
                )
            except Exception as e:
                print(e)

            # raise ValueError("No boolean column found in selectedColumns")

        # Group by the boolean column and count occurrences of True and False
        counts = self.data.groupby(boolean_column).size().reset_index(name="value")

        # Map boolean values to string representation
        counts["category"] = counts[boolean_column].astype(str).str.lower()

        # Prepare the output in the required format
        vega_values = counts[["category", "value"]].to_dict("records")

        return vega_values


class LineChartOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):
        # Convert data to the required format
        values = self.convert_data_to_vega_format(self.data)
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": values,
                    }
                ],
                "axes": [
                    {"orient": "bottom", "scale": "xscale"},
                    {"orient": "left", "scale": "yscale"},
                ],
                "scales": [
                    {
                        "name": "x",
                        "type": "point",
                        "range": "width",
                        "domain": {"data": "table", "field": "x"},
                    },
                    {
                        "name": "y",
                        "type": "linear",
                        "range": "height",
                        "nice": True,
                        "zero": True,
                        "domain": {"data": "table", "field": "y"},
                    },
                    {
                        "name": "color",
                        "type": "ordinal",
                        "range": "category",
                        "domain": {"data": "table", "field": "c"},
                    },
                ],
                "signals": [
                    {
                        "name": "interpolate",
                        "value": "linear",
                        "bind": {
                            "input": "select",
                            "options": [
                                "basis",
                                "cardinal",
                                "catmull-rom",
                                "linear",
                                "monotone",
                                "natural",
                                "step",
                                "step-after",
                                "step-before",
                            ],
                        },
                    },
                ],
                "axes": [
                    {"orient": "bottom", "scale": "x"},
                    {"orient": "left", "scale": "y"},
                ],
                "legends": [
                    {
                        "fill": "color",
                        "title": "Category",
                        "orient": "right",
                    }
                ],
                "marks": [
                    {
                        "type": "group",
                        "from": {
                            "facet": {"name": "series", "data": "table", "groupby": "c"}
                        },
                        "marks": [
                            {
                                "type": "line",
                                "from": {"data": "series"},
                                "encode": {
                                    "enter": {
                                        "x": {"scale": "x", "field": "x"},
                                        "y": {"scale": "y", "field": "y"},
                                        "stroke": {"scale": "color", "field": "c"},
                                        "strokeWidth": {"value": 2},
                                    },
                                    "update": {
                                        "interpolate": {"signal": "interpolate"},
                                        "strokeOpacity": {"value": 1},
                                    },
                                    "hover": {"strokeOpacity": {"value": 0.5}},
                                },
                            }
                        ],
                    }
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self, data):
        """
        Convert the data to the format required by the Vega spec.
        Assumes data is a DataFrame with column names that can be used directly.
        """
        vega_values = []
        for i, row in data.iterrows():
            for col in data.columns:
                vega_values.append({"x": i, "y": row[col], "c": col})
        return vega_values

    def get_attributes(self):
        return {
            "x_axis": "Time",
            "y_axis": "Values",
            "color": "Category",
            "line_style": ["solid", "dashed", "dotted"],
        }


class PieChartOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):
        # Convert data to the required format
        values = self.convert_data_to_vega_format()
        vega_spec = self.get_common_vega_spec()
        chart_title = self.get_chart_title()

        vega_spec.update(
            {
                "$schema": "https://vega.github.io/schema/vega/v5.json",
                "description": "A basic pie chart example.",
                "title": chart_title,  # Add title to the Vega spec
                "width": 150,
                "height": 150,
                "autosize": "none",
                "signals": [
                    {
                        "name": "startAngle",
                        "value": 0,
                    },
                    {
                        "name": "endAngle",
                        "value": 6.29,
                    },
                    {
                        "name": "padAngle",
                        "value": 0,
                        "bind": {"input": "range", "min": 0, "max": 0.1},
                    },
                    {
                        "name": "innerRadius",
                        "value": 0,
                        "bind": {"input": "range", "min": 0, "max": 90, "step": 1},
                    },
                    {
                        "name": "cornerRadius",
                        "value": 0,
                        "bind": {"input": "range", "min": 0, "max": 10, "step": 0.5},
                    },
                    {"name": "sort", "value": False, "bind": {"input": "checkbox"}},
                    {
                        "name": "outerRadius",
                        "value": 100,
                    },
                ],
                "data": [
                    {
                        "name": "table",
                        "values": values,
                        "transform": [
                            {
                                "type": "pie",
                                "field": "value",
                                "startAngle": {"signal": "startAngle"},
                                "endAngle": {"signal": "endAngle"},
                                "sort": {"signal": "sort"},
                            }
                        ],
                    }
                ],
                "scales": [
                    {
                        "name": "color",
                        "type": "ordinal",
                        "domain": {"data": "table", "field": "category"},
                        "range": {"scheme": "category20"},
                    }
                ],
                "marks": [
                    {
                        "type": "arc",
                        "from": {"data": "table"},
                        "encode": {
                            "enter": {
                                "fill": {"scale": "color", "field": "category"},
                                "x": {"signal": "width / 2"},
                                "y": {"signal": "height / 2"},
                            },
                            "update": {
                                "startAngle": {"field": "startAngle"},
                                "endAngle": {"field": "endAngle"},
                                "padAngle": {"signal": "padAngle"},
                                "innerRadius": {"signal": "innerRadius"},
                                "outerRadius": {"signal": "width / 2"},
                                "cornerRadius": {"signal": "cornerRadius"},
                            },
                        },
                    },
                    {
                        "type": "text",
                        "from": {"data": "table"},
                        "encode": {
                            "enter": {
                                "x": {
                                    "signal": "width / 2 + (outerRadius + innerRadius) / 2 * cos((datum.startAngle + datum.endAngle) / 2)"
                                },
                                "y": {
                                    "signal": "height / 2 + (outerRadius + innerRadius) / 2 * sin((datum.startAngle + datum.endAngle) / 2)"
                                },
                                "text": {
                                    "signal": "datum.category + ' (' + datum.value + ')'"
                                },
                                "fontSize": {"value": 10},
                                "align": {"value": "center"},
                                "baseline": {"value": "middle"},
                                "fill": {"value": "black"},
                            }
                        },
                    },
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self):
        """
        Convert the data to the format required by the Vega spec.
        Assumes data is a DataFrame with two columns: one for categories and one for values.
        """
        # Assuming data is a pandas DataFrame
        # Identify the boolean column from selectedColumns
        boolean_column = next(
            (
                col
                for col_dict in self.selectedColumns
                for col, dtype in col_dict.items()
                if dtype == DataTypeCategory.BOOLEAN.value
            ),
            None,
        )
        if boolean_column is None:
            try:
                boolean_column = next(
                    (
                        col
                        for col_dict in self.selectedColumns
                        for col, dtype in col_dict.items()
                        if dtype.value == DataTypeCategory.BOOLEAN.value
                    ),
                    None,
                )
            except Exception as e:
                print(e)

        # Group by the boolean column and count occurrences of True and False
        counts = self.data.groupby(boolean_column).size().reset_index(name="value")

        # Map boolean values to string representation
        counts["category"] = counts[boolean_column].astype(str).str.lower()

        # Prepare the output in the required format
        vega_values = counts[["category", "value"]].to_dict("records")

        return vega_values

    def get_chart_title(self):
        """
        Generate the chart title in the format: "Pie Chart: Column1 vs Column2"
        """
        chart_name = "Pie Chart"
        column_names = " vs ".join(self.data.columns)
        return f"{chart_name}: {column_names}"

    def get_attributes(self):
        return {
            "x_axis": None,
            "y_axis": None,
            "color": "Category",
        }


class ClusteredBarChartOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):
        # Convert data to the required format

        categoryColumn, valueColumns = self.getColumns(self.selectedColumns)
        values, max_stack_value = self.convert_data_to_vega_format(
            self.data, valueColumns
        )
        # Creating the specification for a clustered bar chart
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": values,
                        "transform": [
                            {
                                "type": "fold",
                                "fields": valueColumns,
                                "as": ["CategoryCol", "ValueCol"],
                            },
                            {
                                "type": "stack",
                                "groupby": [categoryColumn],
                                "field": "ValueCol",
                            },
                        ],
                    }
                ],
                "scales": [
                    {
                        "name": "xscale",
                        "type": "band",
                        "domain": {"data": "table", "field": categoryColumn},
                        "range": "width",
                        "padding": 0.05,
                    },
                    {
                        "name": "yscale",
                        "type": "linear",
                        "domain": [0, max_stack_value],
                        "nice": True,
                        "range": "height",
                    },
                    {
                        "name": "color",
                        "type": "ordinal",
                        "domain": {"data": "table", "field": "CategoryCol"},
                        "range": {"scheme": "category10"},
                    },
                ],
                "axes": [
                    {"orient": "bottom", "scale": "xscale", "title": categoryColumn},
                    {"orient": "left", "scale": "yscale", "title": "Sum"},
                ],
                "marks": [
                    {
                        "type": "rect",
                        "from": {"data": "table"},
                        "encode": {
                            "enter": {
                                "x": {"scale": "xscale", "field": categoryColumn},
                                "width": {"scale": "xscale", "band": 1},
                                "y": {"scale": "yscale", "field": "y0"},
                                "y2": {"scale": "yscale", "field": "y1"},
                                "fill": {"scale": "color", "field": "CategoryCol"},
                                "tooltip": {
                                    "signal": "{'"
                                    + categoryColumn
                                    + "': datum['"
                                    + categoryColumn
                                    + "'], 'CategoryCol': datum['CategoryCol'], 'ValueCol': datum['ValueCol']}"
                                },
                            }
                        },
                    }
                ],
                "legends": [{"fill": "color", "title": "CategoryCol"}],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self, data, valueColumns):
        # Assuming data is a pandas DataFrame
        # Identify the boolean column from selectedColumns
        boolean_column = next(
            (
                col
                for col_dict in self.selectedColumns
                for col, dtype in col_dict.items()
                if dtype == DataTypeCategory.CATEGORIES.value
            ),
            None,
        )
        if boolean_column is None:
            try:
                boolean_column = next(
                    (
                        col
                        for col_dict in self.selectedColumns
                        for col, dtype in col_dict.items()
                        if dtype.value == DataTypeCategory.CATEGORIES.value
                    ),
                    None,
                )
            except Exception as e:
                print(e)

        # Group by the boolean column and sum the values
        grouped_data = data.groupby(boolean_column)[valueColumns].sum().reset_index()

        # Calculate the maximum stack value
        max_stack_value = grouped_data[valueColumns].sum(axis=1).max()

        # Convert the grouped DataFrame to the desired list of dictionaries format
        vega_format_data = grouped_data.to_dict(orient="records")

        return vega_format_data, max_stack_value

    def getColumns(self, selectedColumns):
        category_column = None
        number_columns = []

        for col_dict in selectedColumns:
            for col_name, col_type in col_dict.items():
                if col_type.value == DataTypeCategory.CATEGORIES.value:
                    category_column = col_name
                elif col_type.value == DataTypeCategory.NUMBERS.value:
                    number_columns.append(col_name)

        return category_column, number_columns


class ScatterPlotOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns
        self.keys = [list(d.keys())[0] for d in selectedColumns]

    def define(self):
        # Convert data to the required format
        values = self.convert_data_to_vega_format(self.data)
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "title": "Scatter Plot",
                "description": "A basic scatter plot example depicting automobile statistics.",
                "data": [
                    {
                        "name": "source",
                        "values": values,
                    }
                ],
                "scales": [
                    {
                        "name": "x",
                        "type": "linear",
                        "round": True,
                        "nice": True,
                        "zero": True,
                        "domain": {"data": "source", "field": "Value1"},
                        "range": "width",
                    },
                    {
                        "name": "y",
                        "type": "linear",
                        "round": True,
                        "nice": True,
                        "zero": True,
                        "domain": {"data": "source", "field": "Value2"},
                        "range": "height",
                    },
                ],
                "axes": [
                    {
                        "scale": "x",
                        "grid": True,
                        "domain": False,
                        "orient": "bottom",
                        "tickCount": 5,
                        "title": self.keys[0],
                    },
                    {
                        "scale": "y",
                        "grid": True,
                        "domain": False,
                        "orient": "left",
                        "titlePadding": 5,
                        "title": self.keys[1] if len(self.keys) > 1 else self.keys[0],
                    },
                ],
                "marks": [
                    {
                        "name": "marks",
                        "type": "symbol",
                        "from": {"data": "source"},
                        "encode": {
                            "update": {
                                "x": {"scale": "x", "field": "Value1"},
                                "y": {"scale": "y", "field": "Value2"},
                                "shape": {"value": "circle"},
                                "strokeWidth": {"value": 2},
                                "opacity": {"value": 0.5},
                                "stroke": {"value": "#4682b4"},
                                "fill": {"value": "transparent"},
                                "tooltip": {
                                    "signal": f"{{'{self.keys[0]}': datum.Value1, '{self.keys[1]}': datum.Value2}}"
                                },
                            }
                        },
                    }
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self, data):
        """
        Convert the data to the format required by the Vega spec.
        Assumes data is a DataFrame with column names that can be used directly.
        """
        vega_values = [
            {
                f"Value1": row[1][0],
                f"Value2": row[1][1] if len(row[1]) > 1 else row[1][0],
            }
            for row in data.iterrows()
        ]
        return vega_values


class HeatmapOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):
        # Convert data to the required format
        # values = self.convert_data_to_vega_format(self.data)
        vega_spec = self.get_common_vega_spec()

        x_field, y_field, color_field = self.getFields(self.selectedColumns)

        data_list = [
            {
                "x": pd.to_datetime(
                    row[x_field], format="%d-%m-%Y %H:%M", dayfirst=True
                ).strftime("%d"),
                "y": row[y_field],
                "value": row[color_field],
            }
            for _, row in self.data.iterrows()
        ]
        print(data_list, y_field, color_field)
        # Determine the scale types based on data types
        x_scale_type = "band"
        y_scale_type = "band"

        vega_spec.update(
            {
                "description": "A heatmap showing sample data values.",
                "signals": [
                    {
                        "name": "palette",
                        "value": "Viridis",
                        "bind": {
                            "input": "select",
                            "options": heatmapColorOptions,
                        },
                    },
                    {"name": "reverse", "value": False, "bind": {"input": "checkbox"}},
                ],
                "data": [
                    {
                        "name": "heatmap",
                        "values": data_list,
                    }
                ],
                "scales": [
                    {
                        "name": "x",
                        "type": x_scale_type,
                        "domain": {"data": "heatmap", "field": "x"},
                        "range": "width",
                        "padding": 0.1,
                    },
                    {
                        "name": "y",
                        "type": y_scale_type,
                        "domain": {"data": "heatmap", "field": "y"},
                        "range": "height",
                        "padding": 0.1,
                    },
                    {
                        "name": "color",
                        "type": "ordinal",
                        "range": {"scheme": {"signal": "palette"}},
                        "domain": {"data": "heatmap", "field": "value"},
                        "reverse": {"signal": "reverse"},
                    },
                ],
                "axes": [
                    {
                        "orient": "bottom",
                        "scale": "x",
                        "domain": False,
                        "title": "Category",
                    },
                    {"orient": "left", "scale": "y", "domain": False, "title": "Hour"},
                ],
                "legends": [
                    {
                        "fill": "color",
                        "type": "gradient",
                        "title": "Value",
                        "titleFontSize": 12,
                        "titlePadding": 4,
                        "gradientLength": {"signal": "height - 16"},
                    }
                ],
                "marks": [
                    {
                        "type": "rect",
                        "from": {"data": "heatmap"},
                        "encode": {
                            "enter": {
                                "x": {"scale": "x", "field": "x"},
                                "y": {"scale": "y", "field": "y"},
                                "width": {"scale": "x", "band": 1},
                                "height": {"scale": "y", "band": 1},
                                "tooltip": {
                                    "signal": "datum.x + ': ' + datum.y + ' - ' + datum.value"
                                },
                            },
                            "update": {"fill": {"scale": "color", "field": "value"}},
                        },
                    }
                ],
            }
        )
        return vega_spec

    def getFields(self, columns):
        x_field = None
        y_field = None
        color_field = None

        for column in columns:
            for key, value in column.items():
                if value == "dates" and x_field is None:
                    x_field = key
                elif value == "categories" and y_field is None:
                    y_field = key
                elif value == "numbers" and color_field is None:
                    color_field = key

                # Stop the loop if all fields are found
                if x_field and y_field and color_field:
                    break
            if x_field and y_field and color_field:
                break

        return x_field, y_field, color_field


class WordCloudOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):

        # Convert data to the required format
        values = self.convert_data_to_vega_format(self.data)
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": [values],
                        "transform": [
                            {
                                "type": "countpattern",
                                "field": "data",
                                "case": "upper",
                                "pattern": "[\\w']{3,}",
                                "stopwords": "(i|me|my|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|whose|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|will|would|should|can|could|ought|i'm|you're|he's|she's|it's|we're|they're|i've|you've|we've|they've|i'd|you'd|he'd|she'd|we'd|they'd|i'll|you'll|he'll|she'll|we'll|they'll|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|doesn't|don't|didn't|won't|wouldn't|shan't|shouldn't|can't|cannot|couldn't|mustn't|let's|that's|who's|what's|here's|there's|when's|where's|why's|how's|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|upon|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|say|says|said|shall)",
                            },
                            {
                                "type": "formula",
                                "as": "angle",
                                "expr": "[-45, 0, 45][~~(random() * 3)]",
                            },
                            {
                                "type": "formula",
                                "as": "weight",
                                "expr": "if(datum.text=='VEGA', 600, 300)",
                            },
                        ],
                    }
                ],
                "scales": [
                    {
                        "name": "color",
                        "type": "ordinal",
                        "domain": {"data": "table", "field": "text"},
                        "range": ["#d5a928", "#652c90", "#939597"],
                    }
                ],
                "marks": [
                    {
                        "type": "text",
                        "from": {"data": "table"},
                        "encode": {
                            "enter": {
                                "text": {"field": "text"},
                                "align": {"value": "center"},
                                "baseline": {"value": "alphabetic"},
                                "fill": {"scale": "color", "field": "text"},
                            },
                            "update": {"fillOpacity": {"value": 1}},
                            "hover": {"fillOpacity": {"value": 0.5}},
                        },
                        "transform": [
                            {
                                "type": "wordcloud",
                                "size": [400, 200],
                                "text": {"field": "text"},
                                "rotate": {"field": "datum.angle"},
                                "font": "Helvetica Neue, Arial",
                                "fontSize": {"field": "datum.count"},
                                "fontWeight": {"field": "datum.weight"},
                                "fontSizeRange": [6, 32],
                                "padding": 2,
                            }
                        ],
                    }
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self, data):
        # Assuming data is a pandas DataFrame
        combined_string = " ".join(data.astype(str).values.flatten())
        return combined_string


class HistogramOntology(Ontology):
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):

        # Convert data to the required format
        values, columnName = self.convert_data_to_vega_format(self.data)
        minimum = min(x["u"] for x in values)
        maximum = max(x["u"] for x in values)
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {"name": "points", "values": values},
                    {
                        "name": "binned",
                        "source": "points",
                        "transform": [
                            {
                                "type": "bin",
                                "field": "u",
                                "extent": [minimum, maximum],
                                "step": (maximum - minimum) / 10,
                                "as": ["bin0", "bin1"],
                            },
                            {
                                "type": "aggregate",
                                "groupby": ["bin0", "bin1"],
                                "ops": ["count"],
                                "as": ["count"],
                            },
                        ],
                    },
                ],
                "scales": [
                    {
                        "name": "xscale",
                        "type": "linear",
                        "domain": [minimum, maximum],
                        "range": "width",
                        "nice": True,
                        "domainMin": minimum - ((maximum - minimum) / 10),
                    },
                    {
                        "name": "yscale",
                        "type": "linear",
                        "domain": {"data": "binned", "field": "count"},
                        "range": "height",
                        "nice": True,
                        "zero": True,
                    },
                ],
                "axes": [
                    {
                        "orient": "bottom",
                        "scale": "xscale",
                        "title": columnName,
                        "labelAngle": -45,
                        "labelAlign": "right",
                    },
                    {"orient": "left", "scale": "yscale", "title": "Frequency"},
                ],
                "marks": [
                    {
                        "type": "rect",
                        "from": {"data": "binned"},
                        "encode": {
                            "enter": {
                                "x": {"scale": "xscale", "field": "bin0", "offset": 1},
                                "x2": {
                                    "scale": "xscale",
                                    "field": "bin1",
                                    "offset": -1,
                                },
                                "y": {"scale": "yscale", "field": "count"},
                                "y2": {"scale": "yscale", "value": 0},
                                "fill": {"value": "steelblue"},
                                "tooltip": {
                                    "signal": "{'"
                                    + columnName
                                    + "': format(datum.bin0, '.1f') + ' - ' + format(datum.bin1, '.1f'), 'Frequency': datum.count}"
                                },
                            },
                            "update": {"fillOpacity": {"value": 1}},
                            "hover": {"fillOpacity": {"value": 0.5}},
                        },
                    }
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self, data):
        # Assuming data is a pandas DataFrame
        categories = data.columns.tolist()
        values = []
        for i, row in data.iterrows():
            for category in categories:
                values.append(
                    {
                        # "category": category,
                        "u": row[category],
                    }
                )
        return values, category


class TableChartOntology:
    def __init__(self, data, chartType, selectedColumns):
        self.data = data
        self.chartType = chartType
        self.selectedColumns = selectedColumns

    def define(self):
        values = self.convert_data_to_vega_format(self.data)
        columns = self.data.columns.tolist()
        vega_spec = self.get_common_vega_spec(columns, values)
        return vega_spec

    def convert_data_to_vega_format(self, data):
        # Convert the DataFrame to a list of dictionaries
        return data.to_dict(orient="records")

    def get_common_vega_spec(self, columns, values):
        # Define the Vega spec with dynamic columns
        signals = [
            {
                "name": "rowsToDisplay",
                "description": "The number of rows displayed in the table (visible without scrolling)",
                "value": 10,
            },
            {"name": "rowHeight", "description": "Row height in pixels", "value": 40},
            {
                "name": "scrollAreaHeight",
                "description": "Scroll area height in pixels",
                "update": "rowHeight*rowsToDisplay",
            },
            {
                "name": "scrollBarWidth",
                "description": "Scrollbar width in pixels",
                "init": "12",
            },
            {
                "name": "scrollBarHeight",
                "description": "Scrollbar height: Dynamically calculated based on the percentage of visible rows out of all data rows, with a range limited to minimum and maximum values",
                "init": "clamp((rowHeight*rowsToDisplay)*rowsToDisplay/length(data('table')),30,600)",
            },
            {
                "name": "scrollPositionMax",
                "update": "length(data('table'))-rowsToDisplay+1",
            },
            {
                "name": "scrollbarMouseDragY",
                "init": "0",
                "on": [
                    {
                        "events": "[@rect-scrollbar:pointerdown, window:pointerup] > window:pointermove",
                        "update": "clamp(y(),1,scrollAreaHeight)",
                    }
                ],
            },
            {
                "name": "scrollPosition",
                "description": "Scrollbar Position: The scrollbar responds to dragging the scrollbar with a mouse, mouse wheel scrolling, and the Home, End, Page Up, Page Down, Arrow Up, and Arrow Down buttons",
                "value": 1,
                "on": [
                    {
                        "events": {"type": "wheel", "consume": True},
                        "update": "clamp(round(scrollPosition+event.deltaY/abs(event.deltaY)*pow(1.0001, event.deltaY*pow(16, event.deltaMode)),0),1,scrollPositionMax)",
                    },
                    {
                        "events": "window:keydown",
                        "update": "event.code=='Home'?1:event.code=='End'?scrollPositionMax:scrollPosition",
                    },
                    {
                        "events": "window:keydown",
                        "update": "clamp(event.code=='PageDown'?(scrollPosition+rowsToDisplay):event.code=='PageUp'?(scrollPosition-rowsToDisplay):scrollPosition,1,scrollPositionMax)",
                    },
                    {
                        "events": "window:keydown",
                        "update": "clamp(event.code=='ArrowDown'?(scrollPosition+1):event.code=='ArrowUp'?(scrollPosition-1):scrollPosition,1,scrollPositionMax)",
                    },
                    {
                        "events": "[@rect-scrollbar:pointerdown, window:pointerup] > window:pointermove",
                        "update": "clamp(round(invert('scaleScrollBarY',scrollbarMouseDragY),0),1,scrollPositionMax)",
                    },
                ],
            },
            {
                "name": "scrollbarFillOpacity",
                "value": 0.2,
                "on": [
                    {"events": "view:pointerover", "update": "0.4"},
                    {"events": "view:pointerout", "update": "0.2"},
                ],
            },
        ]

        scales = [
            {
                "name": "scaleY",
                "type": "band",
                "domain": {"data": "table", "field": "index", "sort": True},
                "range": [
                    {"signal": "0"},
                    {"signal": "rowHeight*length(data('table'))"},
                ],
            },
            {
                "name": "scaleScrollBarY",
                "type": "linear",
                "domain": [1, {"signal": "scrollPositionMax"}],
                "range": [
                    {"signal": "0"},
                    {"signal": "rowHeight*rowsToDisplay-scrollBarHeight-1"},
                ],
            },
            {
                "name": "scaleRowStripeColors",
                "type": "ordinal",
                "domain": [0, 1],
                "range": ["#FFFFFF", "#EAEAEA"],
            },
        ]

        marks = [
            {
                "name": "rule-scrolltrack-1",
                "type": "rule",
                "encode": {
                    "update": {
                        "x": {"signal": "width-scrollBarWidth-2"},
                        "x2": {"signal": "width-scrollBarWidth-2"},
                        "y": {"signal": "0"},
                        "y2": {"signal": "scrollAreaHeight"},
                        "stroke": {"signal": "'black'"},
                        "strokeWidth": {"signal": "0.2"},
                    }
                },
            },
            {
                "name": "rule-scrolltrack-2",
                "type": "rule",
                "encode": {
                    "update": {
                        "x": {"signal": "width"},
                        "x2": {"signal": "width"},
                        "y": {"signal": "0"},
                        "y2": {"signal": "scrollAreaHeight"},
                        "stroke": {"signal": "'black'"},
                        "strokeWidth": {"signal": "0.2"},
                    }
                },
            },
            {
                "name": "rect-scrollbar",
                "type": "rect",
                "encode": {
                    "update": {
                        "x": {"signal": "width-scrollBarWidth-1"},
                        "y": {"scale": "scaleScrollBarY", "signal": "scrollPosition"},
                        "width": {"signal": "scrollBarWidth"},
                        "height": {"signal": "scrollBarHeight"},
                        "fill": {"value": "#666666"},
                        "fillOpacity": {"signal": "scrollbarFillOpacity"},
                    }
                },
            },
            {
                "name": "rect-table-cell",
                "type": "rect",
                "from": {"data": "table"},
                "encode": {
                    "update": {
                        "x": {"signal": "0"},
                        "x2": {"signal": "width-scrollBarWidth-3"},
                        "y": {"scale": "scaleY", "field": "index", "band": 0},
                        "height": {"signal": "rowHeight"},
                        "fill": {
                            "scale": "scaleRowStripeColors",
                            "signal": "(ceil(datum.index/2,0)==datum.index/2)?1:0",
                        },
                    }
                },
            },
        ]

        # Add text marks for each column dynamically
        for i, column in enumerate(columns):
            marks.append(
                {
                    "name": f"text-cell-content-{i}",
                    "type": "text",
                    "from": {"data": "table"},
                    "encode": {
                        "update": {
                            "text": {"signal": f"datum['{column}']"},
                            "dx": {"value": 5},
                            "y": {"scale": "scaleY", "field": "index", "band": 0.5},
                            "x": {"signal": f"{i * 100}"},
                            "baseline": {"value": "middle"},
                            "align": {"value": "left"},
                        }
                    },
                }
            )

        vega_spec = {
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "An example of a simple table with a scrollbar",
            "width": 300,
            "height": 400,
            "padding": 5,
            "background": "#FFFFFF",
            "config": {
                "title": {"font": "Tahoma", "fontSize": 18},
                "text": {"font": "Tahoma", "fontSize": 16},
            },
            "signals": signals,
            "data": [{"name": "table", "values": values}],
            "scales": scales,
            "title": {"text": "Scrollbar Example"},
            "marks": marks,
        }

        return vega_spec
