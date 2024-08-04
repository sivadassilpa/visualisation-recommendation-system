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
