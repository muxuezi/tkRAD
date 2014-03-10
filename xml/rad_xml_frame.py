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

from tkinter import ttk

from . import rad_xml_widget as XW



class RADXMLFrame (XW.RADXMLWidget, ttk.Frame):
    r"""
        general purpose widget builder and container;

        subclasses tkRAD.xml.RADXMLWidget and ttk.Frame;

        acts as an XML tkinter widget factory and handles child widgets

        into its own ttk.Frame container;
    """



    CONFIG = {

        # for subclass widget pre-configuration

    } # end of CONFIG



    def __init__ (self, master = None, **kw):

        # default values

        self.CONFIG = self.CONFIG.copy()

        self.CONFIG.update(kw)

        # super inits

        ttk.Frame.__init__(self, master)

        self.configure(**self._only_tk(self.CONFIG))

        self.tk_parent = master

        XW.RADXMLWidget.__init__(

            self, tk_owner=self, slot_owner=master, **self.CONFIG
        )

    # end def


# end class RADXMLFrame
