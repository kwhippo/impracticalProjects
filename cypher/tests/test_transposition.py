import unittest
from cypher.transposition import TranspositionCipher, TranspositionKey


class TranspositionCipherTest(unittest.TestCase):

    def setUp(self):
        self.cipher = TranspositionCipher()
        self.cipher.key = TranspositionKey()
        self.plaintext = "All the world's a stage, And & all the men and women merely players;"
        self.cipher.plaintext = self.plaintext
        route_cipher_text = 'PLANE WOMEN A ALL FUDGEL FISH WORLDS AND EDGE CROSS PLAYERS ' \
                            'AND ALL THE FLOW THICK MERELY STAGE DURING MEN THE'

    def test_calculate_route_from_string_numeric(self):
        route_string = '-4 7 3 -6 1 -5 -2'
        route = [-4, 7, 3, -6, 1, -5, -2]
        key = TranspositionKey()
        key.calculate(route_string=route_string)
        self.assertEqual(key.route, route)

    def test_calculate_route_from_string_keyword(self):
        route_string = 'georgE'
        route = [2, 6, 1, 5, 3, 4]
        key = TranspositionKey()
        key.calculate(route_string=route_string)
        self.assertEqual(key.route, route)

    def test_route_decrypt(self):
        pass


if __name__ == '__main__':
    unittest.main()
