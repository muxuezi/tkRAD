#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
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
