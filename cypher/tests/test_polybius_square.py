import unittest
from cypher.polybius_square import PolybiusSquareCipher, validate_cipher_alphabet, validate_xy_key
from cypher.exceptions import KeyValidationError


class PolybiusSquareTest(unittest.TestCase):
    def test_validate_valid_cipher_alphabet(self):
        cipher_alphabet = 'XWPTZIQDSCLUAEMGYNBROVFKH'
        validate_cipher_alphabet(cipher_alphabet)
        self.assertTrue(True)

    def test_validate_invalid_cipher_alphabet(self):
        cipher_alphabet = 'XWPTZIJQDSCLUAEMGYNBROVFKH'
        with self.assertRaises(KeyValidationError):
            validate_cipher_alphabet(cipher_alphabet)

    def test_validate_nonstring_cipher_alphabet(self):
        cipher_alphabet = 1
        with self.assertRaises(KeyValidationError):
            validate_cipher_alphabet(cipher_alphabet)

    def test_validate_valid_xy_key(self):
        xy_key = 'ABCDE'
        validate_xy_key(xy_key)
        self.assertTrue(True)

    def test_validate_long_xy_key(self):
        xy_key = 'ABCDEF'
        with self.assertRaises(KeyValidationError):
            validate_xy_key(xy_key)

    def test_validate_short_xy_key(self):
        xy_key = 'ABCD'
        with self.assertRaises(KeyValidationError):
            validate_xy_key(xy_key)

    def test_validate_nonstring_xy_key(self):
        xy_key = 5
        with self.assertRaises(KeyValidationError):
            validate_xy_key(xy_key)

    def test_encrypt(self):
        c = PolybiusSquareCipher()
        c.set_key()
        c.key.cipher_alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        c.key.x_key = c.key.y_key = 'ABCDE'
        c.plaintext = "All the world's a stage & all the men and women merely players;"
        test_ciphertext = 'AACACADDBCAEEBCDDBCAADDCAADCDDAABBAEAACACADDBCAECBAECCAACCADEBCDCBAE' \
                          'CCCBAEDBAECAEDCECAAAEDAEDBDC'
        c.encrypt()
        self.assertEqual(c.ciphertext, test_ciphertext)

    def test_decrypt(self):
        c = PolybiusSquareCipher()
        c.set_key()
        c.key.cipher_alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        c.key.x_key = c.key.y_key = 'ABCDE'
        c.ciphertext = 'AACACADDBCAEEBCDDBCAADDCAADCDDAABBAEAACACADDBCAECBAECCAACCADEBCDCBAE' \
                       'CCCBAEDBAECAEDCECAAAEDAEDBDC'
        test_plaintext = 'ALLTHEWORLDSASTAGEALLTHEMENANDWOMENMERELYPLAYERS'
        c.decrypt()
        self.assertEqual(c.plaintext, test_plaintext)


if __name__ == '__main__':
    unittest.main()
