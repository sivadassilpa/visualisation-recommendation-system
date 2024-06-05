from backend.ontologies.ontology import Ontology
import pandas as pd


class LineChartOntology(Ontology):
    def define(self, data: pd.DataFrame):
        vega_spec = self.get_common_vega_spec()

        # Extract fields from data
        x_field = data.columns[0]  # Assuming the first column is x-axis
        y_field = data.columns[1]  # Assuming the second column is y-axis
        category_field = data.columns[2] if len(data.columns) > 2 else None
        # Assuming the third column is category

        # Convert DataFrame to dictionary for Vega
        values = data.to_dict(orient="records")

        # Determine if the category field is necessary
        if category_field and data[category_field].nunique() > 1:
            groupby_category = True
        else:
            groupby_category = False
            category_field = None  # Remove the category field if not needed

        # Update the vega_spec with dynamic data
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
                        "domain": {"data": "table", "field": x_field},
                    },
                    {
                        "name": "y",
                        "type": "linear",
                        "range": "height",
                        "nice": True,
                        "zero": True,
                        "domain": {"data": "table", "field": y_field},
                    },
                    (
                        {
                            "name": "color",
                            "type": "ordinal",
                            "range": "category",
                            "domain": {"data": "table", "field": category_field},
                        }
                        if category_field
                        else None
                    ),
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
                "marks": [
                    {
                        "type": "group",
                        "from": (
                            {
                                "facet": {
                                    "name": "series",
                                    "data": "table",
                                    "groupby": category_field,
                                }
                            }
                            if groupby_category
                            else {"data": "table"}
                        ),
                        "marks": [
                            {
                                "type": "line",
                                "from": (
                                    {"data": "series"}
                                    if groupby_category
                                    else {"data": "table"}
                                ),
                                "encode": {
                                    "enter": {
                                        "x": {"scale": "x", "field": x_field},
                                        "y": {"scale": "y", "field": y_field},
                                        "stroke": (
                                            {"scale": "color", "field": category_field}
                                            if category_field
                                            else {"value": "steelblue"}
                                        ),
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

        # Remove any None values that might have been added
        vega_spec["scales"] = [scale for scale in vega_spec["scales"] if scale]

        return vega_spec


class BarChartOntology(Ontology):
    def define(self):
        vega_spec = self.get_common_vega_spec()
        vega_spec.update(
            {
                "data": [
                    {
                        "name": "table",
                        "values": [
                            {"category": "A", "amount": 28},
                            {"category": "B", "amount": 55},
                            {"category": "C", "amount": 43},
                            {"category": "D", "amount": 91},
                            {"category": "E", "amount": 81},
                            {"category": "F", "amount": 53},
                            {"category": "G", "amount": 19},
                            {"category": "H", "amount": 87},
                        ],
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


class PieChartOntology(Ontology):
    def define(self):
        return "PieChart Ontology Defined"

    def get_attributes(self):
        return {"slices": "Category", "values": "Values", "color": "Category"}
