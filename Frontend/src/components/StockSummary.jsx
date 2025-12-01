// src/components/StockSummary.jsx
import React from "react";

const StockSummary = ({ stocks }) => {
  return (
    <div className="mt-10">
      <h1 className="text-2xl font-bold text-center mb-6">Stock Summary</h1>
      <div className="flex justify-center">
        <table className="table-auto border-collapse border border-gray-300 w-1/2">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 px-4 py-2">Ticker</th>
              <th className="border border-gray-300 px-4 py-2">Earliest Record</th>
              <th className="border border-gray-300 px-4 py-2">Latest Record</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock, index) => (
              <tr key={index}>
                <td className="border border-gray-300 px-4 py-2">{stock.ticker}</td>
                <td className="border border-gray-300 px-4 py-2">{stock.start_date}</td>
                <td className="border border-gray-300 px-4 py-2">{stock.end_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StockSummary;
