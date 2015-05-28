from pleasant.base import Atom
from pleasant.util import *
from pleasant.misc import *
from pleasant.verilog.lang import *
from pleasant.verilog import generate


def make_shift(width,depth,set_io=True):
    sreg = [bundle(*[Atom("d_in"+str(i)) for i in range(width)])]

    for d in range(depth):
        sreg += [reg(bundle(*[Atom("r"+str(i)) for i in range(width)]))]

    if set_io:
        generate.set_input(sreg[0])
        generate.set_output(sreg[-1])

    shift = []
    for d in range(depth):
        shift += [let(sreg[d+1],sreg[d])]

    return sync(*shift)
