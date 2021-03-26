import xlrd
import pandas as pd
import streamlit as st
import yfinance as yf
# import seaborn as sns
import plotly.graph_objs as go
# import matplotlib.pyplot as plt
# import matplotlib.animation as ani


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
# df = pd.read_excel('cname.xlsx')
# for index, row in df.iterrows():
#   companies[row[0]] = row[1]

xls = xlrd.open_workbook("cname.xlsx")
sh = xls.sheet_by_index(0)
for i in range(505):
    cell_value_class = sh.cell(i,0).value
    cell_value_id = sh.cell(i,1).value
    companies[cell_value_class] = cell_value_id

############################################################################

def company_name():
    company = st.sidebar.selectbox("Companies", list(companies.keys()), 0)
    return company
company = company_name()

############################################################################

def show_data():
    show = st.sidebar.selectbox("Options", ["Graphs", "Company Data"], 0)
    return show
show_data = show_data()

############################################################################


data = yf.download(tickers=companies[company], period='180d', interval='1d')
def divide(j):
    j = j / 1000000
    return j
data['Volume'] = data['Volume'].apply(divide)
data.rename(columns={'Volume':'Volume (in millions)'}, inplace=True)

############################################################################

if show_data == "Graphs":
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

elif show_data == "Company Data":
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
