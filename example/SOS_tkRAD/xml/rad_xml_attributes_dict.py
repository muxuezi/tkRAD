#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkRAD - tkinter Rapid Application Development library

    (c) 2013+ Raphaël SEBAN <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public
    License along with this program.

    If not, see: http://www.gnu.org/licenses/
"""



# lib imports

from ..core import struct_dict as SD

from . import rad_xml_attribute as XA



class RADXMLAttributesDict (SD.StructDict):
    r"""
        StructDict subclass for commodity;

        handles support for RADXMLAttribute items;
    """



    def __init__ (self, *args, **kw):
        r"""
            class constructor;

            implements @item_type = RADXMLAttribute;
        """

        # super class inits

        super().__init__(*args, **kw)

        # member inits

        self.item_type = XA.RADXMLAttribute

        self.item_value_getter = "get_value"

        self.item_value_setter = "set_value"

    # end def


# end class RADXMLAttributesDict
