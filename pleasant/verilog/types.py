## Copyright 2015 Noah Santer
##
## This file is part of Pleasant.
##
## Pleasant is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Pleasant is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Pleasant.  If not, see <http://www.gnu.org/licenses/>

import pleasant.base as _base

# types
atom_t = _base.atom_t
constant_t = _base.Type("constant_t")
logic_t = _base.Type("logic_t")
expr_t = _base.Type("expr_t")
reg_t = _base.Type("reg_t")
wire_t = _base.Type("wire_t")
bundle_t = _base.Type("bundle_t")
array_t = _base.Type("array_t")
syncable_t = _base.Type("syncable_t")
synced_t = _base.Type("syncable_t")
clock_t = _base.Type("clock_t")

# link types
soft_link_t = _base.Type("soft_link_t") # continuous links
hard_link_t = _base.Type("hard_link_t") # synchronous links
