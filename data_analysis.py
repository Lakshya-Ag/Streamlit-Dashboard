import xlrd
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import seaborn as sns
import plotly.graph_objs as go

#####################################################################################################################

companies = {}
xls = xlrd.open_workbook("cname.xls")
sh = xls.sheet_by_index(0)
for i in range(505):
    cell_value_class = sh.cell(i, 0).value
    cell_value_id = sh.cell(i, 1).value
    companies[cell_value_class] = cell_value_id

############################################################################

def company_name():
    company = st.sidebar.selectbox("Companies", list(companies.keys()), 0)
    return company
# company = company_name()

############################################################################

def show_data():
    show = st.sidebar.selectbox("Options", ["Graphs", "Company Data"], 0)
    return show
# show_data = show_data()

############################################################################

def data_analysis():
    company = company_name()
    def data_download():
        data = yf.download(tickers=companies[company], period='3650d', interval='1d')

        def divide(j):
            j = j / 1000000
            return j

        data['Volume'] = data['Volume'].apply(divide)
        data.rename(columns={'Volume': 'Volume (in millions)'}, inplace=True)
        return data
    data = data_download()
    show = show_data()
    df1 = data

    if show == "Graphs":
        st.header('Visualization for ' + company)
        check = st.checkbox("Show Moving Average")
        if check:
            ma = st.radio("Moving Average Days", [10,50,100,200])
            df1['MA'] = df1.Close.rolling(ma).mean()
        
            fig = go.Figure(data=[go.Candlestick(x=df1.index,
                                         open=df1['Open'],
                                         high=df1['High'],
                                         low=df1['Low'],
                                         close=df1['Close'],
                                         name='Market Data'),
                          go.Scatter(x=list(df1.index), y=list(df1.MA), line=dict(color='blue', width=2), name='Moving Average')])

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
                                     dict(count=365, label="365D", step="day", stepmode="backward"),
                                     dict(step="all")
                                 ])
                             ))
            st.plotly_chart(fig)
        else:
#             df1['MA'] = df1.Close.rolling(ma).mean()
        
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
                                     dict(count=365, label="365D", step="day", stepmode="backward"),
                                     dict(step="all")
                                 ])
                             ))
            st.plotly_chart(fig)
            
#         ma = st.slider('Slide to select days for Moving Average', min_value=5, max_value=100)
#         df1['MA'] = df1.Close.rolling(ma).mean()
        
#         fig = go.Figure(data=[go.Candlestick(x=df1.index,
#                                      open=df1['Open'],
#                                      high=df1['High'],
#                                      low=df1['Low'],
#                                      close=df1['Close'],
#                                      name='Market Data'),
#                       go.Scatter(x=list(df1.index), y=list(df1.MA), line=dict(color='blue', width=2), name='Moving Average')])

#         fig.update_layout(
#             title='Live share price evolution',
#             yaxis_title='Stock Price (USD per shares)', width=850, height=550)

