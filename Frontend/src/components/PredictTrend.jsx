import React, { useState, useRef } from "react";
import Chart from "chart.js/auto";
const token = localStorage.getItem("access_token");


const PredictTrend = () => {
  const [ticker, setTicker] = useState("");
  const [windowSize, setWindowSize] = useState(10);
  const [forecastHorizon, setForecastHorizon] = useState(5);
  const chartRef = useRef(null);
  const canvasRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Estimate clicked");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/predict_chart/${ticker}?window_size=${windowSize}&forecast_horizon=${forecastHorizon}`, { headers: { Authorization: `Bearer ${token}`, }, }
      );

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log("Received data:", data);

      const { historical, forecast, dates: baseDates } = data;

      const lastDate = new Date(baseDates[baseDates.length - 1]);
      const futureDates = [];

      for (let i = 1; i <= forecast.length; i++) {
        const nextDate = new Date(lastDate);
        nextDate.setDate(lastDate.getDate() + i);
        futureDates.push(nextDate.toISOString().split("T")[0]);
      }

      const labels = [...baseDates, ...futureDates];

      if (chartRef.current) {
        chartRef.current.destroy();
      }

      chartRef.current = new Chart(canvasRef.current, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Historical Close",
              data: [...historical, ...new Array(forecast.length).fill(null)],
              borderColor: "blue",
              backgroundColor: "rgba(0, 0, 255, 0.2)",
              fill: false,
            },
            {
              label: "Forecast",
              data: [...new Array(historical.length).fill(null), ...forecast],
              borderColor: "deeppink",
              backgroundColor: "rgba(255, 20, 147, 0.2)",
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: { display: true },
            y: { display: true },
          },
        },
      });
    } catch (error) {
      console.error("Failed to fetch prediction data:", error);
      alert("Prediction failed: " + error.message);
    }
  };

  return (
    <div style={{ margin: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>Predict Stock Trend</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <label>
          Ticker:
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            required
            style={{ margin: "0 1rem" }}
          />
        </label>

        <label>
          Window Size:
          <input
            type="number"
            value={windowSize}
            onChange={(e) => setWindowSize(Number(e.target.value))}
            required
            style={{ margin: "0 1rem" }}
          />
        </label>

        <label>
          Forecast Horizon:
          <input
            type="number"
            value={forecastHorizon}
            onChange={(e) => setForecastHorizon(Number(e.target.value))}
            required
            style={{ margin: "0 1rem" }}
          />
        </label>

        <button type="submit">Estimate</button>
      </form>

      <canvas
        ref={canvasRef}
        id="predictionChart"
        style={{
          width: "100%",
          height: "auto",
          aspectRatio: "2 / 1",
        }}
      ></canvas>
    </div>
  );
};

export default PredictTrend;
