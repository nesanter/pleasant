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
import pleasant.util as _util
from . import rules as _rules
from . import types as _types

# transformations
bitand = _base.Transformation(2,
                        name="&",
                        pattern=("(", _base.Glob(1), " & ", _base.Glob(1), ")"),
                        rules={_rules.body_to_type_r : _rules.r_boolean_tt,
                               _rules.body_to_none_r : _rules.r_width_same})
bitor = _base.Transformation(2,
                       name="|",
                       pattern=("(", _base.Glob(1), " | ",_base.Glob(1), ")"),
                       rules={_rules.body_to_type_r : _rules.r_boolean_tt,
                              _rules.body_to_none_r : _rules.r_width_same})
bitxor =_base.Transformation(2,
                        name="^",
                        pattern=("(",_base.Glob(1), " ^ ",_base.Glob(1), ")"),
                        rules={_rules.body_to_type_r : _rules.r_boolean_tt,
                               _rules.body_to_none_r : _rules.r_width_same})
reduceand =_base.Transformation(1,
                           name="r&",
                           pattern=("&",_base.Glob(1)),
                           rules={_rules.body_to_type_r : _rules.r_boolean_tt,
                                  _rules.none_to_attributes_r : _rules.gen_const_attribute("bundle_width", 1)})
reduceor =_base.Transformation(1,
                          "r|",
                          pattern=("|",_base.Glob(1)),
                          rules={_rules.body_to_type_r : _rules.r_boolean_tt,
                                 _rules.none_to_attributes_r : _rules.gen_const_attribute("bundle_width", 1)})

group =_base.Transformation(0, "GROUP", pattern=("{",_base.Glob(0,sep="; "), "}"))
groupln =_base.Transformation(0, "GROUP", pattern=("{\n",_base.Glob(0, sep=";\n"), "}"))
#case =_base.Transformation(2, name="CASE", pattern=(Glob(1)," : (",Glob(1),")"))
#switch =_base.Transformation(-1, name="SWITCH", pattern=("switch ",Glob(1), " { ",Glob(0), " }"))

wire =_base.Transformation(1,
                      name="WIRE",
                      pattern=("wire:",_base.Glob(1)),
                      rules={_rules.body_to_type_r : _rules.r_wire_tt,
                             _rules.none_to_attributes_r : _rules.gen_const_attribute("bundle_width", 1)})
reg =_base.Transformation(1,
                     name="REG",
                     pattern=("reg:",_base.Glob(1)),
                     rules={_rules.body_to_type_r : _rules.r_reg_tt,
                            _rules.none_to_attributes_r : _rules.gen_const_attribute("bundle_width", 1)})

bundle = _base.Transformation(0,
                              name="BUNDLE",
                              pattern=("{", _base.Glob(0,sep=" "), "}"),
                              rules={_rules.body_to_type_r : _rules.r_bundle_tt,
                                     _rules.body_to_attributes_r : _rules.r_bundle_width})

unbundle = _base.Transformation(1,
                                name="UNBUNDLE",
                                pattern=(_base.Glob(1), _base.Glob("index", default="", transform=lambda v: list(_util.flatten(v)))),
                                rules={_rules.body_to_type_r : _rules.r_unbundle_tt,
                                       _rules.body_and_attributes_to_attributes_r : _rules.r_unbundle_width})
#pack =_base.Transformation(1,
#                      name="PACK",
#                      attributes={"packed_width"},
#                      required_attributes={"packed_width"},
#                      pattern=(_base.Glob(1), ":", _base.Glob("packed_width")),
#                      rules={_rules.body_to_type_r : _rules.r_pack_tt})
#
#cindex = _base.Transformation(1,
#                              name="INDEX",
#                              attributes={"index", "width"},
#                              required_attributes={"index"},
#                              pattern=(_base.Glob(1), "[", _base.Glob("index"), "]"),
#                              rules={_rules.body_to_none_r : _rules.gen_on_attribute(lambda v: v > 0, "packed_width")})
