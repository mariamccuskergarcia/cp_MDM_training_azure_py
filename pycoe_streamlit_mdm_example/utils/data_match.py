import recordlinkage as rl
import pandas as pd


def calc_match_scores(df1, df2, col_info) -> pd.DataFrame:
    """
    Calculate match scores between two DataFrames based on column information.

    Args:
        df1 (pandas.DataFrame): The first DataFrame.
        df2 (pandas.DataFrame): The second DataFrame.
        col_info (list): A list of dictionaries containing column information.
            Each dictionary should have the following keys:
                'name1' (str): The name of the column in df1.
                'name2' (str): The name of the column in df2.
                'ExactCompare' (bool): Whether to perform an exact string comparison.
                'method' (str): The string comparison method to use if 'ExactCompare' is False.

    Returns:
        pandas.DataFrame: A DataFrame containing potential matches and their similarity scores.

    This function uses the record linkage library (rl) to perform a fuzzy matching between
    the two DataFrames based on the provided column information. It calculates similarity
    scores between columns in df1 and df2 using either an exact string comparison or a
    specified string comparison method (e.g., 'jarowinkler', 'levenshtein').
    """
    indexer = rl.Index()
    indexer.full()  # Consider all possible pairs
    candidates = indexer.index(df1, df2)
    compare_cl = rl.Compare()

    for col_dict in col_info:
        if col_dict["ExactCompare"]:
            compare_cl.exact(
                col_dict["name1"],
                col_dict["name2"],
                label="Exact_"
                + col_dict["name1"]
                + ", "
                + col_dict["name2"]
                + "_similarity",
            )
        else:
            compare_cl.string(
                col_dict["name1"],
                col_dict["name2"],
                method=col_dict["method"],
                label=col_dict["name1"] + ", " + col_dict["name2"] + "_similarity",
            )

    potential_matches = compare_cl.compute(candidates, df1, df2)
    return potential_matches


def get_top_matches(
    output_scores, df1, df2, weights, overall_similarity_threshold=0.45, top_n=3
) -> pd.DataFrame:
    """
    Filter and select the top matching rows from a DataFrame of similarity scores.

    Args:
        output_scores (pandas.DataFrame): A DataFrame containing similarity scores for each column.
        df1 (pandas.DataFrame): The first DataFrame with original data (after errors were introduced).
        df2 (pandas.DataFrame): The second DataFrame with original data (after errors were introduced).
        weights (list): A list of weights to be applied to the similarity scores.
        overall_similarity_threshold (float, optional): The minimum overall similarity score required for a row to be included. Default is 0.45.
        top_n (int, optional): The number of top matches to select for each group. Default is 3.

    Returns:
        pandas.DataFrame: A DataFrame containing the top `top_n` matches for each group, sorted by the overall similarity score in descending order.

    This function calculates an overall similarity score for each row in the `output_scores` DataFrame by taking a weighted sum of the individual similarity scores. It then filters the rows to include only those with an overall similarity score above the specified `overall_similarity_threshold`. Finally, it groups the rows and selects the top `top_n` rows within each group based on the overall similarity score.
    """
    output_scores_overall = output_scores.copy()
    output_scores_overall["overall_similarity"] = output_scores.iloc[
        :, : len(weights)
    ].dot(weights)
    scores_filtered_threshold = output_scores_overall[
        output_scores_overall["overall_similarity"] > overall_similarity_threshold
    ]

    top_matches = scores_filtered_threshold.reset_index()
    top_matches = top_matches.merge(
        df1.reset_index(), left_on="level_0", right_index=True
    )
    top_matches = top_matches.merge(
        df2.reset_index(), left_on="level_1", right_index=True, suffixes=("_1", "_2")
    )
    top_matches = top_matches.sort_values(
        ["level_0", "overall_similarity"], ascending=[True, False]
    )
    top_matches = top_matches.groupby("level_0").head(top_n)

    return top_matches
