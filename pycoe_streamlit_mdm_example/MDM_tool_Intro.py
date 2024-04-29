##This is our main


import streamlit as st

permpage1 = {"num_records": 10, "uploadcreate": "Upload"}

# Define session state variables
if "df1" not in st.session_state:
    st.session_state.df1 = None
if "df2" not in st.session_state:
    st.session_state.df2 = None
if "df1_with_errors" not in st.session_state:
    st.session_state.df1_with_errors = None
if "df2_with_errors" not in st.session_state:
    st.session_state.df2_with_errors = None
if "df1_from_upload" not in st.session_state:
    st.session_state.df1_from_upload = None
if "df2_from_upload" not in st.session_state:
    st.session_state.df2_from_upload = None
##final df defined to take to match page
if "df1_final" not in st.session_state:
    st.session_state.df1_final = None
if "df2_final" not in st.session_state:
    st.session_state.df2_final = None

if "permpage1" not in st.session_state:
    st.session_state.permpage1 = permpage1


st.set_page_config(
    page_title="MDM Tool Introduction", layout="wide", initial_sidebar_state="auto"
)
st.image("images/KA_DM_Header.png")
st.title("Welcome To The Kubrick MDM Training and Development Tool")
st.markdown(
    "This tool is designed to be used by data management consultants to help them understand the fundamentals of master data management."
)
st.divider()
st.write("""The application is split into three separate sections:""")
st.markdown(
    "- Data Creation/Upload, where you the data used in the exercise will be introduced"
)
st.markdown(
    "- Matching, where you will select the columns to match, the methods to match them by, and the weight each matched pair should have in the output"
)
st.markdown(
    "- Merging, where you will select how the merge process should take place, to produce one master dataset."
)
st.write(
    "Please navigate to the different pages using the page selection on the left of the application"
)
st.divider()
st.divider()
st.markdown(
    """Developed by Matthew Pilkington. Repository for the code can be found in Kubrick's ADO instance
         - please reach out to matthewpilkington@kubrickgroup.com if you are interested."""
)
