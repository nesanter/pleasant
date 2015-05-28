from pleasant.base import Atom
from pleasant.util import *
from pleasant.misc import *
from pleasant.verilog.lang import *

def make_simple_state():
    s = bundle(reg(Atom()),reg(Atom()))
    s.set_alias("state")

    d_in = Atom("d_in")
    d_out = reg(Atom("d_out"))

    i = Unbundler(s)

    return sync(
                let(i[0], bitxor(d_in, i[0])),
                let(i[1], i[0]),
                let(d_out, bitxor(d_in, i[1]))
            )

def make_state_table(inputbits, statebits):
    d_in = bundle(*[Atom("d_in"+str(i)) for i in range(inputbits)], alias="d_in")
    state = reg(bundle(*[Atom("s"+str(i)) for i in range(statebits)], alias="state"))
    mem = make_array(bundle(*[Atom("s"+str(i)) for i in range(statebits)],alias="mem"), 2**(statebits+inputbits))
    print(state.types)
    print(mem.types)
    print(bundle(d_in,state).types)
    print(varindex(mem, bundle(d_in,state)).types)
    return let(state, varindex(mem, bundle(d_in,state)))

