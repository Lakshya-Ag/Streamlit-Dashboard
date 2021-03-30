import urllib
import xlrd
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import seaborn as sns
import plotly.graph_objs as go
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
plt.style.use('bmh')
import matplotlib.animation as ani
import altair as alt

########################################################################################################################

def main():
    readme_text = st.markdown(get_file_content_as_string("README.md"))
    st.sidebar.header("What To Do")
    app_mode = st.sidebar.selectbox("Select the app mode", ["Cover Page", "Data Analysis", "Prediction", "Show the Code"])
    if app_mode == "Cover Page":
        st.sidebar.success("Select Data Analysis or prediction to move on")
    elif app_mode == "Data Analysis":
        readme_text.empty()
        data_analysis()
    elif app_mode == "Prediction":
        readme_text.empty()
        prediction()
    elif app_mode == "Show the Code":
        readme_text.empty()
        st.code(get_file_content_as_string("myapp.py"))

########################################################################################################################

# companies = {"Tesla":"TSLA","Apple":"AAPL","Google":"GOOGL","Microsoft":"MSFT","Amazon":"AMZN",
#              "Facebook":"FB","Alibaba":"BABA","Berkshire Hathway":"BRK.A","Visa":"V","JPMorgan Chase":"JPM",
#              "Johnson & Johnson":"JNJ","Mastercard":"MA","Disney":"DIS","Walmart":"WMT","Taiwan Semiconductor":"TSM",
#              "United Health":"UNH","Bank of America":"BAC","Procter & Gamble":"PG","NVIDIA":"NVDA","Home Depot":"HD",
#              "PayPal":"PYPL","ExxonMobil":"XOM","Comcast":"CMCSA","Intel":"INTC","Verizon":"VZ",
#              "Coca Cola":"KO","Netflix":"NFLX","AT&T":"T","Oracle":"ORCL","Nike":"NKE","Chevron":"CVX",
#              "ASML":"ASML","Toyota":"TM","Abbott Laboratories":"ABT","Adobe":"ADBE","Cisco Systems":"CSCO",
#              "Eli Lilly":"LLY","Pfizer":"PFE","Salesforce":"CRM","Novartis AG":"NVS","Merck":"MRK",
#              "AbbVie":"ABBV","Pepsi":"PEP","Thermo Fischer Scientific":"TMO","Boardcom":"AVGO","Pinduoduo":"PDD",
#              "Royal Dutch Shell":"RDS.A","Accenture":"ACN","Wells Fargo":"WFC","T-Mobile US":"TMUS"}


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

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/Lakshya-Ag/Streamlit-Dashboard/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

############################################################################


# def data_download():
#     company = company_name()
#     data = yf.download(tickers=companies[company], period='180d', interval='1d')
#
#     def divide(j):
#         j = j / 1000000
#         return j
#
#     data['Volume'] = data['Volume'].apply(divide)
#     data.rename(columns={'Volume': 'Volume (in millions)'}, inplace=True)
#     return data

###################################################################################

