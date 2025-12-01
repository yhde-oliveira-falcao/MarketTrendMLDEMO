import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from models import StockDaily

from dotenv import load_dotenv
load_dotenv()

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

def fetch_and_save_stock_data(ticker_symbol: str, db: Session, from_date: str = None, to_date: str = None):
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker_symbol,
        "outputsize": "full",
        "apikey": STOCK_API_KEY,
    }

    try:
        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        response.raise_for_status()
        data = response.json().get("Time Series (Daily)", {})
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {e}")
        return
    except KeyError:
        print("Unexpected API format")
        return

    from_dt = datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
    to_dt = datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

    added = 0
    for date_str, values in data.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        if from_dt and date_obj < from_dt:
            continue
        if to_dt and date_obj > to_dt:
            continue

        # Check if record exists
        exists = db.query(StockDaily).filter_by(ticker=ticker_symbol, date=date_obj).first()
        if exists:
            continue

        stock_record = StockDaily(
            ticker=ticker_symbol,
            date=date_obj,
            open=float(values["1. open"]),
            high=float(values["2. high"]),
            low=float(values["3. low"]),
            close=float(values["4. close"]),
            volume=int(values["5. volume"])
        )
        db.add(stock_record)
        added += 1

    db.commit()
    print(f"{added} new records inserted for {ticker_symbol}")



