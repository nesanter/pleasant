from pleasant.base import Atom
from pleasant.util import *
from pleasant.misc import *
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
        sn.set_alias("q"+str(i))
        c_outn = apply(f, c_out)

        prev = c_outn
        adder += [(sn,c_outn)]

    C_IN = adder[0][0][1]
    A = bundle(*[add[0][0][0] for add in adder])
    B = bundle(*[add[0][0][1] for add in adder])
    Q = bundle(*[add[0] for add in adder])
    C_OUT = adder[-1][1]
    C_OUT.set_alias("c_out")

    return (A,B,C_IN,Q,C_OUT)

add4 = make_adder(4)

#for adder in add4:
#    print(set().union(*[obj.atoms() for obj in network(adder)]))
