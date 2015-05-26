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

import pleasant.util as _util
from pleasant.exceptions import RuleViolation
from .types import *

# rule accessor / mutators
body_to_type_r = (lambda obj: obj.body, lambda obj, res: obj.set_types(res))
body_to_none_r = (lambda obj: obj.body, None)
body_to_attributes_r = (lambda obj: obj.body, lambda obj, res: obj.attributes.update(res))
none_to_attributes_r = (None, lambda obj, res: obj.attributes.update(res))
attributes_to_attributes_r = (lambda obj: obj.attributes, lambda obj, res: obj.attributes.update(res))
body_and_attributes_to_attributes_r = (lambda obj: (obj.attributes, obj.body), lambda obj, res: obj.attributes.update(res))

# rule functions
def type_transform(match, add, remove, objs):
    if any(map(lambda obj: obj.types.isdisjoint(match), objs)):
        raise RuleViolation
    return add.union(*iter([obj.types for obj in objs])).difference(remove)

def all_same_weak(vals):
    cur = None
    for val in vals:
        if val == None:
            pass
        elif cur == None:
            cur = val
        elif cur == val:
            pass
        else:
            raise RuleViolation

def assert_all(fn, vals):
    if any(map(fn, vals)):
        raise RuleViolation

def const_attribute(attribute, value, objs):
    return {attribute: value}

def on_attribute(fn, attribute, objs):
    return map(fn, (obj.attributes.get(attribute) for obj in objs))

# rule generators
def gen_type_transform(match, nomatch=None, add=None, remove=None):
    if nomatch == None:
        nomatch = set()
    if add == None:
        add = set()
    if remove == None:
        remove = set()
    return _util.curry(type_transform, match, add, remove)

def gen_const_attribute(attribute, value):
    return _util.curry(const_attribute, attribute, value)

def gen_on_attribute(fn, attribute):
    return _util.curry(on_attribute, fn, attribute)

# generated rules
r_boolean_tt = gen_type_transform(
    {atom_t, expr_t, logic_t},
    add={expr_t}, remove={atom_t, reg_t, wire_t})

r_reg_tt = gen_type_transform(
    {atom_t}, nomatch={expr_t, logic_t},
    add={reg_t, logic_t}, remove={atom_t})

r_wire_tt = gen_type_transform(
    {atom_t}, nomatch={expr_t, logic_t},
    add={wire_t, logic_t}, remove={atom_t})

r_bundle_tt = gen_type_transform(
    {atom_t, logic_t, bundle_t},
    add={logic_t, bundle_t}, remove={atom_t})

r_unbundle_tt = gen_type_transform(
    {atom_t, bundle_t},
    add=set(), remove={atom_t})

r_width_same = gen_on_attribute(all_same_weak, "bundle_width")

r_bundle_width = lambda body: {"bundle_width" : sum((obj.attributes.get("bundle_width",1) for obj in body))}
r_unbundle_width = lambda ab: {"bundle_width" : sum((obj.attributes.get("bundle_width",1) for obj in ab[1][0].body[slice(*_util.flatten(ab[0].get("index")))]))}
