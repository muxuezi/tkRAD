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



class RADFrame (RW.RADWidgetBase, TK.Frame):
    r"""
        generic tkinter.Frame + RADWidgetBase subclass;

        implements all tkRAD app-wide services by default;

        acts as a tkinter.Frame widget container;
    """



    CONFIG = {

        # for subclass tkinter config()

    } # end of CONFIG



    TK_ATTRS = (

        "bg", "background", "bd", "borderwidth", "cursor", "height",

        "highlightbackground", "highlightcolor", "highlightthickness",

        "padx", "pady", "relief", "takefocus", "width",

    ) # end of TK_ATTRS



    def __init__ (self, master = None, **kw):

        # default values

        self.CONFIG.update(kw)

        # super inits

        TK.Frame.__init__(self, master, **self._only_tk(self.CONFIG))

        RW.RADWidgetBase.__init__(self, master, **self.CONFIG)

    # end def


# end class RADFrame
