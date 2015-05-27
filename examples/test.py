#!idle -r

from pleasant.base import Atom
from pleasant.exceptions import RuleViolation
from pleasant.util import *
from pleasant.misc import *
from pleasant.verilog.lang import *
from pleasant.verilog.generate import *

import shift
import adder

x, y, z = Atom("x"), Atom("y"), Atom("z")

m_shift = Module("shift4x4", shift.make_shift(4,4))
add8 = adder.make_adder(8)
