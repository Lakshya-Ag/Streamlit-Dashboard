import urllib
import xlrd
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import seaborn as sns
import plotly.graph_objs as go
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
import matplotlib.pyplot as plt
plt.style.use('bmh')
import sqlite3
conn=sqlite3.connect('Data.db')
c=conn.cursor()
import quandl
import matplotlib.animation as ani
import altair as alt

############################################################################
def main():
    st.success("Select Data Analysis or prediction to move on")
    readme_text = st.markdown(get_file_content_as_string("README.md"))
###########################################################################

def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/Lakshya-Ag/Streamlit-Dashboard/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

##################################################################################

if __name__ == "__main__":
    main()