
from security import get_current_user, create_access_token, router as auth_router
from security import create_access_token

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from api_requests import fetch_and_save_stock_data
from database import engine, SessionLocal, get_db
from models import StockDaily, User
import models

from datetime import timedelta
from analysis import predict_knn, get_stock_dataframe

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from security import ACCESS_TOKEN_EXPIRE_MINUTES
import crud
import schemas
import security

#from auth import crud, schemas, get_current_user, router as auth_router
#import auth



app = FastAPI()

# Create tables AFTER ensuring DB exists
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend's domain in prod
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc)
)



#=======================================================================Security and User Management-=======================================================================

from security import router as auth_router
app.include_router(auth_router)


@app.post("/signup", response_model=schemas.UserOut)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in.username, user_in.email, user_in.password)
    return user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/fetch_stock_data/{ticker}")
def fetch_stock_data_route(
    ticker: str,
    from_date: str = None,
    to_date: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    fetch_and_save_stock_data(ticker, db, from_date, to_date)
    return {"message": f"Stock data for {ticker} fetched and saved."}




#=======================================================================Stock Data Management-=======================================================================
@app.get("/stocks/summary")
def get_stocks_summary(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    results = (
        db.query(
            StockDaily.ticker,
            func.min(StockDaily.date).label("start_date"),
            func.max(StockDaily.date).label("end_date")
        )
        .group_by(StockDaily.ticker)
        .all()
    )
    summaries = [
        {"ticker": ticker, "start_date": start_date.isoformat(), "end_date": end_date.isoformat()}
        for ticker, start_date, end_date in results
    ]
    return JSONResponse(content=summaries)



@app.get("/predict/{ticker}")
def predict_stock_price_route(
    ticker: str,
    window_size: int = 10,
    forecast_horizon: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from analysis import analyze_and_predict_trend
    result = analyze_and_predict_trend(ticker, db, window_size, forecast_horizon)
    return JSONResponse(content=result)



@app.get("/predict_chart/{ticker}")
def predict_chart_data(
    ticker: str, 
    window_size: int = 10, 
    forecast_horizon: int = 5, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    df = get_stock_dataframe(ticker, db)
    if df.empty:
        return JSONResponse(status_code=404, content={"error": "No data available."})

    historical = df["close"].tolist()
    dates = [d.strftime("%Y-%m-%d") for d in df.index]

    forecast = predict_knn(df, window_size, forecast_horizon)

    extended_dates = dates + [
        (df.index[-1] + timedelta(days=i+1)).strftime("%Y-%m-%d")
        for i in range(forecast_horizon)
    ]

    historical_extended = historical + [None] * forecast_horizon

    return JSONResponse(content={
        "ticker": ticker,
        "dates": extended_dates,
        "historical": historical_extended,
        "forecast": forecast
    })
