import urllib
import pandas as pd
import numpy as np
import streamlit as st

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
