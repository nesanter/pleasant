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
    C_IN.set_alias("C_IN")
    A = bundle(*[add[0][0][0] for add in adder])
    A.set_alias("A")
    B = bundle(*[add[0][0][1] for add in adder])
    B.set_alias("B")
    Q = bundle(*[add[0] for add in adder])
    Q.set_alias("Q")
    C_OUT = adder[-1][1]
    C_OUT.set_alias("C_OUT")

    return (A,B,C_IN,Q,C_OUT)

add4 = make_adder(4)

#for adder in add4:
#    print(set().union(*[obj.atoms() for obj in network(adder)]))


def make_adder2(n):
    a, b, c_in = Atom("a"), Atom("b"), Atom("c_in")
    s = bitxor(bitxor(a, b), c_in)
    c_out = bitor(bitand(a, b), bitand(bitxor(a, b), c_in))

    A = bundle(*[Atom("a"+str(i)) for i in range(n)])
    B = bundle(*[Atom("b"+str(i)) for i in range(n)])
    ua = Unbundler(A)
    ub = Unbundler(B)

    adder = []
    prev = None
    for i in range(n):
        c_inn = Atom("c_in"+str(i))
        if not prev == None:
            soft_link(prev, c_inn)
        f = curry(multireplace, {a:ua[i], b:ub[i], c_in:c_inn})
        sn = apply(f, s)
        c_outn = apply(f, c_out)
        adder += [(sn, c_outn)]


