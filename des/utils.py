from typing import List, Union


def to_bit_array(bs: bytes) -> List[int]:
    ret = []
    for row, b in enumerate(bs):
        for _ in range(8):
            ret.append(0)
        for i in range(8):
            ba_idx = row * 8 + (7 - i)
            ret[ba_idx] = b >> i & 1

    return ret


def int_to_bit_array(n: int, align: Union[int, None]=None) -> List[int]:
    if align is not None:
        ret = [0 for _ in range(align)]
    else:
        l = n.bit_length()
        ret = [0 for _ in range(l)]

    idx = len(ret) - 1
    while n:
        ret[idx] = n & 1
        n >>= 1
        idx -= 1

    return ret


def bits_to_byte(bits: List[int]) -> bytes:
    ret = 0
    for b in bits:
        ret <<= 1
        ret |= b

    return ret.to_bytes(1, "little")


def bit_array_to_bytes(ba: List[int]) -> bytes:
    ret = b""
    bytes_cnt = len(ba) // 8
    for i in range(bytes_cnt):
        byte = bits_to_byte(ba[8*i:8*(i+1)])
        ret += byte

    return ret


def print_list(l: List, cnt_in_row: int = 8, delim: str = " "):
    size = len(l)
    row_cnt = size // cnt_in_row
    if size % cnt_in_row != 0:
        row_cnt += 1
    for row in range(row_cnt):
        dump_str = ""
        for col in range(cnt_in_row):
            idx = row * cnt_in_row + col
            if idx == size:
                break
            elm = l[idx]
            dump_str += str(elm) + delim
        print(dump_str)


def substitute(target, sub_func):
    ret = []
    for idx in sub_func:
        ret.append(target[idx])

    return ret


def list_xor(l1, l2):
    ret = []
    for idx in range(len(l1)):
        ret.append(l1[idx] ^ l2[idx])

    return ret
