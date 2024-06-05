import React, { useEffect, useRef } from "react";
import * as vega from "vega";

export interface VegaChartProps {
  spec: object;
}

const VegaChart: React.FC<VegaChartProps> = ({ spec }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<vega.View>();

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

  useEffect(() => {
    async function updateView() {
      if (viewRef.current) {
        await viewRef.current.runAsync();
      }
    }

    updateView();
  }, [spec]);

  return <div ref={chartRef} />;
};

export default VegaChart;