def data_analysis():
    company = company_name()
    def data_download():
        data = yf.download(tickers=companies[company], period='180d', interval='1d')

        def divide(j):
            j = j / 1000000
            return j

        data['Volume'] = data['Volume'].apply(divide)
        data.rename(columns={'Volume': 'Volume (in millions)'}, inplace=True)
        return data
    data = data_download()
    show = show_data()
    if show == "Graphs":
        st.header('Visualization for ' + company)
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
                         rangeselector=dict(
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

        st.markdown("### Volume of the stocks")
        st.line_chart(data['Volume (in millions)'])
        st.markdown("### Opening prices of the stock")
        st.line_chart(data['Open'])
        st.markdown("### High price for the stock")
        st.line_chart(data['High'])
        st.markdown("### Lowest price for the stock")
        st.line_chart(data['Low'])
        st.markdown("### Closing price of the stock")
        st.line_chart(data['Close'])

    ############################################################################

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

    ################################################################################################################

    # elif show_data == "Animation":
    # data2 = data.drop(['Adj Close', 'Open', 'High', 'Low'], axis=1)
    # color = ['orange', 'purple']
    # fig1 = plt.figure(figsize=(9, 5))
    # plt.ion()
    # plt.xticks(rotation=45, ha="right", rotation_mode="anchor")  # rotate the x-axis values
    # plt.subplots_adjust(bottom=0.2, top=0.9)  # ensuring the dates (on the x-axis) fit in the screen
    #
    #
    # def buildmebarchart(i=int):
    #     plt.legend(data2.columns)
    #     p = plt.plot(data2[:i].index, data2[:i].values,
    #                  linewidth=0.8)  # note it only returns the dataset, up to the point i
    #
    #     for i in range(0, 2):
    #         p[i].set_color(color[i])  # set the colour of each curve
    #
    #
    # animator = ani.FuncAnimation(fig1, buildmebarchart, interval=500)
    #
    # st.plotly_chart(fig1)

###################################################################################

def prediction():
    def data_download():
        company = company_name()
        data = yf.download(tickers=companies[company], period='200d', interval='1d')

        def divide(j):
            j = j / 1000000
            return j

        data['Volume'] = data['Volume'].apply(divide)
        data.rename(columns={'Volume': 'Volume (in millions)'}, inplace=True)
        return data
    df = data_download()
    
    pred = st.sidebar.radio("Regression Type", ["Linear Regression", "Tree Prediction"])

    # removing index which is date
    df['Date'] = df.index
    df.reset_index(drop=True, inplace=True)

    # rearranging the columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume (in millions)']]

    df = df[['Close']]

    # create a variable to predict 'x' days out into the future
    future_days = 50
    # create a new column( target) shifted 'x' units/days up
    df['Prediction'] = df[['Close']].shift(-future_days)

    # create the feature data set (x) and convet it to a numpy array and remove the last 'x' rows
    x = np.array(df.drop(['Prediction'], 1))[:-future_days]

    # create a new target dataset (y) and convert it to a numpy array and get all of the target values except the last'x' rows)
    y = np.array(df['Prediction'])[:-future_days]

    # split the data into 75% training and 25% testing
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # create the models
    # create the decision treee regressor model
    tree = DecisionTreeRegressor().fit(x_train, y_train)
    # create the linear regression model
    lr = LinearRegression().fit(x_train, y_train)

    # get the last x rows of the feature dataset
    x_future = df.drop(['Prediction'], 1)[:-future_days]
    x_future = x_future.tail(future_days)
    x_future = np.array(x_future)

    # show the model tree prediction
    tree_prediction = tree.predict(x_future)

    # show thw model linear regression prediction
    lr_prediction = lr.predict(x_future)

    if pred == "Linear Regression":
        predictions = lr_prediction
        valid = df[x.shape[0]:]
        valid['predictions'] = predictions

        # alter
        data = {'Close': [], 'Vclose': [], 'Vpredictions': []}
        mod = pd.DataFrame(data)
        mod.set_index = 'index'
        mod.Close = df.Close

        # mod.Vclose = df.Close.loc[:747]
        # mod.Vpredictions = df.Close.loc[:747]

        mod.Vclose.loc[148:] = valid.Close
        mod.Vpredictions.loc[148:] = valid.predictions
        mod.Close = df.Close.loc[:150]
        # plt.figure(figsize=(16,8))
        # plt.plot(mod.Vpredictions,color='white')
        # plt.plot(mod.Close, color='lightgrey')
        chart_data = mod
        st.line_chart(chart_data)

    elif pred == "Tree Prediction":
        predictions = tree_prediction
        valid = df[x.shape[0]:]
        valid['predictions'] = predictions

        # alter
        data = {'Close': [], 'Vclose': [], 'Vpredictions': []}
        mod = pd.DataFrame(data)
        mod.set_index = 'index'
        mod.Close = df.Close

        # mod.Vclose = df.Close.loc[:747]
        # mod.Vpredictions = df.Close.loc[:747]

        mod.Vclose.loc[148:] = valid.Close
        mod.Vpredictions.loc[148:] = valid.predictions
        mod.Close = df.Close.loc[:150]
        # plt.figure(figsize=(16,8))
        # plt.plot(mod.Vpredictions,color='white')
        # plt.plot(mod.Close, color='lightgrey')
        chart_data = mod
        st.line_chart(chart_data)


##################################################################################

if __name__ == "__main__":
    main()
