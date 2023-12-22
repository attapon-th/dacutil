import pandas as pd
from pandas import DataFrame


def check_mod11(cid: str) -> bool:
    """
    Validate Thai citizen ID is Mod11

    เช็คเลขบัตรประชาชน 13 หลัก ตาม Mod11

    Args:
        cid (str): Thai citizen ID

    Returns:
        bool: True if valid else False
    """
    if (
        pd.isna(cid) or len(cid) != 13 or not cid.isnumeric()
    ):  # ถ้า pid ไม่ใช่ 13 ให้คืนค่า False
        return False

    cid12: str = cid[0:12]  # ตัวเลขหลักที่ 1 - 12 ของบัตรประชาชน
    cid13: str = cid[12]  # ตัวเลขหลักที่ 13 ของบัตรประชาชน
    sum_num: int = 0  # ผลรวม
    for i, num in enumerate(cid12):  # วนลูปเช็คว่า pid มีตัวอักษรอยู่ในตำแหน่งไหน
        sum_num += int(num) * (13 - i)  # นำตัวเลขที่เจอมาคูณกับ 13 - i

    digit13: int = sum_num % 11  # หาเศษจากผลรวมที่ได้จากการคูณด้วย 11
    digit13 = (11 - digit13) % 10
    return int(cid13) == digit13
