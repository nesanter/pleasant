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

from pleasant import exceptions as _exceptions

class Linkable:
    def __init__(this):
        this.link_in = []
        this.link_out = []
    def link(this, to):
        l = Link(this, to)
        to.link_in += [l]
        this.link_out += [l]

class Atom(Linkable):
    def __init__(this, name=None):
        this.name = name
        this.link_in = []
        this.link_out = []
        this.types = {atom_t}
        this.attributes = dict()
    def __repr__(this):
        if this.name == None:
            return "<atom>"
        else:
            return str(this.name)
    def atoms(this):
        return {this}

class Composite(Linkable):
    def __init__(this, trans, *body, alias=None, attributes=None):
        if not isinstance(trans,Transformation):
            raise _exceptions.InvalidComposition
        if not all(map(lambda obj: isinstance(obj, (Composite,Atom)), body)):
            raise _exceptions.InvalidComposition
        this.trans = trans
        this.body = body
        this.alias = alias
        this.link_in = []
        this.link_out = []
        if attributes == None:
            this.attributes = dict()
        else:
            this.attributes = attributes
        this.types = {}
        trans.apply_rules(this)

    def __repr__(this):
        if this.alias != None:
            return this.alias
        elif this.trans.pattern == None:
            return "(" + str(this.trans) + " . " + str(this.body) + ")"
        else:
            s = ""
            tmp = this.body
            for el in this.trans.pattern:
                if type(el) == str:
                    s += el
                elif type(el) == Glob:
                    ss, tmp = el(tmp, this.attributes)
                    s += ss
#                elif type(el) == int and this.attributes != None and el < len(this.attributes):
#                    s += str(this.attributes[el])
                else:
                    raise _exceptions.InvalidPattern
            return s
    def set_alias(this, alias):
        this.alias = alias

    def atoms(this):
        s = set()
        for obj in this.body:
            s = s.union(obj.atoms())
        return s
    def set_types(this, types):
        this.types = types

class Transformation:
    def __init__(this, nary,
                 name=None,
                 pattern=None,
                 attributes=None,
                 required_attributes=None,
                 rules=None):
        this.name = name
        this.nary = nary
        this.pattern = pattern
        if attributes == None:
            this.attributes = set()
        else:
            this.attributes = attributes
        if required_attributes == None:
            required_attributes = set()
        elif not required_attributes.issubset(this.attributes):
            raise _exceptions.InvalidTransformation
        this.required_attributes = required_attributes
        this.rules = rules

    def __call__(this, *args, attributes=None):
        if this.nary == 0 or (this.nary < 0 and len(args) >= -this.nary) or len(args) == this.nary:
            if attributes == None:
                attributes = set()
            if this.attributes.issuperset(attributes) and this.required_attributes.issubset(attributes):
                return Composite(this, *args, attributes=attributes)
            else:
                raise _exceptions.InvalidTransformationAttributes
        raise _exceptions.InvalidTransformation

    def __repr__(this):
        if this.name == None:
            return "<transform>"
        else:
            return str(this.name)

    def apply_rules(this, obj):
        if type(this.rules) != dict:
            return
        for key, value in this.rules.items():
            if len(key) == 0:
                value(obj)
            elif len(key) == 2:

                if key[0] == None:
                    key = (lambda x: x, key[1])
                if key[1] == None:
                    key = (key[0], lambda x, res: None)

                if not callable(value):
                    raise _exceptions.InvalidRule

                key[1](obj, value(key[0](obj)))
            else:
                raise _exceptions.InvalidRule

class Glob:
    def __init__(this, length, sep=", ", filt=None, default=None):
        this.length = length
        this.sep = sep
        this.filt = filt
        this.default = default
    def __call__(this, objs, attributes):
        if type(this.length) == str:
            return str(attributes.get(this.length, this.default)), objs
        first = True
        s = ""
        if this.length == 0:
            length = len(objs)
        else:
            length = this.length
        for obj in objs[:length]:
            if this.filt != None:
                if this.filt(obj):
                    break
            if first:
                first = False
            else:
                s += this.sep
            s += str(obj)
        return s, objs[length:]

class Link:
    def __init__(this, a, b):
        if not isinstance(a, (Atom,Composite)) or not isinstance(b, (Atom,Composite)):
            raise _exceptions.InvalidLink
        this.a = a
        this.b = b
    def __repr__(this):
        return str(this.a) + " --> " + str(this.b)

class Type:
    def __init__(this, name=None):
        this.name = name
    def __repr__(this):
        if this.name == None:
            return "<type>"
        else:
            return str(this.name)

# base types
atom_t = Type("atom_t")
