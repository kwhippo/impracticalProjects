from cypher.caesar import CaesarKey
from cypher.substitution import SubstitutionKey
from pprint import pprint

k = CaesarKey()
k.calculate(numeric_key=1)
k.print()
k.calculate(ab_key='AB')
k.print()
k.calculate(a_key='B')
k.print()
k.calculate(alpha_key='BCDEFGHIJKLMNOPQRSTUVWXYZA')
k.print()
print(type(k) == SubstitutionKey)

pt = 'Hide the gold in the stump'


