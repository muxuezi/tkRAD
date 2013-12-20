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

from . import rad_xml_widget as XW



class RADXMLFrame (XW.RADXMLWidget, TK.Frame):
    r"""
        general purpose widget builder and container;

        subclasses tkRAD.xml.RADXMLWidget and tkinter.Frame;

        acts as an XML tkinter widget factory and handles child widgets

        in its own tkinter.Frame container;
    """



    TK_ATTRS = (

        "bg", "background", "bd", "borderwidth", "cursor", "height",

        "highlightbackground", "highlightcolor", "highlightthickness",

        "padx", "pady", "relief", "takefocus", "width",

    ) # end of TK_ATTRS



    def __init__ (self, master = None, **kw):
        r"""
            class constructor;

            initializes tkinter.Frame first and then RADXMLWidget;

            @kw keywords are filtered in Frame inits to avoid

            useless extra exceptions, but are kept fully genuine in

            RADXMLWidget inits;
        """

        # super inits

        TK.Frame.__init__(self, master, **self._only_tk(kw))

        XW.RADXMLWidget.__init__(self, tk_owner = self, **kw)

    # end def


# end class RADXMLFrame
