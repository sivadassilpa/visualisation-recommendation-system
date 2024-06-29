from backend.ontologies.ontology import Ontology
import pandas as pd

from backend.utils.dataTypes import DataTypeCategory


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
                    {"orient": "left", "scale": "yscale"},
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
                        "domain": {"data": "table", "field": "amount"},
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
                                "y": {"scale": "yscale", "field": "amount"},
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
                                    "signal": "tooltip.amount",
                                    "offset": -2,
                                },
                                "text": {"signal": "tooltip.amount"},
                                "fillOpacity": [
                                    {"test": "isNaN(tooltip.amount)", "value": 0},
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
        categories = data.columns.tolist()
        values = []
        for i, row in data.iterrows():
            for category in categories:
                values.append(
                    {
                        "category": category,
                        "amount": row[category],
                        "series": category,  # Change this if there are multiple series
                    }
                )
        return values


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
                        "bind": {"input": "range", "min": 0, "max": 6.29, "step": 0.01},
                    },
                    {
                        "name": "endAngle",
                        "value": 6.29,
                        "bind": {"input": "range", "min": 0, "max": 6.29, "step": 0.01},
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
                    }
                ],
            }
        )
        return vega_spec

    def convert_data_to_vega_format(self):
        """
        Convert the data to the format required by the Vega spec.
        Assumes data is a DataFrame with two columns: one for categories and one for values.
        """
        # Identify the boolean column from selectedColumns
        boolean_column = next(
            (
                col
                for col_dict in self.selectedColumns
                for col, dtype in col_dict.items()
                if dtype == DataTypeCategory.BOOLEAN
            ),
            None,
        )
        if boolean_column is None:
            raise ValueError("No boolean column found in selectedColumns")

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
