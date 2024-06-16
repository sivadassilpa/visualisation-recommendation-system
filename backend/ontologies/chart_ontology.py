from backend.ontologies.ontology import Ontology
import pandas as pd


class BarChartOntology(Ontology):
    def __init__(self, data):
        self.data = data

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
    def __init__(self, data):
        self.data = data

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
    def define(self):
        return "PieChart Ontology Defined"

    def get_attributes(self):
        return {"slices": "Category", "values": "Values", "color": "Category"}
