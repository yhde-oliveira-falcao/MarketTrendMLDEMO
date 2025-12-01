// src/pages/StockSummaryPage.jsx
import React, { useEffect, useState } from "react";
import StockSummary from "../components/StockSummary";

const StockSummaryPage = () => {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
  const token = localStorage.getItem("access_token");

  fetch("http://localhost:8000/stocks/summary", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Unauthorized");
      return res.json();
    })
    .then((data) => setStocks(data))
    .catch((err) => {
      console.error("Failed to fetch stock summary:", err);
      alert("Please login to access stock summary.");
    });
}, []);


  return <StockSummary stocks={stocks} />;
};

export default StockSummaryPage;
