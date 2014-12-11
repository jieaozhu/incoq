# Some sets in the input program are already relations.

from runtimelib import *

OPTIONS(
    obj_domain = True,
    input_rels = ['N'],
)



N = Set()
for i in range(1, 5):
    N.add(i)

s1 = Set()
s2 = Set()
for i in N:
    o = Obj()
    o.i = i
    if i % 2:
        s1.add(o)
    else:
        s2.add(o)

QUERYOPTIONS(
    '{o.i for o in s if o.i in N}',
    params = ['s'],
    uset_mode = 'none',
    impl = 'inc',
)
s = s1
print(sorted({o.i for o in s if o.i in N}))
s = s2
print(sorted({o.i for o in s if o.i in N}))
