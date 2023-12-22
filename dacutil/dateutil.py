from datetime import datetime, date
from typing import Union, Literal
import pyarrow as pa
import pandas as pd


def datediff(
    start_dt: Union[pa.Array, pa.Scalar, pd.Series, date, datetime],
    ended_dt: Union[pa.Array, pa.Scalar, pd.Series, date, datetime],
    scalar: Literal["Y", "M", "D", "h", "m", "s", "ms"] = "Y",
) -> pd.Series:
    """
    Calculate the difference between two dates/timestamps and return the result as a pandas Series.

    Parameters:
        start_dt (Union[pa.Array, pa.Scalar, pd.Series, date, datetime]): The start date/timestamp.
        ended_dt (Union[pa.Array, pa.Scalar, pd.Series, date, datetime]): The end date/timestamp.
        scalar (Literal["Y", "M", "D", "h", "m", "s", "ms"]): The unit of the difference. Defaults to "Y".

    Returns:
        pd.Series: The calculated difference between the start and end dates/timestamps.
    """
    pa_type = pa.timestamp("ns")

    # convert to type pyarrow
    fr_dt: Union[pa.Array, pa.Scalar]
    if isinstance(start_dt, pd.Series):
        fr_dt = pa.array(pa.array(start_dt), type=pa_type)
    elif isinstance(start_dt, datetime):
        fr_dt = pa.scalar(start_dt, type=pa_type)
    elif isinstance(start_dt, date):
        fr_dt = pa.scalar(datetime.combine(start_dt, datetime.min.time()), type=pa_type)
    elif isinstance(start_dt, pa.Array) or isinstance(start_dt, pa.Scalar):
        fr_dt = start_dt
    else:
        return pd.Series()

    to_dt: Union[pa.Array, pa.Scalar]
    if isinstance(ended_dt, pd.Series):
        to_dt = pa.array(pa.array(ended_dt), type=pa_type)
    elif isinstance(ended_dt, datetime):
        to_dt = pa.scalar(ended_dt, type=pa_type)
    elif isinstance(ended_dt, date):
        to_dt = pa.scalar(datetime.combine(ended_dt, datetime.min.time()), type=pa_type)
    elif isinstance(ended_dt, pa.Array) or isinstance(ended_dt, pa.Scalar):
        to_dt = ended_dt
    else:
        return pd.Series()

    sr: pa.Array
    if scalar == "Y":
        sr = pa.compute.years_between(fr_dt, to_dt)
    elif scalar == "M":
        sr = pa.compute.months_between(fr_dt, to_dt)
    elif scalar == "D":
        sr = pa.compute.days_between(fr_dt, to_dt)
    elif scalar == "W":
        sr = pa.compute.weeks_between(fr_dt, to_dt)
    elif scalar == "h":
        sr = pa.compute.hours_between(fr_dt, to_dt)
    elif scalar == "m":
        sr = pa.compute.minutes_between(fr_dt, to_dt)
    elif scalar == "s":
        sr = pa.compute.seconds_between(fr_dt, to_dt)
    elif scalar == "ms":
        sr = pa.compute.milliseconds_between(fr_dt, to_dt)
    else:
        return pd.Series()
    return sr.to_pandas(types_mapper=pd.ArrowDtype)
