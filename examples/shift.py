from pleasant.base import Atom
from pleasant.util import *
from pleasant.misc import *
from pleasant.verilog.lang import *


def make_shift(width,depth):
    sreg = [bundle(*[Atom("d_in"+str(i)) for i in range(width)])]
    for d in range(depth):
        sreg += [reg(bundle(*[Atom("r"+str(i)) for i in range(width)]))]

    shift = []
    for d in range(depth):
        shift += [let(sreg[d+1],sreg[d])]

    return sync(*shift)
