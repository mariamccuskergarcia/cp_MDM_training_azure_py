from faker import Faker as fkr
import pandas as pd
import random
import string
from datetime import datetime, timedelta
import streamlit as st


def set_num_records() -> None:
    st.session_state["permpage1"]["num_records"] = st.session_state["num_records"]
    return None


def set_uploadcreate() -> None:
    st.session_state["permpage1"]["uploadcreate"] = st.session_state["uploadcreate"]
    return None


def generate_fake_data(num_records) -> pd.DataFrame:
    """
    Generate a pandas DataFrame with fake data for a specified number of records.

    Args:
        num_records (int): The number of fake records to generate.

    Returns:
        pd.DataFrame: A DataFrame containing fake names, addresses, phone numbers,
                      dates, timestamps, and other generic columns like email, job, etc.
                      The columns are: 'name', 'address', 'phone', 'date', 'timestamp',
                      'email', 'job', etc.

    The function uses the `faker` library to generate realistic fake data for names,
    addresses, phone numbers, dates, emails, job titles, etc. The dates and timestamps
    are randomly generated within the past 10 years from the current date. Phone numbers
    and addresses may be outdated or invalid.
    """

    fake = fkr()

    names = []
    addresses = []
    phone_numbers = []
    dates = []
    timestamps = []
    emails = []
    jobs = []

    for _ in range(num_records):
        names.append(fake.name())
        addresses.append(fake.address())
        phone_numbers.append(fake.phone_number())
        dates.append(fake.date_between(start_date="-10y", end_date=datetime.today()))
        timestamps.append(
            fake.date_time_between(start_date="-10y", end_date=datetime.today())
        )
        emails.append(fake.email())
        jobs.append(fake.job())

    df = pd.DataFrame(
        {
            "name": names,
            "address": addresses,
            "phone": phone_numbers,
            "date": dates,
            "timestamp": timestamps,
            "email": emails,
            "job": jobs,
        }
    )

    df["date"] = df["date"].astype(str)
    df["timestamp"] = df["timestamp"].astype(str)

    # Introduce outdated or invalid phone numbers and addresses
    df["phone"] = df["phone"].apply(
        lambda x: x.replace(x[-4:], "1234") if random.random() < 0.2 else x
    )
    df["address"] = df["address"].apply(
        lambda x: fake.address() if random.random() < 0.1 else x
    )

    return df


def introduce_spelling_errors(df, error_rate=0.05, columns=None) -> pd.DataFrame:
    """
    Introduce random spelling errors in the specified columns of a pandas DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        error_rate (float, optional): The fraction of characters to be replaced with a random alphabet character.
            Default is 0.05 (5% of characters).
        columns (list, optional): The list of column names to introduce errors in. If None, all
            object (string) columns in the DataFrame will be used.

    Returns:
        pd.DataFrame: A new DataFrame with spelling errors introduced in the specified columns.

    The function iterates over the specified columns and randomly replaces a fraction of characters (based on
    the provided error rate) in each string value with a random alphabet character. If no columns are specified,
    it will introduce errors in all object (string) columns of the input DataFrame.
    """
    if columns is None:
        columns = df.select_dtypes(include="object").columns
        columns = columns.drop(["date", "timestamp"], errors="ignore")

    for col in columns:
        for i in range(len(df)):
            original_value = df.loc[i, col]
            new_value = ""
            for char in original_value:
                if random.random() < error_rate:
                    new_value += random.choice(string.ascii_letters)
                else:
                    new_value += char
            df.loc[i, col] = new_value

    return df


