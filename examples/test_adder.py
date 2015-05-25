from pleasant.base import Atom
from pleasant.util import *
from pleasant.verilog.lang import *

def make_adder(n):
    a, b, c_in = Atom("a"), Atom("b"), Atom("c_in")
    s = bitxor(bitxor(a, b), c_in)
    c_out = bitor(bitand(a,b),bitand(bitxor(a,b),c_in))
    
    adder = []

    prev = None
    for i in range(n):
        an, bn, c_inn = Atom("a"+str(i)), Atom("b"+str(i)), Atom("c_in"+str(i))
        if prev:
            prev.link(c_inn)
        f = curry(multireplace, {a:an, b:bn, c_in:c_inn})
        sn = apply(f, s)
        c_outn = apply(f, c_out)

        prev = c_outn
        adder += [group(sn,c_outn)]

    return adder


add4 = make_adder(4)

for adder in add4:
    print(set().union(*[obj.atoms() for obj in network(adder)]))
