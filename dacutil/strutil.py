from pandas import DataFrame


def df_strip(df: DataFrame) -> DataFrame:
    """
    Trim space in string column

    ตัดช่องว่าง หน้าหลังของคอลัมน์



    Args:
        df (DataFrame): DataFrame

    Returns:
        df (DataFrame): DataFrame
    """
    cols = df.select_dtypes(["string[pyarrow]", "string", "object"]).columns
    df[cols] = df[cols].apply(lambda x: x.str.strip())
    return df
