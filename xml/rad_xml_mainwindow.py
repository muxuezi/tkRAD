#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
"""



# lib imports

from ..widgets import rad_mainwindow as MW

from . import rad_xml_frame as XF



class RADXMLMainWindow (MW.RADMainWindow):
    r"""
        general purpose tkRAD MainWindow class implementing

        XML tkinter widget building;
    """



    def _init_mainframe (self, **kw):
        r"""
            inherited from RADMainWindow class;
        """

        # widget inits

        self.mainframe = XF.RADXMLFrame(self, **kw)

        self.mainframe.set_xml_filename(

            kw.get("xml_filename", "mainwindow")
        )

        # shortcut inits

        self.xml_build = self.mainframe.xml_build

        self.tk_children = self.mainframe.winfo_children

        self.mainframe.quit_app = self.slot_quit_app

    # end def


# end class RADXMLMainWindow
