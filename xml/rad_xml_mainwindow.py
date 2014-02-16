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

from ..core import tools

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

        self.mainframe = tools.choose(

            kw.get("mainframe"),

            XF.RADXMLFrame(self, **kw),
        )

        if hasattr(self.mainframe, "set_xml_filename"):

            self.mainframe.set_xml_filename(

                tools.choose_str(

                    kw.get("xml_filename"),

                    "mainwindow",
                )
            )

        # end if

        # shortcut inits

        if hasattr(self.mainframe, "xml_build"):

            self.xml_build = self.mainframe.xml_build

        # end if

        self.tk_children = self.mainframe.winfo_children

        self.mainframe.quit_app = self._slot_quit_app

    # end def


# end class RADXMLMainWindow
