import streamlit as st
import pandas as pd
from faker import Faker

# Import your functions
from utils.gen_data import (
    set_uploadcreate,
    set_num_records,
    generate_fake_data,
    introduce_format_inconsistencies,
    introduce_spelling_errors,
)
from utils.data_match import calc_match_scores, get_top_matches


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


def data_generation_page():
    st.header("Data Creation/Upload")
    if st.session_state.permpage1["uploadcreate"] == "Upload":
        uploadcreateindex = 0
    else:
        uploadcreateindex = 1
    uploadcreate = st.radio(
        "Please select whether you would like to upload your own data, or generate artificial data:",
        ["Upload", "Generate"],
        key="uploadcreate",
        index=uploadcreateindex,
        on_change=set_uploadcreate,
    )

    if st.session_state.permpage1["uploadcreate"] == "Upload":
        uploadcol1, uploadcol2 = st.columns(2)
        with uploadcol1:
            file1 = st.file_uploader(
                "Please upload your first file:", type="csv", key="file1"
            )

        with uploadcol2:
            file2 = st.file_uploader(
                "Please upload your second file:", type="csv", key="file2"
            )

        uploaddisplaycol1, uploaddisplaycol2 = st.columns(2)

        if file1 is not None:
            st.session_state.df1_from_upload = pd.read_csv(file1)
        if st.session_state.df1_from_upload is not None and (
            st.session_state.df1_final is None
            or st.session_state.df1_from_upload.equals(st.session_state.df1_final)
        ):
            with uploaddisplaycol1:
                st.subheader("DataFrame 1:")
                st.write(st.session_state.df1_from_upload.head(3))

        if file2 is not None:
            st.session_state.df2_from_upload = pd.read_csv(file2)
        if st.session_state.df2_from_upload is not None and (
            st.session_state.df2_final is None
            or st.session_state.df2_from_upload.equals(st.session_state.df2_final)
        ):
            with uploaddisplaycol2:
                st.subheader("DataFrame 2:")
                st.write(st.session_state.df2_from_upload.head(3))

        st.session_state.df1_final = st.session_state.df1_from_upload
        st.session_state.df2_final = st.session_state.df2_from_upload

    else:
        # User inputs
        num_records = st.number_input(
            "Number of records for DataFrames",
            key="num_records",
            min_value=1,
            value=st.session_state.permpage1["num_records"],
            step=1,
            on_change=set_num_records,
        )

        # Generate DataFrames
        if st.button("Generate DataFrames"):
            st.session_state.df1 = generate_fake_data(num_records)
            st.session_state.df2 = st.session_state.df1.copy()

        if st.session_state.df1 is not None and st.session_state.df2 is not None:
            # Display initial DataFrames
            st.subheader("Initial DataFrame")
            st.write(st.session_state.df1.head(3))

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            spelling_error_rate1 = st.slider(
                "Spelling error rate (DataFrame 1)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
            spelling_error_rate2 = st.slider(
                "Spelling error rate (DataFrame 2)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
        with col2:
            date_error_rate1 = st.slider(
                "Date error rate (DataFrame 1)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
            date_error_rate2 = st.slider(
                "Date error rate (DataFrame 2)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
        with col3:
            phone_error_rate1 = st.slider(
                "Phone error rate (DataFrame 1)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
            phone_error_rate2 = st.slider(
                "Phone error rate (DataFrame 2)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
        with col4:
            address_error_rate1 = st.slider(
                "Address error rate (DataFrame 1)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
            address_error_rate2 = st.slider(
                "Address error rate (DataFrame 2)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
            name_error_rate1 = (
                address_error_rate1  # Use the same error rate for name as address
            )
            name_error_rate2 = (
                address_error_rate2  # Use the same error rate for name as address
            )
        with col5:
            timestamp_error_rate1 = st.slider(
                "Timestamp error rate (DataFrame 1)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )
            timestamp_error_rate2 = st.slider(
                "Timestamp error rate (DataFrame 2)",
                min_value=0.0,
                max_value=0.3,
                value=0.0,
                step=0.01,
            )

        # Introduce errors
        if st.button("Introduce Errors"):
            st.session_state.df1_with_errors = introduce_spelling_errors(
                st.session_state.df1, error_rate=spelling_error_rate1
            )
            st.session_state.df1_with_errors = introduce_format_inconsistencies(
                st.session_state.df1_with_errors,
                columns=["date", "phone", "address", "name", "timestamp"],
                date_inconsistency_rate=date_error_rate1,
                phone_inconsistency_rate=phone_error_rate1,
                phone_variation_rate=phone_error_rate1,
                address_capitalization_rate=address_error_rate1,
                address_comma_rate=address_error_rate1,
                address_abbreviation_rate=address_error_rate1,
                name_abbreviation_rate=name_error_rate1,
                name_title_rate=name_error_rate1,
                timestamp_inconsistency_rate=timestamp_error_rate1,
            )

            st.session_state.df2_with_errors = introduce_spelling_errors(
                st.session_state.df2, error_rate=spelling_error_rate2
            )
            st.session_state.df2_with_errors = introduce_format_inconsistencies(
                st.session_state.df2_with_errors,
                columns=["date", "phone", "address", "name", "timestamp"],
                date_inconsistency_rate=date_error_rate2,
                phone_inconsistency_rate=phone_error_rate2,
                phone_variation_rate=phone_error_rate2,
                address_capitalization_rate=address_error_rate2,
                address_comma_rate=address_error_rate2,
                address_abbreviation_rate=address_error_rate2,
                name_abbreviation_rate=name_error_rate2,
                name_title_rate=name_error_rate2,
                timestamp_inconsistency_rate=timestamp_error_rate2,
            )

        # Display DataFrames with errors
        if (
            st.session_state.df1_with_errors is not None
            and st.session_state.df2_with_errors is not None
        ):
            st.subheader("DataFrames with Errors")
            st.write("DataFrame 1 with errors (first 5 rows):")
            st.write(st.session_state.df1_with_errors.head(3))
            st.write("DataFrame 2 with errors (first 5 rows):")
            st.write(st.session_state.df2_with_errors.head(3))
            st.session_state.df1_final = st.session_state.df1_with_errors
            st.session_state.df2_final = st.session_state.df2_with_errors


data_generation_page()
