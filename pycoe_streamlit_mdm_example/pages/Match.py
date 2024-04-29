import streamlit as st
import pandas as pd

# Import your functions
from utils.data_match import calc_match_scores, get_top_matches


def matching_process_page():
    st.header("Matching Process")

    # Check if DataFrames with errors exist
    if st.session_state.df1_final is None or st.session_state.df2_final is None:
        st.warning(
            "Please generate DataFrames and introduce errors in the Data Generation page first."
        )
        return

    st.write("DataFrames for matching:")
    matchdf_col1, matchdf_col2 = st.columns(2)
    with matchdf_col1:
        st.write(st.session_state.df1_final.head(3))
    with matchdf_col2:
        st.write(st.session_state.df2_final.head(3))

    if st.button("Clear DataFrames"):
        st.session_state.df1_final = None
        st.session_state.df2_final = None
        return

    # Column selection for matching
    st.subheader("Column Selection for Matching")
    col_info = []
    weights = []
    nummatchescol1, nummatchescol2, nummatchescol3, nummatchescol4 = st.columns(4)
    with nummatchescol1:
        num_cols = st.number_input(
            "Number of columns to match", min_value=1, value=1, step=1
        )
    st.divider()
    (
        matchselectcol1,
        matchselectcol2,
        matchselectcol3,
        matchselectcol4,
        matchselectcol5,
    ) = st.columns(5)
    for i in range(num_cols):
        with matchselectcol1:
            col_name1 = st.selectbox(
                f"Column {i+1} in DataFrame 1",
                st.session_state.df1_final.columns,
                key=f"col1_{i}",
            )
        with matchselectcol2:
            col_name2 = st.selectbox(
                f"Column {i+1} in DataFrame 2",
                st.session_state.df2_final.columns,
                key=f"col2_{i}",
            )
        with matchselectcol3:
            st.write(f"Exact Compare for Column {i+1} ")
            exact_compare = st.checkbox("", value=True, key=f"exact_{i}")
        with matchselectcol4:
            if not exact_compare:
                method = st.selectbox(
                    f"Matching Method for Column {i+1}",
                    [
                        "jaro",
                        "jarowinkler",
                        "levenshtein",
                        "damerau_levenshtein",
                        "qgram",
                        "cosine",
                        "smith_waterman",
                        "lcs",
                    ],
                    key=f"method_{i}",
                )
            else:
                method = None
        with matchselectcol5:
            weight = st.number_input(
                f"Weight for Column {i+1}",
                min_value=0.0,
                max_value=1.0,
                value=1.0 / num_cols,
                step=0.01,
                key=f"weight_{i}",
            )

        col_info.append(
            {
                "name1": col_name1,
                "name2": col_name2,
                "ExactCompare": exact_compare,
                "method": method,
            }
        )
        weights.append(weight)

    # Check if weights sum up to 1
    if sum(weights) != 1.0:
        st.warning("Please ensure that the weights sum up to 1.")
        return

    # Matching process
    if st.button("Run Matching Process"):
        output_scores = calc_match_scores(
            st.session_state.df1_final, st.session_state.df2_final, col_info
        )
        top_matches = get_top_matches(
            output_scores,
            st.session_state.df1_final,
            st.session_state.df2_final,
            weights,
        )
        st.subheader("Top Matches")
        st.write(top_matches.head())


matching_process_page()
