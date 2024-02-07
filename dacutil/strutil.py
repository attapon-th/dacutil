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
