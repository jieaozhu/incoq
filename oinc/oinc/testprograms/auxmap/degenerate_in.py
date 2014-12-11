# Degenerate auxiliary maps -- all bound or all unbound.
# Not practical for writing readable code, but an interesting edge
# case that is sometimes generated by automatic transformations.

from runtimelib import *

R = Set()

for x, y in [(1, 2), (1, 3), (2, 3), (1, 4)]:
    R.add((x, y))

R.remove((1, 4))

print(sorted(setmatch(R, 'bb', (1, 2))))
print(sorted(setmatch(R, 'uu', ())))