def introduce_date_inconsistencies(
    df, col="date", inconsistency_rate=0.2
) -> pd.DataFrame:
    """
    Introduce format inconsistencies in the 'date' column of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str, optional): The name of the date column. Default is 'date'.
        inconsistency_rate (float, optional): The probability of introducing an inconsistency in a date value.
            Default is 0.2 (20% chance).

    Returns:
        pd.DataFrame: A new DataFrame with format inconsistencies introduced in the date column.
    """
    for i in range(len(df)):
        if random.random() < inconsistency_rate:
            date_str = df.loc[i, col]
            try:
                date_dt = pd.to_datetime(date_str)
                if "/" in date_str:
                    df.loc[i, col] = date_dt.strftime("%Y-%m-%d")
                elif "-" in date_str:
                    df.loc[i, col] = date_dt.strftime("%Y.%m.%d")
            except pd.errors.ParserError:
                # Skip the row if parsing fails
                continue
    return df


def introduce_phone_inconsistencies(
    df, col="phone", inconsistency_rate=0.3, variation_rate=0.4
) -> pd.DataFrame:
    """
    Introduce format inconsistencies in the 'phone' column of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str, optional): The name of the phone column. Default is 'phone'.
        inconsistency_rate (float, optional): The probability of introducing an inconsistency in a phone value.
            Default is 0.3 (30% chance).
        variation_rate (float, optional): The probability of adding variations (e.g., spaces) to the phone value.
            Default is 0.4 (40% chance).

    Returns:
        pd.DataFrame: A new DataFrame with format inconsistencies introduced in the phone column.
    """
    for i in range(len(df)):
        if random.random() < inconsistency_rate:
            phone_str = df.loc[i, col]
            if random.random() < variation_rate:  # Add variations
                phone_str = phone_str[:3] + " " + phone_str[3:]
            else:  # Remove variations
                phone_str = phone_str.replace(" ", "").replace("-", "")
            df.loc[i, col] = phone_str
    return df


def introduce_address_inconsistencies(
    df, col="address", capitalization_rate=0.15, comma_rate=0.15, abbreviation_rate=0.15
) -> pd.DataFrame:
    """
    Introduce format inconsistencies in the 'address' column of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str, optional): The name of the address column. Default is 'address'.
        capitalization_rate (float, optional): The probability of changing the capitalization of the address value.
            Default is 0.15 (15% chance).
        comma_rate (float, optional): The probability of adding or removing commas from the address value.
            Default is 0.15 (15% chance).
        abbreviation_rate (float, optional): The probability of abbreviating or unabbreviating street names.
            Default is 0.15 (15% chance).

    Returns:
        pd.DataFrame: A new DataFrame with format inconsistencies introduced in the address column.
    """
    for i in range(len(df)):
        address_str = df.loc[i, col]

        # Change capitalization
        if random.random() < capitalization_rate:
            df.loc[i, col] = (
                address_str.upper() if address_str.islower() else address_str.lower()
            )

        # Add/remove commas
        if random.random() < comma_rate:
            df.loc[i, col] = (
                address_str.replace(",", "")
                if "," in address_str
                else address_str + ","
            )

        # Abbreviation variations
        if random.random() < abbreviation_rate:
            df.loc[i, col] = (
                address_str.replace("Street", "St.")
                if "Street" in address_str
                else address_str.replace("St.", "Street")
            )
    return df


def introduce_name_inconsistencies(
    df, col="name", abbreviation_rate=0.2, title_rate=0.3
) -> pd.DataFrame:
    """
    Introduce format inconsistencies in the 'name' column of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str, optional): The name of the name column. Default is 'name'.
        abbreviation_rate (float, optional): The probability of abbreviating a first name.
            Default is 0.2 (20% chance).
        title_rate (float, optional): The probability of adding a title to the name.
            Default is 0.3 (30% chance).

    Returns:
        pd.DataFrame: A new DataFrame with format inconsistencies introduced in the name column.
    """
    for i in range(len(df)):
        name = df.loc[i, col]
        # Abbreviate names
        if random.random() < abbreviation_rate and len(name.split()) > 1:
            first_initial = name.split()[0][0] + "."
            df.loc[i, col] = first_initial + " " + name.split()[-1]

        # Add titles
        if random.random() < title_rate:
            titles = ["Mr.", "Mrs.", "Dr.", "Prof."]
            df.loc[i, col] = random.choice(titles) + " " + name
    return df


