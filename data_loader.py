import yfinance as yf
import pandas as pd
import streamlit as st

def get_financial_data(ticker):
    
    try:
        data = yf.download(ticker, period="max", auto_adjust=True)
        
        if data is not None and not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            data.columns = [str(col).capitalize() for col in data.columns]
            return data.dropna()
    except Exception as e:
        st.error(f"Erreur lors du téléchargement de {ticker}: {e}")
    return None
