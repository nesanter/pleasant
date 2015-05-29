#!idle -r

from pleasant.base import Atom
from pleasant.exceptions import RuleViolation
from pleasant.util import *
from pleasant.misc import *
from pleasant.verilog.lang import *
from pleasant.verilog.generate import *
from pleasant.verilog.tools import *

import shift
import adder

x, y, z = Atom("x"), Atom("y"), Atom("z")
B = bundle(*[Atom("b"+str(i)) for i in range(8)])
B.set_alias("B")
A = make_array(B, 256)

m_shift = Module(shift.make_shift(4,4), name="shift4x4")
add8 = adder.make_adder(8)
