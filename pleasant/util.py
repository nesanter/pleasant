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
    if isinstance(obj, _base.Composite):
        if alias:
            newalias = obj.alias
        else:
            newalias = None
        return _base.Composite(fn(obj.trans),
                               *map(lambda o: apply(fn, o, alias=alias, keepatoms=keepatoms), obj.body),
                               alias=newalias)
    elif isinstance(obj, _base.Atom):
        if keepatoms:
            return fn(obj)
        else:
            return fn(_base.Atom(obj.name+"'"))
    elif isinstance(obj, _base.Transformation):
        return fn(obj)
    else:
        return _exceptions.InvalidResolution

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

def dup(obj, alias=True, keepatoms=True):
    return apply(lambda x: x, obj, alias=alias, keepatoms=keepatoms)


