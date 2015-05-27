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
from . import lang as _lang
from . import types as _types

def generic_symbol_stream():
    n = 0
    while True:
        yield "_gen"+str(n)
        n += 1

class Module:
    def __init__(this, name, *objs, symbol_stream=None):
        this.objs = objs
        this.name = name
        this.symbols = {}
        if symbol_stream == None:
            this.symbol_stream = generic_symbol_stream()
        elif callable(symbol_stream):
            this.symbol_stream = symbol_stream()
        else:
            this.symbol_stream = symbol_stream
    def get_symbol(this, obj):
        if not obj in this.symbols:
            this.symbols[obj] = next(this.symbol_stream)
        return this.symbols[obj]
    def output_declarations(this, fn=print):
        this.output_declaration_type(_lang.reg, "reg", fn=fn)
        this.output_declaration_type(_lang.wire, "wire", fn=fn)
    def output_declaration_type(this, decltype, declstr, fn=print):
        rdecls = set().union(*[_util.get_by_transform(decltype, obj) for obj in this.objs])
        for decl in rdecls:
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

            fn(declstr+pstr+this.get_symbol(decl)+upstr)
    def __repr__(this):
        return "Module("+str(this.name)+")"

