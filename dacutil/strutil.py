from pandas import DataFrame


# Character X00 is error character
CHAR_X00 = r"\x00"
CHAR_TAB = r"\t"
CHAR_RET = r"\r"
CHAR_NEWLINE = r"\n"


def df_strip(df: DataFrame, columns: list[str] | None = None) -> DataFrame:
    """
    Trim space in string column

    ตัดช่องว่าง หน้าหลังของคอลัมน์

    Args:
        df (DataFrame): DataFrame

    Returns:
        df (DataFrame): DataFrame
    """
    if columns is None:
        columns = df.select_dtypes(["string"]).columns.tolist()
    for col in columns:
        if df[col].empty or not hasattr(df[col], "str"):
            continue
        df[col] = df[col].str.strip()
    return df


def df_remove_char_error(df: DataFrame, regex_remove=CHAR_X00, columns: list[str] | None = None) -> DataFrame:
    """
    Removes a specified character or sequence of characters from string columns in the DataFrame.

    Parameters:
        df (DataFrame): The input DataFrame.
        regex_remove (str, optional): The regular expression pattern to remove. Defaults to "\\x00".
        columns (list[str] | None, optional): The list of columns to apply the regex pattern to. If None, string columns are selected by default. Defaults to None.

    Returns:
        DataFrame: The DataFrame with the specified characters removed from the specified columns.
    """
    if columns is None:
        columns = df.select_dtypes(["string"]).columns.tolist()
    for col in columns:
        if df[col].empty or not hasattr(df[col], "str"):
            continue
        df[col] = df[col].str.replace(regex_remove, "", regex=True)
    return df


def df_replace(df: DataFrame, regex, replace="", columns: list[str] | None = None) -> DataFrame:
    """
    Replaces occurrences of a specified regular expression pattern in string columns of a DataFrame with a given replacement string.

    Parameters:
        df (DataFrame): The input DataFrame.
        regex (str): The regular expression pattern to search for.
        replace (str, optional): The replacement string. Defaults to an empty string.
        columns (list[str] | None, optional): The list of columns to apply the regex pattern to. If None, string columns are selected by default. Defaults to None.

    Returns:
        DataFrame: The DataFrame with the specified occurrences of the regex pattern replaced in the specified columns.
    """
    if columns is None:
        columns = df.select_dtypes(["string"]).columns.tolist()
    for col in columns:
        if df[col].empty or not hasattr(df[col], "str"):
            continue
        df[col] = df[col].str.replace(regex, replace, regex=True)
    return df


def df_fixchar(df: DataFrame) -> DataFrame:
    """
    Removes special characters and replaces them with spaces or tabs in a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.

    Returns:
        DataFrame: The DataFrame with special characters removed and replaced.
    """
    df = df_strip(df)
    df = df_remove_char_error(df)
    df = df_replace(df, regex=f"{CHAR_RET}|{CHAR_NEWLINE}", replace=" ")
    df = df_replace(df, regex=f"{CHAR_TAB}", replace="    ")
    return df
