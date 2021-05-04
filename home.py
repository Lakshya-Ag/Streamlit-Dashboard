import urllib
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import matplotlib.pyplot as plt
plt.style.use('bmh')

############################################################################
def main():
    box = st.selectbox("Information", ["Stock Market Info", "Covid-19 impact"])
    if box == "Stock Market Info":
        readme_text = st.markdown(get_file_content_as_string("README.md"))
    elif box == "Covid-19 impact":
        df1 = yf.download(tickers="NIFTY 50", start="2020-01-01", end="2020-12-31")
        fig = go.Figure(data=[go.Candlestick(x=df1.index,
                                             open=df1['Open'],
                                             high=df1['High'],
                                             low=df1['Low'],
                                             close=df1['Close'],
                                             name='Market Data')
                              ])
        fig.update_layout(
            title='Live share price evolution',
            yaxis_title='Stock Price (USD per shares)', width=850, height=550)

        fig.update_xaxes(rangeslider_visible=True,
                         rangeselector=dict(
                             buttons=list([
                                 dict(count=30, label="30D", step="day", stepmode="backward"),
                                 dict(count=60, label="60D", step="day", stepmode="backward"),
                                 dict(count=90, label="90D", step="day", stepmode="backward"),
                                 dict(count=180, label="180D", step="day", stepmode="backward"),
                                 dict(count=270, label="270D", step="day", stepmode="backward"),
                                 dict(step="all")
                             ])
                         ))
        st.plotly_chart(fig)
###########################################################################

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/Lakshya-Ag/Streamlit-Dashboard/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

##################################################################################

if __name__ == "__main__":
    main()
