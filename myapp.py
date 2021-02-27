import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
# import matplotlib.pyplot as plt
# import matplotlib.animation as ani

st.header("Stock Market Analysis")
companies = {"Tesla":"TSLA", "Apple":"AAPL", "Google":"GOOGL"}
def show_data():
    show = st.sidebar.selectbox("Things you wanna see!!", ["Stock Price Data","Visual Representation"], 0)
    return show
show_data = show_data()

############################################################################

def company_name():
    company = st.sidebar.selectbox("Companies", list(companies.keys()), 0)
    return company
company = company_name()

############################################################################

data = yf.download(tickers=companies[company], period='180d', interval='1d')
def divide(j):
    j = j / 1000000
    return j
data['Volume'] = data['Volume'].apply(divide)
data.rename(columns={'Volume':'Volume (in millions)'}, inplace=True)

############################################################################

if show_data == "Stock Price Data":
    st.dataframe(data)

############################################################################

elif show_data == "Visual Representation":
    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='market data'))

    fig.update_layout(
        title='Live share price evolution',
        yaxis_title='Stock Price (USD per shares)')

    # button_list = {
    #     "All":dict(step="all"),
    #     "30 days":dict(count=30, step="day", stepmode="backward"),
    #     "60 days":dict(count=60, step="day", stepmode="backward"),
    #     "90 days":dict(count=90, step="day", stepmode="backward"),
    #     "120 days":dict(count=120, step="day", stepmode="backward"),
    #     "150 days":dict(count=150, step="day", stepmode="backward")
    # }
    # button = st.sidebar.radio("Radio", list(button_list.keys()))

    fig.update_xaxes(rangeslider_visible=True,
                     rangeselector= dict(
                         buttons=list([
                             dict(count=30, label="30D", step="day", stepmode="backward"),
                             dict(count=60, label="60D", step="day", stepmode="backward"),
                             dict(count=90, label="90D", step="day", stepmode="backward"),
                             dict(count=120, label="120D", step="day", stepmode="backward"),
                             dict(count=150, label="150D", step="day", stepmode="backward"),
                             dict(step="all")
                         ])
    ))

    st.plotly_chart(fig)