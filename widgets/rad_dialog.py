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

import re

import traceback

import tkinter as TK

import tkinter.messagebox as MB

from . import rad_widget_base as RW

from ..xml import rad_xml_frame as XF

from ..core import tools



# ===========================   CLASS DEF   ============================



class RADDialog (RW.RADWidgetBase, TK.Toplevel):
    r"""
        Generic Dialog window class;

        supports transient parent;
        supports modal priority;
        supports self-centering along parent;
    """



    def __init__ (self, master, **kw):
        r"""
            class constructor;
        """

        try:

            # super inits

            TK.Toplevel.__init__(self)

            RW.RADWidgetBase.__init__(self, tk_owner=None, **kw)

            # mandatory inits

            self.tk_owner = tools.choose(

                kw.get("tk_owner"),

                master,
            )

            self.cast_parent(self.tk_owner)

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



    def _get_geometry_position (self, str_geometry):
        r"""
            protected method def;

            this shan't be overridden in subclass;

            no return value (void);
        """

        _pos = re.search(r"([\+\-]\d+[\+\-]\d+)", str(str_geometry))

        if _pos:

            _pos = _pos.group(0)

        # end if

        return _pos

    # end def



    def _hook_center_dialog (self, tk_event=None, *args, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        self.center_dialog(tk_event, *args, **kw)

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

        self._init_title(**kw)

        self._init_geometry(**kw)

        self._init_contents(**kw)

        self._init_events(**kw)

    # end def



    def _init_contents (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # set widget inits (hook method from RADWidgetBase)

        self.init_widget(**kw)

    # end def



    def _init_events (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # connecting people

        self.events.connect_dict(
            {
                "DialogCancel": self._slot_button_cancel,

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

                # default parent widget

                self.tk_owner,
            )
        )

        # make dialog window resizable

        self.resizable(

            **tools.choose(

                kw.get("resizable"),

                # default is *NOT* resizable (dialog box)

                dict(width=False, height=False),
            )
        )

        self.minsize(

            **tools.choose(

                kw.get("minsize"),

                # default minimum size

                dict(width=20, height=20),
            )
        )

        # avoid accidental showing up

        self.hide()

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
                    "dialog_state": "normal",
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

        _title = kw.get("title")

        if tools.is_pstr(_title):

            # set i18n translations support

            self.title(_(_title))

        # end if

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

                _("dialog's window state should be one of {slist}.")

                .format(slist=str(tuple(self.STATE.keys())))
            )

            # reset value

            state = "normal"

        # end if

        # member inits

        self.__window_state = state

        # update rc options

        self.options["geometry"]["dialog_state"] = str(state)

    # end def



    def _slot_button_cancel (self, tk_event=None, *args, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # cancel pending tasks (hook method)

        if self.cancel_dialog(tk_event, *args, **kw):

            # switch off flag

            self._slot_pending_task_off()

            # quit dialog

            self._slot_quit_dialog()

        # end if

    # end def



    def _slot_dialog_changed (self, tk_event=None, *args, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        self.options["geometry"]\
                            [self.classname()] = self.winfo_geometry()

    # end def



    def _slot_pending_task_off (self, tk_event=None, *args, **kw):
        r"""
            slot method for event signal "DialogPendingTaskOff";

            no return value (void);
        """

        self.__pending_task = False

    # end def



    def _slot_pending_task_on (self, tk_event=None, *args, **kw):
        r"""
            slot method for event signal "DialogPendingTaskOn";

            no return value (void);
        """

        self.__pending_task = True

    # end def



    def _slot_quit_dialog (self, tk_event=None, *args, **kw):
        r"""
            makes some controls before quitting this dialog window;
        """

        # got some pending operations?

        if self.get_pending_task():

            _response = MB.askquestion(

                _("Please confirm"),

                _(
                    "Some important tasks are still running.\n"

                    "Should I try to cancel them?"
                ),

                parent=self,
            )

            if _response == TK.YES:

                self._slot_button_cancel()

            # end if

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



    def cancel_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog cancellation method;

            this is a hook called by '_slot_button_cancel()';

            this *MUST* be overridden in subclass;

            returns True on success, False otherwise;
        """

        # put here your own code in subclass

        # succeeded

        return True

    # end def



    def center_dialog (self, tk_event=None, *args, **kw):
        r"""
            tries to center dialog either along screen dims if no
            parent defined or along parent window if transient;

            no return value (void);
        """

        # ensure dims are correct

        self.update_idletasks()

        # dialog size inits

        _dlg_width = self.winfo_reqwidth()

        _dlg_height = self.winfo_reqheight()

        # got parent (transient)?

        if self.is_tk_parent(self.tk_owner):

            _root_width = self.tk_owner.winfo_width()

            _root_height = self.tk_owner.winfo_height()

            _root_x = self.tk_owner.winfo_rootx()

            _root_y = self.tk_owner.winfo_rooty()

        # no parent - use screen size

        else:

            _root_width = self.winfo_screenwidth()

            _root_height = self.winfo_screenheight()

            _root_x = 0

            _root_y = 0

        # end if

        # make calculations

        _left = tools.ensure_int(

            _root_x + (_root_width - _dlg_width)//2
        )

        _top = tools.ensure_int(

            _root_y + (_root_height - _dlg_height)//2
        )

        # update geometry

        self.geometry("+{x}+{y}".format(x=_left, y=_top))

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
            'normal' or 'hidden' string of chars;
        """

        return self.__window_state

    # end def



    def hide (self, tk_event=None, *args, **kw):
        r"""
            hides this dialog window;

            no return value (void);
        """

        self.unbind("<Configure>")

        self.withdraw()

        self._set_state("hidden")

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # put your own code in subclass;

        _xml = """
            <tkwidget>
                <ttklabel
                    text="{text}"
                    foreground="red"
                    layout="pack"
                    layout_options="pady=10"
                    resizable="yes"
                    wraplength="10cm"
                />
                <ttkbutton
                    text="_OK"
                    command="._slot_button_cancel"
                    layout="pack"
                />
            </tkwidget>

        """.format(

            text =  "_Please, use "
                    "RADDialog(master, xml=xml_code) "
                    "or RADDialog(master, "
                    "filename=xml_filepath_or_filename) "
                    "to build your own dialog GUI."
        )

        _contents = tools.choose_str(

            kw.get("xml"), kw.get("filename"), _xml,
        )

        # set contents

        self.set_contents(_contents, **kw)

    # end def



    def is_modal (self):
        r"""
            returns True if this dialog window is MODAL, False
            otherwise;
        """

        return self.__modal

    # end def



    def minimize (self, tk_event=None, *args, **kw):
        r"""
            minimizes (iconifies) this dialog window;

            no return value (void);
        """

        self.unbind("<Configure>")

        self.iconify()

        self._set_state("minimized")

    # end def



    def set_contents (self, contents, pad_x=7, pad_y=7, **kw):
        r"""
            sets dialog widget contents;

            no return value (void);
        """

        # param controls

        if tools.is_pstr(contents):

            _frame = XF.RADXMLFrame(self)

            _frame.xml_build(contents)

            contents = _frame

        # end if

        # contents is already a widget?

        if self.cast_widget(contents):

            for _w in self.winfo_children():

                _w.pack_forget()
                _w.grid_forget()
                _w.place_forget()

            # end for

            self.container = contents

            self.container.grid(

                in_=self,

                row=0, column=0,

                padx=pad_x, pady=pad_y,

                sticky=self.STICKY_ALL,
            )

        # end if

    # end def



    def set_modal (self, value=None, **kw):
        r"""
            sets this dialog window in modal mode or not;

            no return value (void);
        """

        self.__modal = tools.choose_type(

            bool, value, kw.get("modal"), True
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



    def show (self, tk_event=None, *args, **kw):
        r"""
            shows (deiconifies) this dialog window;

            no return value (void);
        """

        # update window state

        self._set_state("normal")

        # must show in modal mode?

        if self.is_modal() and hasattr(self.tk_owner, "wait_window"):

            # modal dialogs should be centered (hook method)

            self._hook_center_dialog(tk_event, *args, **kw)

            # pop-up dialog

            self.deiconify()

            # show modal

            self.grab_set()

            # wait until dialog window is destroyed

            self.tk_owner.wait_window(self)

        # toolbox mode (transient, non-modal)

        else:

            # get RC stored geometry

            self.geometry(

                self._get_geometry_position(

                    self.options["geometry"].get(self.classname())
                )
            )

            # pop-up dialog

            self.deiconify()

            # size bindings

            self.update_idletasks()

            self.bind("<Configure>", self._slot_dialog_changed)

        # end if

    # end def



    def validate_dialog (self, tk_event=None, *args, **kw):
        r"""
            user dialog validation method;

            this is a hook called by '_slot_button_ok()';

            this *MUST* be overridden in subclass;

            returns True on success, False otherwise;
        """

        # put here your own code in subclass

        # succeeded

        return True

    # end def


# end class RADDialog



# ===========================   CLASS DEF   ============================



class RADButtonsDialog (RADDialog):
    r"""
        RADDialog subclass implementing a buttonbar;
    """



    # current list of supported buttons

    BUTTONS = (

        "Abandon", "Abort", "Apply", "Cancel", "Delete", "Ignore",
        "No", "OK", "Ok", "Rename", "Replace", "Reply", "Reset",
        "Retry", "Save", "SaveAs", "Send", "Submit", "Validate",
        "Verify", "Yes",

    ) # end of BUTTONS



    # button's slot template string

    BUTTON_SLOT = "_slot_button_{button_name}"



    def _get_slot (self, name, raise_error=True):
        r"""
            protected method def;

            this shan't be overridden in subclass;

            no return value (void);
        """

        # inits

        _slot = self.BUTTON_SLOT.format(

            button_name = tools.normalize_id(name).lower()
        )

        if raise_error:

            return getattr(self.slot_owner, _slot)

        else:

            return getattr(self.slot_owner, _slot, None)

        # end if

    # end def



    def _init_contents (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # set widget inits (hook method from RADWidgetBase)

        self.init_widget(**kw)

    # end def



    def _init_events (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # connecting people

        super()._init_events(**kw)

        for _button in self.BUTTONS:

            self.events.connect(

                "Dialog" + _button, self._get_slot(_button)
            )

        # end for

    # end def



    def _init_members (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # member inits

        super()._init_members(**kw)

        self.__buttons = None

    # end def



    def _slot_button_abandon (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_abort (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_apply (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_delete (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_ignore (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_no (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_ok (self, tk_event=None, *args, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # validate dialog (hook method)

        if self.validate_dialog(tk_event, *args, **kw):

            # switch off flag

            self._slot_pending_task_off()

            # quit dialog

            self._slot_quit_dialog()

        # end if

    # end def



    def _slot_button_rename (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_replace (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_reply (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_reset (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_retry (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_save (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_saveas (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_send (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_submit (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_validate (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_verify (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def _slot_button_yes (self, tk_event=None, *args, **kw):
        r"""
            dialog button slot method;

            this *MUST* be overridden in subclass;

            no return value (void);
        """

        # put your own code in subclass

        pass

    # end def



    def init_widget (self, **kw):
        r"""
            widget main inits;
        """

        # put your own code in subclass;

        _xml = """
            <tkwidget>
                <ttklabel
                    text="{text}"
                    foreground="red"
                    layout="pack"
                    resizable="yes"
                    wraplength="10cm"
                />
            </tkwidget>

        """.format(

            text =  "_Please, use "
                    "RADButtonsDialog(master, xml=xml_code) "
                    "or RADButtonsDialog(master, "
                    "filename=xml_filepath_or_filename) "
                    "to build your own dialog GUI."
        )

        _contents = tools.choose_str(

                kw.get("xml"), kw.get("filename"), _xml,
        )

        # set contents

        self.set_contents(_contents, **kw)

        # set buttonbar

        self.set_buttons(*kw.get("buttons", list()), **kw)

    # end def



    def set_buttons (self, *args, pad_x=7, pad_y=7, **kw):
        r"""
            sets up buttonbar;
        """

        # param inits

        _buttons = tools.choose(

            args,

            self.__buttons,

            ("OK", "Cancel"),
        )

        # update members

        self.__buttons = _buttons

        self.buttonbar = TK.ttk.Frame(self)

        # loop on buttons list

        for _button in _buttons:

            TK.ttk.Button(

                self.buttonbar,

                text=_(_button),

                command=self._get_slot(_button),

            ).pack(side=TK.LEFT, padx=5)

        # end for

        # buttonbar layout

        self.buttonbar.grid(row=1, column=0, padx=pad_x, pady=pad_y)

    # end def


# end class RADButtonsDialog

