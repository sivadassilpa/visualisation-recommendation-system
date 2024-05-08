import React, { useEffect, useRef } from "react";
import * as vega from "vega";

interface VegaChartProps {
  spec: object; // The Vega specification without the data
  data: object[]; // The data for the chart
}

const VegaChart: React.FC<VegaChartProps> = ({ spec, data }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<vega.View>();

  // Initialize the chart
  useEffect(() => {
    async function createView() {
      try {
        if (chartRef.current) {
          const view = new vega.View(vega.parse(spec), {
            renderer: "canvas",
            container: chartRef.current,
            hover: true,
          });
          viewRef.current = view;
          await view.runAsync();
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (chartRef.current && !viewRef.current) {
      createView();
    }
  }, [spec]);

  // Update data when it changes
  useEffect(() => {
    async function updateData() {
      if (viewRef.current) {
        viewRef.current.change(
          "data",
          vega
            .changeset()
            .remove(() => true)
            .insert(data)
        );
        await viewRef.current.runAsync();
      }
    }

    updateData();
  }, [data]);

  return <div ref={chartRef} />;
};

export default VegaChart;
