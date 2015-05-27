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
import pleasant.exceptions as _exceptions

def apply(fn, obj, alias=False, keepatoms=True):
    obj = fn(obj)
    if isinstance(obj, _base.Composite):
        if alias:
            newalias = obj.alias
        else:
            newalias = None
        return _base.Composite(fn(obj.trans),
                               *map(lambda o: apply(fn, o, alias=alias, keepatoms=keepatoms), obj.body),
                               alias=newalias,
                               attributes=obj.attributes)
    elif isinstance(obj, _base.Atom):
        if keepatoms:
            return obj
        else:
            return _base.Atom(obj.name+"'",attributes=obj.attributes)
#    elif isinstance(obj, _base.Transformation):
#        return obj
    else:
        return _exceptions.InvalidResolution

def dup(obj, alias=True, keepatoms=True):
    return apply(lambda x: x, obj, alias=alias, keepatoms=keepatoms)

def replace(old, new, obj):
    if obj == old:
        return new
    else:
        return obj

def multireplace(mapping, obj):
    if obj in mapping:
        return mapping[obj]
    else:
        return obj

def network(obj, s=None):
    if s == None:
        s = set()

    if isinstance(obj, _base.Composite):
        for sub in obj.body:
            if sub not in s:
                network(sub, s)

    s.add(obj)

    for l in obj.link_in:
        if l.a not in s:
            network(l.a, s)

    for l in obj.link_out:
        if l.b not in s:
            network(l.b, s)

    return s

def get_net_atoms(obj):
    return set().union(*[{at for at in sub.atoms()} for sub in network(obj)])

def get_atoms(objs):
    return set().union(*[obj.atoms() for obj in objs])

def get_by_transform(transform, obj):
    if isinstance(obj, _base.Composite):
        if obj.trans == transform:
            return {obj}
        else:
            return set.union(*[get_by_transform(transform, sub) for sub in obj])
    else:
        return set()

def get_inputs(obj):
    res = get_net_atoms(obj)
    net = network(obj).difference({obj})
    subs = [sub for sub in net if len(sub.link_in) > 0]
    subatoms = set().union(*[obj.atoms() for obj in subs])
    return res.difference(subatoms)


