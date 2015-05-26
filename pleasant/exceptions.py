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

class PleasantException(Exception):
    pass

class InvalidComposition(PleasantException):
    pass

class InvalidTransformation(PleasantException):
    pass

class InvalidTransformationAttributes(InvalidTransformation):
    pass

class InvalidResolution(PleasantException):
    pass

class InvalidPattern(PleasantException):
    pass

class InvalidLink(PleasantException):
    pass

class InvalidRule(PleasantException):
    pass

class RuleViolation(PleasantException):
    pass
