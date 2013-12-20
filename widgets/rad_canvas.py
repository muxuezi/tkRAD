#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
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

        self.CONFIG.update(kw)

        # super inits

        TK.Canvas.__init__(self, master, **self._only_tk(self.CONFIG))

        RW.RADWidgetBase.__init__(self, master, **self.CONFIG)

    # end def


# end class RADCanvas
