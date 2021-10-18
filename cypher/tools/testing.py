from cypher.playfaircipher import PlayfairCipher, PlayfairKey

k = PlayfairKey()
k.validate()
k.print()

pt = 'Hide the gold in the stump'

c = PlayfairCipher(plaintext=pt, key=k)
c.encrypt()
print(c.ciphertext)
c.decrypt()
print(c.plaintext)


