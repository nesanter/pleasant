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

import pleasant.misc as _misc
from pleasant.exceptions import RuleViolation
from .types import *

# rule accessor / mutators
body_to_type_r = (lambda obj: obj.body, lambda obj, res: obj.set_types(res))
body_to_none_r = (lambda obj: obj.body, None)
body_to_attributes_r = (lambda obj: obj.body, lambda obj, res: obj.attributes.update(res))
none_to_attributes_r = (None, lambda obj, res: obj.attributes.update(res))
attributes_to_none_r = (lambda obj: obj.attributes, None)
attributes_to_attributes_r = (lambda obj: obj.attributes, lambda obj, res: obj.attributes.update(res))
attributes_and_body_to_attributes_r = (lambda obj: (obj.attributes, obj.body), lambda obj, res: obj.attributes.update(res))
attributes_and_body_to_none_r = (lambda obj: (obj.attributes, obj.body), None)
attributes_to_remove_type_r = (lambda obj: obj.attributes, lambda obj, res: obj.set_types(obj.types.difference(res)))

# rule functions
def type_transform(match, nomatch, add, remove, objs):
    if any(map(lambda obj: obj.types.isdisjoint(match) or not obj.types.isdisjoint(nomatch), objs)):
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

def enforce(istrue):
    if not istrue:
        raise RuleViolation

def test(fn, iftrue, iffalse, args):
    if fn(args):
        return iftrue
    else:
        return iffalse

def const_attribute(attribute, value, objs):
    return {attribute: value}

def attribute_exists(key, attributes):
    if not key in attributes:
        raise RuleViolation

def attribute_test(key, fn, iftrue, iffalse, attributes):
    if fn(attributes.get(key)):
        return iftrue
    else:
        return iffalse

def on_attribute(fn, attribute, objs):
    return map(fn, (obj.attributes.get(attribute) for obj in objs))

def unbundle_width(attribs):
    base_width = attribs.get("bundle_width", None)
    if base_width == None:
        raise RuleViolation
    index = attribs.get("index")
    if index == None:
        raise RuleViolation
    if type(index) == int:
        s = slice(index,index+1)
    elif type(index) == slice:
        s = index
    else:
        s = slice(*index)
    if s.stop != None and s.stop > base_width:
        raise RuleViolation
    if s.start != None and s.start >= base_width:
        raise RuleViolation
    indices = s.indices(base_width)
    new_width = (indices[1] - indices[0]) // indices[2]
    if new_width == 0:
        raise RuleViolation
    return {"bundle_width" : new_width}

# rule generators
def gen_type_transform(match, nomatch=None, add=None, remove=None):
    if nomatch == None:
        nomatch = set()
    if add == None:
        add = set()
    if remove == None:
        remove = set()
    return _misc.curry(type_transform, match, nomatch, add, remove)

def gen_const_attribute(attribute, value):
    return _misc.curry(const_attribute, attribute, value)

def gen_on_attribute(fn, attribute):
    return _misc.curry(on_attribute, fn, attribute)

def gen_attribute_exists(attribute):
    return _misc.curry(attribute_exists, attribute)

def gen_attribute_test(attribute, fn, iftrue=True, iffalse=False):
    return _misc.curry(attribute_test, attribute, fn, iftrue, iffalse)

def gen_test(fn, iftrue=True, iffalse=False):
    return _misc.curry(test, fn, iftrue, iffalse)

# generated rules
r_boolean_tt = gen_type_transform(
    {atom_t, expr_t, logic_t}, nomatch={array_t},
    add={expr_t, logic_t}, remove={atom_t, reg_t, wire_t})

r_reg_tt = gen_type_transform(
    {atom_t}, nomatch={expr_t, logic_t, array_t},
    add={reg_t, logic_t}, remove={atom_t})

r_wire_tt = gen_type_transform(
    {atom_t}, nomatch={expr_t, logic_t, array_t},
    add={wire_t, logic_t}, remove={atom_t})

r_bundle_tt = gen_type_transform(
    {atom_t, logic_t, bundle_t}, nomatch={array_t},
    add={logic_t, bundle_t}, remove={atom_t})

r_unbundle_tt = gen_type_transform(
    {atom_t, bundle_t}, nomatch={array_t},
    remove={atom_t})

r_sync_tt = gen_type_transform(
    {atom_t, syncable_t},
    add={synced_t}, remove={atom_t,syncable_t})

r_array_tt = gen_type_transform(
    {atom_t, reg_t, wire_t, bundle_t}, nomatch={expr_t,array_t},
    add={array_t}, remove={atom_t})

r_index_tt = gen_type_transform(
    {atom_t, array_t},
    remove={atom_t, array_t})

r_unbundle_tt2 = gen_attribute_test("bundle_width", lambda v: v == 1, {bundle_t}, set())

r_index_check = lambda ab: enforce(len(list(_misc.flatten(ab[0].get("index", [])))) == len(list(_misc.flatten(ab[1][0].attributes.get("array_width")))) and all(((lambda a,b: a<b)(*v) for v in  zip((v for v in _misc.flatten(ab[0].get("index"))),(v for v in _misc.flatten(ab[1][0].attributes.get("array_width")))))))

r_let_check = lambda body: enforce(not body[0].types.isdisjoint({atom_t, reg_t}) and body[0].types.isdisjoint({expr_t, array_t}) and not body[1].types.isdisjoint({atom_t, logic_t, array_t}))
r_let_tt = lambda body: {syncable_t}

r_width_same = gen_on_attribute(all_same_weak, "bundle_width")

r_bundle_width = lambda body: {"bundle_width" : sum((obj.attributes.get("bundle_width",1) for obj in body))}
#r_unbundle_width = lambda ab: {"bundle_width" : sum((obj.attributes.get("bundle_width",1) for obj in ab[1][0].body[slice(*_misc.flatten(ab[0].get("index")))]))}
r_unbundle_width = unbundle_width

r_trigger_valid = lambda attribs: type_transform({atom_t, clock_t}, set(), set(), set(), attribs.get("clock",[]))
