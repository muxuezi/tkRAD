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

import tkinter as TK

from . import rad_widget_base as RW



class RADCanvas (RW.RADWidgetBase, TK.Canvas):
    r"""
        generic tkinter.Canvas + RADWidgetBase subclass;

        implements all tkRAD app-wide services by default;

        acts as a tkinter.Canvas widget;
    """



    CONFIG = {

        "borderwidth": 0,

        "highlightthickness": 0,

        "relief": TK.FLAT,

    } # end of CONFIG



    TK_ATTRS = (

        "bg", "background", "bd", "borderwidth", "closeenough",

        "confine", "cursor", "height", "highlightbackground",

        "highlightcolor", "highlightthickness", "relief",

        "scrollregion", "selectbackground", "selectborderwidth",

        "selectforeground", "takefocus" , "width", "xscrollincrement",

        "xscrollcommand", "yscrollincrement", "yscrollcommand",

    ) # end of TK_ATTRS



    def __init__ (self, master = None, **kw):

        # default values

        self.CONFIG = self.CONFIG.copy()

        self.CONFIG.update(kw)

        # super inits

        TK.Canvas.__init__(self, master, **self._only_tk(self.CONFIG))

        RW.RADWidgetBase.__init__(self, master, **self.CONFIG)

    # end def


# end class RADCanvas
