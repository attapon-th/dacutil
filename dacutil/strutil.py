from pandas import DataFrame


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


def df_remove_char_error(
    df: DataFrame,
    regex_remove=r"\x00",
    columns: list[str] | None = None,
) -> DataFrame:
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
