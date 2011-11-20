#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 by Victor von Rhein
victor@caern.de

This file is part of DiceRoller-WoD.

DiceRoller-WoD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation,  either version 3 of the License,  or
(at your option) any later version.

DiceRoller-WoD is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DiceRoller-WoD.  If not,  see <http://www.gnu.org/licenses/>.

@package DiceRoller-WoD
"""



import os
from cx_Freeze import setup, Executable
import sip

import Nexus




if os.name == "nt":
	_base = "Win32GUI"
else:
	_base = "Console"


exe = Executable(
	script="DiceRoller-WoD.py",
	base = _base
	)


setup(
	name = Nexus.PROGRAM_NAME,
	version = Nexus.PROGRAM_VERSION_MAJOR,
	description = Nexus.PROGRAM_DESCRIPTION,
	executables = [exe]
	)
