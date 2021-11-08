from cypher.vigenere import VigenereCipher
from pprint import pprint

c = VigenereCipher(plaintext='testing')
c.set_key()
c.print()
c.encrypt()
