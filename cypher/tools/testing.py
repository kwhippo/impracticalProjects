from cypher.caesar import CaesarKey, create_keys
from pprint import pprint

k = CaesarKey()
k.random()
k.validate()
k.print()
a = k.a_key
ab = k.ab_key
alpha = k.alpha_key
n = k.numeric_key
