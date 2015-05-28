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
import pleasant.misc as _misc
from . import rules as _rules
from . import types as _types
from . import tools as tools
#from . import generate as generate

# transformations
bitand = _base.Transformation(2,
                        name="&",
                        pattern=("(", _base.Glob(1), " & ", _base.Glob(1), ")"),
                        rules=((_rules.body_to_type_r, _rules.r_boolean_tt),
                               (_rules.body_to_none_r, _rules.r_width_same),
                               (_rules.body_to_attributes_r, _rules.r_inherit_width)))
bitor = _base.Transformation(2,
                       name="|",
                       pattern=("(", _base.Glob(1), " | ",_base.Glob(1), ")"),
                       rules=((_rules.body_to_type_r, _rules.r_boolean_tt),
                              (_rules.body_to_none_r, _rules.r_width_same),
                              (_rules.body_to_attributes_r, _rules.r_inherit_width)))
bitxor =_base.Transformation(2,
                        name="^",
                        pattern=("(",_base.Glob(1), " ^ ",_base.Glob(1), ")"),
                        rules=((_rules.body_to_type_r, _rules.r_boolean_tt),
                               (_rules.body_to_none_r, _rules.r_width_same),
                               (_rules.body_to_attributes_r, _rules.r_inherit_width)))

reduceand =_base.Transformation(1,
                           name="r&",
                           pattern=("&",_base.Glob(1)),
                           rules=((_rules.body_to_type_r, _rules.r_boolean_tt),
                                  (_rules.none_to_attributes_r, _rules.gen_const_attribute("bundle_width", 1))))
reduceor =_base.Transformation(1,
                          "r|",
                          pattern=("|",_base.Glob(1)),
                          rules=((_rules.body_to_type_r, _rules.r_boolean_tt),
                                 (_rules.none_to_attributes_r, _rules.gen_const_attribute("bundle_width", 1))))


let = _base.Transformation(2,
                           name="LET",
                           pattern=(_base.Glob(1)," := ",_base.Glob(1)),
                           rules=((_rules.body_to_none_r, lambda *args: (_rules.r_let_check(*args), _rules.r_width_same(*args))),
                                  (_rules.body_to_type_r, _rules.r_let_tt),
                                  (_rules.body_to_none_r, _rules.r_hard_link_left)))

#group =_base.Transformation(0, "GROUP", pattern=("{",_base.Glob(0,sep="; "), "}"))
#groupln =_base.Transformation(0, "GROUP", pattern=("{\n",_base.Glob(0, sep=";\n"), "}"))
#case =_base.Transformation(2, name="CASE", pattern=(Glob(1)," : (",Glob(1),")"))
#switch =_base.Transformation(-1, name="SWITCH", pattern=("switch ",Glob(1), " { ",Glob(0), " }"))

sync = _base.Transformation(0,
                            name="SYNC",
                            pattern=("@",_base.Glob("trigger",default="*"),": ",_base.Glob(0,sep=", "),";"),
                            rules=((_rules.body_to_type_r, _rules.r_sync_tt),
                                   (_rules.attributes_to_none_r, _rules.r_trigger_valid)))

wire =_base.Transformation(1,
                      name="WIRE",
                      pattern=("wire:",_base.Glob(1)),
                      rules=((_rules.body_to_type_r, _rules.r_wire_tt),
                             (_rules.body_to_attributes_r, _rules.r_inherit_width)))
#                             (_rules.none_to_attributes_r, _rules.gen_const_attribute("bundle_width", 1))))
reg =_base.Transformation(1,
                     name="REG",
                     pattern=("reg:",_base.Glob(1)),
                     rules=((_rules.body_to_type_r, _rules.r_reg_tt),
                            (_rules.body_to_attributes_r, _rules.r_inherit_width)))
#                            (_rules.none_to_attributes_r, _rules.gen_const_attribute("bundle_width", 1))))

