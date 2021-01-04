from sub_params import pc1, pc2
from utils import to_bit_array, substitute


class SubKey:
    def __init__(self, key: bytes) -> None:
        self.__keys = []
        self.__bit_array = to_bit_array(key)
        res = substitute(self.__bit_array, pc1)
        c, d = res[:28], res[28:]
        for i in range(16):
            if i in [0, 1, 8, 15]:
                c = c[1:] + c[:1]
                d = d[1:] + d[:1]
            else:
                c = c[2:] + c[:2]
                d = d[2:] + d[:2]

            k = substitute(c + d, pc2)
            self.__keys.append(k)

    @property
    def keys(self):
        return self.__keys

    def get_i_key(self, idx):
        return self.__keys[idx]
