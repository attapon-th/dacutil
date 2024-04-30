import pandas as pd
from pandas import DataFrame

# constants for Thai citizen ID
CID_NONE: int = 0
CID_LENGTH13: int = 1
CID_NUMBER: int = 2
CID_THAI: int = 9


def check_mod11(cid: str) -> bool:
    """
    Validate Thai citizen ID is Mod11

    เช็คเลขบัตรประชาชน 13 หลัก ตาม Mod11

    Args:
        cid (str): Thai citizen ID

    Returns:
        bool: True if valid else False
    """
    if pd.isna(cid) or len(cid) != 13 or not cid.isnumeric():  # ถ้า pid ไม่ใช่ 13 ให้คืนค่า False
        return False
    cid0 = int(cid[0])
    cid1 = int(cid[1])
    if cid0 == 0:  # ตัวเลขหลักที่ 0 ของบัตรประชาชน ไม่มีค่าเป็น 0
        return False
    if cid1 == 0:  # ตัวเลขหลักที่ 1 ของบัตรประชาชน
        return False

    cid12: str = cid[0:12]  # ตัวเลขหลักที่ 1 - 12 ของบัตรประชาชน
    cid13: str = cid[12]  # ตัวเลขหลักที่ 13 ของบัตรประชาชน
    sum_num: int = 0  # ผลรวม
    for i, num in enumerate(cid12):  # วนลูปเช็คว่า pid มีตัวอักษรอยู่ในตำแหน่งไหน
        sum_num += int(num) * (13 - i)  # นำตัวเลขที่เจอมาคูณกับ 13 - i

    digit13: int = sum_num % 11  # หาเศษจากผลรวมที่ได้จากการคูณด้วย 11
    digit13 = (11 - digit13) % 10
    return int(cid13) == digit13


def verify_thaicid(cid: str) -> int:
    """
    Determines the type of Thai citizen ID based on the input string.

    Args:
        cid (str): The Thai citizen ID to be checked.

    Returns:
        int: The type of the Thai citizen ID. Possible return values are:

            - `CID_THAI`(9): If the ID is a valid Thai citizen ID.

            - `CID_NUMBER`(2): If the ID is a numeric string of length 13.

            - `CID_LENGTH13`(1): If the ID is a string of length 13.

            - `CID_NONE`(0): If the ID is not a valid Thai citizen ID.
    """
    if not isinstance(cid, str):
        cid = str(cid)

    if len(cid) == 13 and check_mod11(cid):
        return CID_THAI
    if len(cid) == 13 and cid.isnumeric():
        return CID_NUMBER
    if len(cid) == 13:
        return CID_LENGTH13
    return CID_NONE