def introduce_timestamp_inconsistencies(
    df, col="timestamp", inconsistency_rate=0.1
) -> pd.DataFrame:
    """
    Introduce inconsistencies in the 'timestamp' column of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col (str, optional): The name of the timestamp column. Default is 'timestamp'.
        inconsistency_rate (float, optional): The probability of introducing an inconsistency in a timestamp value.
            Default is 0.1 (10% chance).

    Returns:
        pd.DataFrame: A new DataFrame with inconsistencies introduced in the timestamp column.
    """
    for i in range(len(df)):
        if random.random() < inconsistency_rate:
            timestamp_str = df.loc[i, col]
            try:
                timestamp_dt = pd.to_datetime(timestamp_str)
                offset_days = random.randint(
                    -365, 365
                )  # Offset between -1 year and +1 year
                new_timestamp = timestamp_dt + timedelta(days=offset_days)
                df.loc[i, col] = new_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            except pd.errors.ParserError:
                # Skip the row if parsing fails
                continue
    return df


def introduce_format_inconsistencies(
    df,
    columns=None,
    date_inconsistency_rate=0.2,
    phone_inconsistency_rate=0.3,
    phone_variation_rate=0.4,
    address_capitalization_rate=0.15,
    address_comma_rate=0.15,
    address_abbreviation_rate=0.15,
    name_abbreviation_rate=0.2,
    name_title_rate=0.3,
    timestamp_inconsistency_rate=0.1,
) -> pd.DataFrame:
    """
    Introduce format inconsistencies in the specified columns of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (list, optional): The list of column names to introduce inconsistencies in.
            If None, all relevant columns ('date', 'phone', 'address', 'name', 'timestamp') will be used.
        date_inconsistency_rate (float, optional): The probability of introducing an inconsistency in a date value.
            Default is 0.2 (20% chance).
        phone_inconsistency_rate (float, optional): The probability of introducing an inconsistency in a phone value.
            Default is 0.3 (30% chance).
        phone_variation_rate (float, optional): The probability of adding variations (e.g., spaces) to the phone value.
            Default is 0.4 (40% chance).
        address_capitalization_rate (float, optional): The probability of changing the capitalization of an address value.
            Default is 0.15 (15% chance).
        address_comma_rate (float, optional): The probability of adding or removing commas from an address value.
            Default is 0.15 (15% chance).
        address_abbreviation_rate (float, optional): The probability of abbreviating or unabbreviating street names.
            Default is 0.15 (15% chance).
        name_abbreviation_rate (float, optional): The probability of abbreviating a first name.
            Default is 0.2 (20% chance).
        name_title_rate (float, optional): The probability of adding a title to a name.
            Default is 0.3 (30% chance).
        timestamp_inconsistency_rate (float, optional): The probability of introducing an inconsistency in a timestamp value.
            Default is 0.1 (10% chance).

    Returns:
        pd.DataFrame: A new DataFrame with format inconsistencies introduced in the specified columns.
    """
    if columns is None:
        columns = []
        if "date" in df.columns:
            columns.append("date")
        if "phone" in df.columns:
            columns.append("phone")
        if "address" in df.columns:
            columns.append("address")
        if "name" in df.columns:
            columns.append("name")
        if "timestamp" in df.columns:
            columns.append("timestamp")

    for col in columns:
        if col == "date":
            df = introduce_date_inconsistencies(df, col, date_inconsistency_rate)
        elif col == "phone":
            df = introduce_phone_inconsistencies(
                df, col, phone_inconsistency_rate, phone_variation_rate
            )
        elif col == "address":
            df = introduce_address_inconsistencies(
                df,
                col,
                address_capitalization_rate,
                address_comma_rate,
                address_abbreviation_rate,
            )
        elif col == "name":
            df = introduce_name_inconsistencies(
                df, col, name_abbreviation_rate, name_title_rate
            )
        elif col == "timestamp":
            df = introduce_timestamp_inconsistencies(
                df, col, timestamp_inconsistency_rate
            )

    return df
