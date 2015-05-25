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

class InvalidComposition(Exception):
    pass

class InvalidTransformation(Exception):
    pass

class InvalidTransformationAttributes(InvalidTransformation):
    pass

class InvalidResolution(Exception):
    pass

class InvalidPattern(Exception):
    pass

class InvalidLink(Exception):
    pass

class InvalidRule(Exception):
    pass

class RuleViolation(Exception):
    pass
