from subkey import SubKey
from sub_params import ip_sub, ip_sub_inv, expansion, sbox, p_out
from utils import print_list, to_bit_array, substitute, list_xor, int_to_bit_array, bit_array_to_bytes


round_count = 16


class DES:
    def __init__(self, key: bytes) -> None:
        self.__enc_keys = SubKey(key)


    def encrypt(self, plain: bytes):
        self.__bit_array = to_bit_array(plain)
        self.__bit_array = substitute(self.__bit_array, ip_sub)

        for round in range(round_count):
            l, r = self.__bit_array[:32], self.__bit_array[32:]
            key = self.__enc_keys.get_i_key(round)
            expanded = substitute(r, expansion)
            xor_k_e = list_xor(key, expanded)
            sbox_subed = []
            for i in range(8):
                six_bits = xor_k_e[i*6:(i+1)*6]
                sb_row = six_bits[5] + (six_bits[0] << 1)
                sb_col = (six_bits[1] << 3) + (six_bits[2] << 2) + (six_bits[3] << 1) + six_bits[4]
                res = int_to_bit_array(sbox[i][sb_row][sb_col], 4)
                sbox_subed += res
            res = substitute(sbox_subed, p_out)
            xored = list_xor(l, res)
            print(xored)
            self.__bit_array = r + xored if round < round_count - 1 else xored + r

        self.__bit_array = substitute(self.__bit_array, ip_sub_inv)

        return bit_array_to_bytes(self.__bit_array)

    # [debug]
    def print_current(self):
        print_list(self.__bit_array)


if __name__ == "__main__":
    # print_list(ip_sub)
    # print_list(ip_sub_inv)
    test_plain = b"\x01\x23\x45\x67\x89\xab\xcd\xef"
    test_key = b"\x13\x34\x57\x79\x9b\xbc\xdf\xf1"
    des = DES(test_key)
    ct = des.encrypt(test_plain)
    print(ct)
