from unittest import TestCase
from .context import bencode


class TestBencode(TestCase):
    type_str = 'abc'
    bencoded_str = str(len(type_str)).encode() + b':' + type_str.encode()

    type_dict_str = {'key': 'value', 'key2': 23}
    bencoded_dict_str = b'd3:key5:value4:key2i23ee'

    type_list_str = ['a', 'b', 'c', 1, 2, 3]
    bencoded_list_str = b'l1:a1:b1:ci1ei2ei3ee'

    type_byte = b'abc\x99'
    bencoded_bytes = str(len(type_byte)).encode() + b':' + type_byte

    type_int = 1234
    bencoded_int = b'i' + bytes(str(type_int).encode()) + b'e'

    type_dict = {b'key': b'value', b'key2':23}
    bencoded_dict = b'd3:key5:value4:key2i23ee'

    type_list = [b'a', b'b', b'c', 1, 2, 3]
    bencoded_list = b'l1:a1:b1:ci1ei2ei3ee'

    def test_bdecode(self):
        self.assertEqual(bencode.bdecode(self.bencoded_bytes), self.type_byte)
        self.assertRaises(bencode.BTFailure,bencode.bdecode, self.type_str)
        self.assertEqual(bencode.bdecode(self.bencoded_int), self.type_int)
        self.assertEqual(bencode.bdecode(self.bencoded_list), self.type_list)
        self.assertEqual(bencode.bdecode(self.bencoded_dict), self.type_dict)

    def test_bencode(self):
        self.assertEqual(bencode.bencode(self.type_byte), self.bencoded_bytes)
        self.assertEqual(bencode.bencode(self.type_int), self.bencoded_int)
        self.assertEqual(bencode.bencode(self.type_dict), self.bencoded_dict)
        self.assertEqual(bencode.bencode(self.type_list), self.bencoded_list)

    def test_string_handling(self):
        self.assertNotEqual(bencode.bdecode(self.bencoded_str), self.type_str)
        self.assertNotEqual(bencode.bdecode(self.bencoded_dict_str), self.type_dict_str)
        self.assertNotEqual(bencode.bdecode(self.bencoded_list_str), self.type_list_str)

        self.assertEqual(bencode.bencode(self.type_list_str), self.bencoded_list_str)
        self.assertEqual(bencode.bencode(self.type_str), self.bencoded_str)
        self.assertEqual(bencode.bencode(self.type_dict_str), self.bencoded_dict_str)

    def test_roundtrip(self):
        with open('Bencode.py.torrent','rb') as infile:
            test_data = infile.read()
        decoded = bencode.bdecode(test_data)
        encoded = bencode.bencode(decoded)
        self.assertEqual(test_data,encoded)