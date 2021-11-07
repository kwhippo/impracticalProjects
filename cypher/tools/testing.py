from cypher.cipher import Key, Cipher
from pprint import pprint

k = Key()
k.key_variable = None
# k.validate()

c = Cipher(plaintext='testing')
try:
    c.encrypt()
except Exception as e:
    print(e)
