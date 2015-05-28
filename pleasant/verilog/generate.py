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

import string

import pleasant.util as _util
from . import lang as _lang
from . import types as _types

def generic_symbol_stream():
    n = 0
    obj = (yield None)
    while True:
        obj = (yield "_gen"+str(n)+"_"+escape(str(obj)))
        n += 1

valid_chars = string.ascii_letters + string.digits
def escape(s):
    return str().join([(ch in valid_chars and ch) or '_' for ch in s])

class Module:
    def __init__(this, *objs, name=None, symbol_stream=None, supress=None):
        this.objs = objs
        this.name = name
        this.symbols = {}
        if supress == None:
            this.supress = set()
        else:
            this.supress = supress

        if symbol_stream == None:
            this.symbol_stream = generic_symbol_stream()
        elif callable(symbol_stream):
            this.symbol_stream = symbol_stream()
        else:
            this.symbol_stream = symbol_stream
        try:
            this.symbol_stream.send(None)
        except TypeError:
            pass
    def get_symbol(this, obj):
        if not obj in this.symbols:
            this.symbols[obj] = this.symbol_stream.send(obj)
        return this.symbols[obj]
    def format_declaration(this, decl):
        pwidth = decl.attributes.get("bundle_width", 0)
        upwidth = decl.attributes.get("array_width", ())

        if pwidth == 0:
            pstr = " "
        else:
            pstr = " ["+str(pwidth-1)+":0] "

        if len(upwidth) == 0:
            upstr = ""
        else:
            upstr = " "
            for w in upwidth:
                upstr += "["+str(w-1)+":0]"
        return pstr+this.get_symbol(decl)+upstr

    def output_declarations(this, fn=print):
        this.output_declaration_type(_lang.reg, "reg", fn=fn)
        this.output_declaration_type(_lang.wire, "wire", fn=fn)
    def output_declaration_type(this, decltype, declstr, fn=print):
        rdecls = set().union(*[_util.get_by_transform(decltype, obj) for obj in this.objs])
        for decl in rdecls:
            if decl.attributes.get("output",False):
                continue
            fn(declstr+this.format_declaration(decl))
    def output_ports(this, fn=print):
        inputs = set()
        outputs = set()
        for obj in this.objs:
            manual_inputs = {sub for sub in _util.network(obj) if sub.attributes.get("input", False)}
            ignore = set().union(*[sub.atoms() for sub in manual_inputs])
            inputs.update({sub for sub in _util.get_inputs(obj) if not sub in ignore}.union(manual_inputs).difference(this.supress))
            outputs.update({sub for sub in _util.network(obj) if sub.attributes.get("output", False)}.difference(this.supress))

        for i in inputs:
            fn("input"+this.format_declaration(i))
        for o in outputs:
            if _types.reg_t in o.types:
                fn("output reg"+this.format_declaration(o))
            else:
                fn("output"+this.format_declaration(o))
    def __repr__(this):
        if this.name == None:
            return "Module("+str(objs)+")"
        return "Module("+str(this.name)+")"


def set_input(obj, is_input=True):
    obj.attributes["input"] = is_input

def set_output(obj, is_output=True):
    obj.attributes["output"] = is_output
