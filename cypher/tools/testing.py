from cypher.caesar import CaesarKey, CaesarCipher
from cypher.caesar_keyword import CaesarKeywordKey, CaesarKeywordCipher
from cypher.caesar_keyword import create_caesar_keyword_keys
from pprint import pprint

ck = CaesarKey()
ck.validate()
ck.print()

pt = 'Hide the gold in the stump'

cc = CaesarCipher(plaintext=pt, key=ck)
cc.encrypt()
print(cc.ciphertext)
cc.decrypt()
print(cc.plaintext)

ckwk = CaesarKeywordKey()
ckwk.validate()
ckwk.print()

ckwc = CaesarKeywordCipher(plaintext=pt, key=ckwk)
ckwc.encrypt()
print(ckwc.ciphertext)
ckwc.decrypt()
print(ckwc.plaintext)
