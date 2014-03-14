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

from tkinter import ttk

from ..core import tools

from . import rad_frame as RF



class RADStatusBar (RF.RADFrame):
    r"""
        generic status bar for rapid application development (RAD);

        supports direct and constant display of message;

        e.g. self.info("Ready.");

        supports notification-type message (short-living message);

        e.g. self.notify("This message will end in 5 seconds.");

        supports notification delay settings;

        e.g. self.delay = 5.2  # in seconds;
    """



    NOTIFICATION_DELAY = 5 # seconds

    MINIMUM_CONSISTENT_DELAY = 0.5 # seconds



    def _stop_notification (self):
        r"""
            protected method def;

            stops any pending notification and

            resets process id pointer;

            no return value (void);
        """

        # stop any pending notification

        self.after_cancel(self.__notify_pid)

        # reset process id

        self.__notify_pid = 0

    # end def



    @property
    def delay (self):
        r"""
            returns current internal notification delay value;
        """

        return self.__delay

    # end def



    @delay.setter
    def delay (self, value):

        self.__delay = max(

            self.MINIMUM_CONSISTENT_DELAY,

            tools.ensure_float(value),
        )

    # end def



    @delay.deleter
    def delay (self):

        del self.__delay

    # end def



    def get_correct_delay (self, delay = None):
        r"""
            tries to retrieve a correct delay value amongst many;

            returns found value or default value, otherwise;
        """

        return max(

            self.MINIMUM_CONSISTENT_DELAY,

            tools.choose_num(

                lambda x: x > 0,

                delay,

                self.options["gui"]
                    .get("statusbar_notification_delay"),

                self.delay,

                self.NOTIFICATION_DELAY,

                5 # last but not least
            )
        )

    # end def



    def info (self, text = None):
        r"""
            sets the highest priority-level message for this status

            bar object;

            any pending notifications will be stopped to ensure the

            current message won't be masked at any time;

            no return value (void);
        """

        # stop any pending notification

        self._stop_notification()

        # default text inits

        self.__static_text = tools.choose_str(

            text,

            self.__static_text,

            _("Ready."),

            "Ready."
        )

        # end if

        self.message.set(self.__static_text)

    # end def



    def init_widget (self, **kw):
        r"""
            inherited method from RADWidgetBase base class;

            here come the main inits;

            no return value (void);
        """

        # member inits

        self.__notify_pid = 0

        self.__static_text = None

        self.toggle_var = TK.StringVar()

        self.delay = self.NOTIFICATION_DELAY

        self.MINIMUM_CONSISTENT_DELAY = \
            abs(self.MINIMUM_CONSISTENT_DELAY)

        # rc options inits

        self.options.set_sections("gui")

        self.options.load()

        # widget inits

        ttk.Sizegrip(self).pack(padx=2, pady=2, side=TK.RIGHT)

        self.message = TK.StringVar()

        self.label = ttk.Label(

            self,

            textvariable = self.message,

            anchor = TK.W,

            justify = TK.LEFT,

            relief = TK.SUNKEN,
        )

        self.label.pack(padx=2, pady=2, **self.PACK_OPTIONS)

        self.info()

    # end def



    def notify (self, text, delay = None):
        r"""
            sets a low priority-level message for a delayed bit of

            time (in seconds);

            any pending notifications will be stopped to ensure the

            current message won't be masked at any time;

            no return value (void);
        """

        # param controls

        if tools.is_pstr(text):

            # stop any pending notification

            self._stop_notification()

            # set new message

            self.message.set(text)

            # look for a correct value

            delay = self.get_correct_delay(delay)

            # restore static text after @delay (in seconds)

            # notice: @delay param can be of 'int' or 'float' type /!\

            self.__notify_pid = self.after(

                tools.ensure_int(delay * 1000.0),

                self.info
            )

            # must update idle tasks

            self.update_idletasks()

        # end if

    # end def



    def toggle (self, *args, **kw):
        r"""
            switches ON / OFF display of status bar along toggle_var

            internal integer value (0 = OFF, other = ON);

            raises "StatusbarShow" and "StatusbarHide" named events

            just before toggling display of status bar;

            these events are of tkRAD.core.events type, *NOT* of

            tkinter ones;

            /!\ notice: for technical reasons, toggling is only done

            with self.grid() and self.grid_remove() methods

            as self.pack() and self.pack_forget() do *NOT* keep

            correctly the reserved space for status bar in window;

            no return value (void);
        """

        # only if toggle_var is set up /!\

        if self.toggle_var:

            # tk control var inits

            _value = self.toggle_var.get()

            # update config options

            self.options["gui"]["show_statusbar"] = str(_value)

            # show status bar

            if tools.ensure_int(_value):

                self.grid()

                self.events.raise_event("StatusbarShow", widget = self)

            # hide status bar

            else:

                self.grid_remove()

                self.events.raise_event("StatusbarHide", widget = self)

            # end if

        else:

            print("[WARNING] toggle_var is *NOT* set up.")

        # end if

    # end def



    @property
    def toggle_var (self):
        r"""
            returns current internal tkinter StringVar control
            variable;
        """

        return self.__toggle_var

    # end def



    @toggle_var.setter
    def toggle_var (self, arg):

        # param control

        if isinstance(arg, TK.StringVar):

            self.__toggle_var = arg

        else:

            raise TypeError(
                _(
                    "Statusbar toggle variable must be "

                    "of type {obj_type}."

                ).format(obj_type = repr(TK.StringVar))
            )

            # set a rescue var nevertheless

            self.__toggle_var = TK.StringVar()

        # end if

        # config options inits

        self.__toggle_var.set(

            self.options["gui"].get("show_statusbar", "1")
        )

    # end def



    @toggle_var.deleter
    def toggle_var (self):

        del self.__toggle_var

    # end def



    def toggle_var_set (self, value):
        r"""
            sets a @value to current toggle_var StringVar;

            toggles automatically statusbar along @value;

            no return value (void);
        """

        if self.toggle_var:

            self.toggle_var.set(str(value))

            self.toggle()

        else:

            print("[WARNING] toggle_var is *NOT* set up.")

        # end if

    # end def


# end class RADStatusBar
