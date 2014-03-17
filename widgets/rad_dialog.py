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

import traceback

import tkinter as TK

import tkinter.messagebox as MB

from . import rad_widget_base as RW

from ..core import tools



class RADDialog (RW.RADWidgetBase, TK.Toplevel):
    r"""
        Generic Dialog window class;

        supports transient parent;
        supports modal priority;
        supports self-centering along parent;
    """



    def __init__ (self, master=None, **kw):
        r"""
            class constructor;
        """

        try:

            # super inits

            TK.Toplevel.__init__(self)

            RW.RADWidgetBase.__init__(self, tk_owner=None, **kw)

            # mandatory inits

            self.tk_owner = master

            self.slot_owner = tools.choose(

                kw.get("slot_owner"),

                self,
            )

            # method hooks

            self._init__main(**kw)

        except:

            MB.showerror(

                _("Caught exception"),

                _("An exception has occurred:\n\n{msg}")

                .format(msg=traceback.format_exc(limit=1))
            )

            raise

            exit(1)

        # end try

    # end def



    def _init__main (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # main inits

        self._init_wm_protocols(**kw)

        self._init_members(**kw)

        self._init_options(**kw)

        self._init_geometry(**kw)

        self._init_title(**kw)

        self._init_contents(**kw)

        self._init_layout(**kw)

        self._init_events(**kw)

    # end def



    def _init_events (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # bind events

        self.bind("<Configure>", self._slot_dialog_changed)

        self.events.connect_dict(
            {
                "cancel": self._slot_cancel_dialog,
                "Cancel": self._slot_cancel_dialog,
                "DialogCancel": self._slot_cancel_dialog,

                "ok": self._slot_validate_dialog,
                "OK": self._slot_validate_dialog,
                "DialogOk": self._slot_validate_dialog,
                "DialogOK": self._slot_validate_dialog,
                "validate": self._slot_validate_dialog,
                "Validate": self._slot_validate_dialog,
                "DialogValidate": self._slot_validate_dialog,

                "quit": self._slot_quit_dialog,
                "Quit": self._slot_quit_dialog,

                "DialogPendingTaskOn": self._slot_pending_task_on,
                "DialogPendingTaskOff": self._slot_pending_task_off,
            }
        )

    # end def



    def _init_geometry (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # transient dialog window

        self.transient(

            tools.choose(

                kw.get("transient"),

                kw.get("parent"),

                self.tk_owner,
            )
        )

        # make dialog window resizable

        self.resizable(

            **tools.choose(

                kw.get("resizable"),

                dict(width=False, height=False),
            )
        )

        self.minsize(

            **tools.choose(

                kw.get("minsize"),

                dict(width=100, height=100),
            )
        )

        # dialog window geometry

        self.geometry(

            tools.choose_str(

                kw.get("geometry"),

                self.options["geometry"].get(self.classname()),

                "100x100",
            )
        )

        # maximize dialog window?

        self.set_window_state(

            tools.choose_str(

                kw.get("window_state"),

                self.options["geometry"].get("mainwindow_state"),

                "normal",
            )
        )

    # end def



    def _init_members (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # member inits

        self.STATE = {

            "hidden": self.hide,

            "minimized": self.minimize,

            "normal": self.show,
        }

        self._slot_pending_task_off()

        self.set_modal(**kw)

    # end def



    def _init_options (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # rc options default sections inits

        self.options.set_sections("geometry", "gui")

        # set some default values

        self.options.set_defaults(

            **tools.choose(

                kw.get("rc_defaults"),

                {
                    self.classname(): "100x20",

                    dialog_state = "normal",
                },
            )
        )

        # load options

        self.options.load()

    # end def



    def _init_title (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # dialog window title inits

        _app_title = None

        if hasattr(self.app, "APP") and tools.is_pdict(self.app.APP):

            _app_title = self.app.APP.get("title")

        # end if

        self.title(

            tools.choose_str(

                kw.get("title"),

                _app_title,

                _("Main Window"),

                "Main Window",
            )
        )

    # end def



    def _init_wm_protocols (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # capture window manager's events handling

        self.protocol("WM_DELETE_WINDOW", self._slot_quit_dialog)

    # end def



    def _set_state (self, state):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # param inits

        state = str(state).lower()

        # param controls - unsupported

        if state not in self.STATE:

            raise ValueError(

                _("dialog window's state should be one of {slist}.")

                .format(slist = str(tuple(self.STATE.keys())))
            )

            # reset value

            state = "normal"

        # end if

        # member inits

        self.__window_state = state

        # update rc options

        self.options["geometry"]["dialog_state"] = str(state)

    # end def



    def _slot_dialog_changed (self, tk_event=None, *args, **kw):
        r"""
            slot method for tkinter event "<Configure>";

            updates rc config options on-the-fly;

            no return value (void);
        """

        # /!\ avoid useless calls from child widgets /!\

        if hasattr(tk_event, "widget") and \
                        isinstance(tk_event.widget, self.__class__):

            self._set_state("normal")

            self.options["geometry"]\
                            [self.classname()] = str(self.geometry())

        # end if

    # end def



    def _slot_pending_task_off (self, *args, **kw):
        r"""
            slot method for event signal "DialogPendingTaskOff";

            no return value (void);
        """

        self.__pending_task = False

    # end def



    def _slot_pending_task_on (self, *args, **kw):
        r"""
            slot method for event signal "DialogPendingTaskOn";

            no return value (void);
        """

        self.__pending_task = True

    # end def



    def _slot_quit_dialog (self, *args, **kw):
        r"""
            makes some controls before quitting this dialog window;
        """

        # got some pending operations?

        if self.get_pending_task():

        # dialog in modal mode?

        elif self.is_modal():

            # destroy this dialog window

            self.destroy()

        # all is OK?

        else:

            # keep it simply hidden

            self.hide()

        # end if

    # end def



    def get_pending_task (self):
        r"""
            returns current "pending task" flag value;
        """

        return self.__pending_task

    # end def



    def get_window_state (self):
        r"""
            returns this dialog window state i.e. one of 'minimized',

            'maximized', 'normal' or 'hidden' string of chars;
        """

        return self.__window_state

    # end def



    def hide (self, *args, **kw):
        r"""
            hides this dialog window;

            no return value (void);
        """

        self.withdraw()

        self._set_state("hidden")

    # end def



    def is_modal (self):
        r"""
            returns True if this dialog window is MODAL, False
            otherwise;
        """

        return self.__modal

    # end def



    def minimize (self, *args, **kw):
        r"""
            minimizes (iconifies) this dialog window;

            no return value (void);
        """

        self.iconify()

        self._set_state("minimized")

    # end def



    def set_modal (self, **kw):
        r"""
            sets this dialog window in modal mode or not;

            no return value (void);
        """

        self.__modal = bool(

            tools.choose(

                kw.get("modal"),

                kw.get("dialog"),

                True,
            )
        )

    # end def



    def set_window_state (self, state):
        r"""
            sets this dialog window state i.e. one of 'minimized',
            'normal' or 'hidden' string of chars;

            sets also *REAL* window state along value;

            no return value (void);
        """

        # param inits

        state = str(state).lower()

        # get appropriate method call

        _method = self.STATE.get(state)

        if callable(_method):

            _method()

        else:

            raise ValueError(

                _("unsupported window state '{w_state}'.")

                .format(w_state = state)
            )

        # end if

    # end def



    def show (self, *args, **kw):
        r"""
            shows (deiconifies) this dialog window;

            no return value (void);
        """

        self.deiconify()

        self._set_state("normal")

        # must show in modal mode?

        if self.is_modal() and hasattr(self.tk_owner, "wait_window"):

            # show modal

            self.grab_set()

            self.tk_owner.wait_window(self)

        # end if

    # end def


# end class RADDialog
