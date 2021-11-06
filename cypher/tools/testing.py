from cypher.route_cipher import RouteKey, recommended_grid
from cypher.tools.utilities import get_factors
from pprint import pprint

tl = 21

pprint(get_factors(tl))
print(recommended_grid(tl))

kl = [-1, 3, -2, 4]
ks = '-1 3 -2 4'
cols = 4


k = RouteKey()
k.calculate(key_list=kl)
k.print()

k.calculate(key_string=ks)
k.print()

k.calculate(columns=cols)
k.print()

k.calculate(best_fit_length=tl)
k.print()