bundle = _base.Transformation(0,
                              name="BUNDLE",
                              pattern=("{", _base.Glob(0,sep=" "), "}"),
                              rules=((_rules.body_to_type_r, _rules.r_bundle_tt),
                                     (_rules.body_to_attributes_r, _rules.r_bundle_width)))



def slice_printer(index):
    if type(index) == slice:
        pass
    elif type(index) == int:
#        index = slice(index,index+1)
        return "["+str(index)+"]"
    else:
        index = slice(*index)
    s = ""
    if index.start != None:
        s += str(index.start)
    s += ":"
    if index.stop != None:
        s += str(index.stop)
    if index.step != None:
        s += ":"+str(index.step)
    return "["+s+"]"

unbundle = _base.Transformation(1,
                                name="UNBUNDLE",
                                pattern=(_base.Glob(1), _base.Glob("index", default="", transform=slice_printer)),
                                rules=((_rules.body_to_type_r, _rules.r_unbundle_tt),
                                       (_rules.body_to_attributes_r, _rules.r_bundle_width),
                                       (_rules.attributes_to_attributes_r, _rules.r_unbundle_width),
                                       (_rules.attributes_to_remove_type_r, _rules.r_unbundle_tt2)))

def index_printer(index):
    s = ""
    for i in _misc.flatten(index):
        s += "["+str(i)+"]"
    return s

array = _base.Transformation(1,
                             name="ARRAY",
                             pattern=(_base.Glob(1), "#", _base.Glob("array_width")),
                             rules=((_rules.body_to_type_r, _rules.r_array_tt),
                                    (_rules.attributes_to_none_r, _rules.gen_attribute_exists("array_width")),
                                    (_rules.body_to_attributes_r, _rules.r_inherit_width)))

index = _base.Transformation(1,
                             name="INDEX",
                             pattern=(_base.Glob(1), _base.Glob("index", default="", transform=index_printer)),
                             rules=((_rules.body_to_type_r, _rules.r_index_tt),
                                    (_rules.attributes_and_body_to_none_r, _rules.r_index_check),
                                    (_rules.none_to_attributes_r, _rules.gen_const_attribute("array_width", None))))

varindex = _base.Transformation(2,
                                name="VARINDEX",
                                pattern=(_base.Glob(1), "[", _base.Glob(1), "]", _base.Glob("index", default="", transform=index_printer)),
                                rules=((_rules.body_to_type_r, _rules.r_index_tt),
                                       (_rules.attributes_and_body_to_none_r, _rules.r_varindex_check),
                                       (_rules.none_to_attributes_r, _rules.gen_const_attribute("array_width", None))))

# helper functions

class Unbundler:
    def __init__(this, obj):
        this.obj = obj
    def __getitem__(this, idx):
        return unbundle(this.obj, attributes={"index" : idx})
    def __iter__(this):
        yield from (unbundle(this.obj, attributes={"index" : n}) for n in range(this.obj.attributes.get("bundle_width")))
    def __len__(this):
        return this.obj.attributes.get("bundle_width")
    def __repr__(this):
        return "Unbundler("+str(this.obj)+")"

class Indexer:
    def __init__(this, obj):
        this.obj = obj
    def __getitem__(this, idx):
        return index(this.obj, attributes={"index":idx})
    def __iter__(this):
        yield from (index(this.obj, attributes={"index":idx}) for idx in _exhaust(this.obj.attributes.get("array_width")))
    def __len__(this):
        return this.obj.attributes.get("array_width")
    def __repr__(this):
        return "Indexer("+str(this.obj)+")"

def make_array(obj, *dims):
    return array(obj, attributes={"array_width":dims})

def _exhaust(dims):
    if type(dims) == int:
        yield from ((n,) for n in range(dims))
    elif len(dims) == 1:
        yield from ((n,) for n in range(dims[0]))
    else:
        yield from ((x,)+y for x in range(dims[0]) for y in _exhaust(dims[1:]))

def soft_link(a, b):
    a.link(b, types={soft_link_t})