#         fig.update_xaxes(rangeslider_visible=True,
#                          rangeselector=dict(
#                              buttons=list([
#                                  dict(count=30, label="30D", step="day", stepmode="backward"),
#                                  dict(count=60, label="60D", step="day", stepmode="backward"),
#                                  dict(count=90, label="90D", step="day", stepmode="backward"),
#                                  dict(count=120, label="120D", step="day", stepmode="backward"),
#                                  dict(count=150, label="150D", step="day", stepmode="backward"),
#                                  dict(step="all")
#                              ])
#                          ))
#         st.plotly_chart(fig)

        # ma = st.slider('Slide to select days for Moving Average', min_value=5, max_value=100)
        # df1 = yf.download(tickers=companies[company], period='1460d', interval='1d')
        # df1['MA'] = df1.Close.rolling(ma).mean()
        # fig0 = go.Figure()
        # fig0.add_trace(go.Scatter(x=list(df1.index), y=list(df1.MA)))
        # fig0.update_layout(title_text="Volume of the stock in millions")
        # fig0.update_xaxes(rangeslider_visible=True)
        # st.plotly_chart(fig0)

        st.markdown("### Volume of the stocks")
        st.markdown("Trading volume is a measure of how much of a given financial asset has traded in a period of "
                    "time. For stocks, volume is measured in the number of shares traded and, for futures and options, "
                    "it is based on how many contracts have changed hands.")

        # fig1 = go.Figure()
        # fig1.add_trace(go.Scatter(x=list(data.index), y=list(data['Volume (in millions)'])))

        fig1 = go.Figure([go.Bar(x=data.index, y=data['Volume (in millions)'])])
        fig1.update_layout(title_text="Volume of the stock in millions", width=850, height=550)
        fig1.update_xaxes(rangeslider_visible=True,
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=30, label="30D", step="day", stepmode="backward"),
                                  dict(count=60, label="60D", step="day", stepmode="backward"),
                                  dict(count=90, label="90D", step="day", stepmode="backward"),
                                  dict(count=180, label="180D", step="day", stepmode="backward"),
                                  dict(count=365, label="365D", step="day", stepmode="backward"),
                                  dict(step="all")
                              ])
                          ))

        st.plotly_chart(fig1)
        st.markdown("### Opening prices of the stock")
        st.markdown("The opening price is the price at which a security first trades upon the opening of an exchange "
                    "on a trading day; for example, the National Stock Exchange (NSE) opens at precisely 9:00 a.m. "
                    "Eastern time. The price of the first trade for any listed stock is its daily opening price. The "
                    "opening price is an important marker for that day's trading activity, particularly for those "
                    "interested in measuring short-term results such as day traders.")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=list(data.index), y=list(data.Open)))
        fig2.update_layout(title_text="Opening price of the stock", width=850, height=550)
        fig2.update_xaxes(rangeslider_visible=True,
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=30, label="30D", step="day", stepmode="backward"),
                                  dict(count=60, label="60D", step="day", stepmode="backward"),
                                  dict(count=90, label="90D", step="day", stepmode="backward"),
                                  dict(count=180, label="180D", step="day", stepmode="backward"),
                                  dict(count=365, label="365D", step="day", stepmode="backward"),
                                  dict(step="all")
                              ])
                          ))

        st.plotly_chart(fig2)

        st.markdown("### High price for the stock")
        st.markdown("Today's high refers to a company's intraday high trading price. Today's high is the highest "
                    "price at which a stock traded during the course of the trading day. Today's high is typically "
                    "higher than the closing or opening price. More often than not this is higher than the closing "
                    "price.")

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=list(data.index), y=list(data.High)))
        fig3.update_layout(title_text="High price of the stock", width=850, height=550)
        fig3.update_xaxes(rangeslider_visible=True,
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=30, label="30D", step="day", stepmode="backward"),
                                  dict(count=60, label="60D", step="day", stepmode="backward"),
                                  dict(count=90, label="90D", step="day", stepmode="backward"),
                                  dict(count=180, label="180D", step="day", stepmode="backward"),
                                  dict(count=365, label="365D", step="day", stepmode="backward"),
                                  dict(step="all")
                              ])
                          ))

        st.plotly_chart(fig3)

        st.markdown("### Lowest price for the stock")
        st.markdown("Today’s low is a security's intraday low trading price. Today's low is the lowest price at which a"
                    " stock trades over the course of a trading day. Today's low is typically lower than the opening or"
                    " closing price, as it is unusual that the lowest price of the day would happen to occur at those "
                    "particular moments.")

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=list(data.index), y=list(data.Low)))
        fig4.update_layout(title_text="Low price of the stock", width=850, height=550)
        fig4.update_xaxes(rangeslider_visible=True,
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=30, label="30D", step="day", stepmode="backward"),
                                  dict(count=60, label="60D", step="day", stepmode="backward"),
                                  dict(count=90, label="90D", step="day", stepmode="backward"),
                                  dict(count=180, label="180D", step="day", stepmode="backward"),
                                  dict(count=365, label="365D", step="day", stepmode="backward"),
                                  dict(step="all")
                              ])
                          ))

        st.plotly_chart(fig4)

        st.markdown("### Closing price of the stock")
        st.markdown("The closing price of a stock is the price at which the share closes at the end of trading hours "
                    "of the stock market. In simple terms, the closing price is the weighted average of all prices "
                    "during the last 30 minutes of the trading hours.")

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(x=list(data.index), y=list(data.Close)))
        fig5.update_layout(title_text="Closing price of the stock", width=850, height=550)
        fig5.update_xaxes(rangeslider_visible=True,
                          rangeselector=dict(
                              buttons=list([
                                  dict(count=30, label="30D", step="day", stepmode="backward"),
                                  dict(count=60, label="60D", step="day", stepmode="backward"),
                                  dict(count=90, label="90D", step="day", stepmode="backward"),
                                  dict(count=180, label="180D", step="day", stepmode="backward"),
                                  dict(count=365, label="365D", step="day", stepmode="backward"),
                                  dict(step="all")
                              ])
                          ))

        st.plotly_chart(fig5)

######################################################################################

    elif show == "Company Data":
        symbolticker = companies[company]
        dataticker = yf.Ticker(symbolticker)
        st.header('Information of company ' + company)
        st.markdown(dataticker.info)
        st.markdown("### Stock Price Data")
        st.dataframe(data)
        st.markdown("### International Securities Identification Number")
        st.markdown(dataticker.isin)
        # st.markdown("### Sustainability")
        st.dataframe(dataticker.sustainability)
        st.markdown("### Major Holders")
        st.dataframe(dataticker.major_holders)
        st.markdown("### Institutional Holders")
        st.dataframe(dataticker.institutional_holders)
        st.markdown("### Calendar")
        st.dataframe(dataticker.calendar)
        st.markdown("### Recommendations")
        st.dataframe(dataticker.recommendations)

#############################################################################
if __name__ == "__main__":
    data_analysis()
