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

import tkinter as TK

from tkinter import ttk

from ..core import tools

from ..core import path

from . import rad_xml_widget_base as RB



class RADXMLWidget (RB.RADXMLWidgetBase):
    r"""
        generic XML to tkinter widget builder;

        this is THE tkinter widget building processor of tkRAD;

        supports tkinter natives in XML script
        e.g. <button id="" text="OK" command="@OKClicked" .../>

        supports user-defined specific widgets in XML script
        e.g. <widget id="" class="MyClassName" .../>

        supports on-the-fly module imports
        e.g. <module import="tkinter" as="TK"/>

        and many, many other features (see doc for more);
    """



    # 'anchor' XML attribute pre-compiled subs

    ANCHORS = (

        (re.compile(r"(?i)north|top|up"), TK.N),
        (re.compile(r"(?i)south|bottom|down"), TK.S),
        (re.compile(r"(?i)east|right"), TK.E),
        (re.compile(r"(?i)west|left"), TK.W),
        (re.compile(r"\W+"), r""),
        (re.compile(TK.N + "+"), TK.N),
        (re.compile(TK.S + "+"), TK.S),
        (re.compile(TK.E + "+"), TK.E),
        (re.compile(TK.W + "+"), TK.W),
        (re.compile(TK.W + TK.N), TK.NW),
        (re.compile(TK.E + TK.N), TK.NE),
        (re.compile(TK.W + TK.S), TK.SW),
        (re.compile(TK.E + TK.S), TK.SE),

    ) # end of ANCHORS



    # default XML attribute values
    # overrides RADXMLWidgetBase.ATTRS

    ATTRS = {

        "common": {
            "id": None,
        },

        "button": {
            "underline": None,
        },

        "checkbutton": {
            "underline": None,
        },

        "label": {
            "underline": None,
        },

        "listbox": {
            #~ "name": None,
            "class": None,
            "args": None,
            "module": None,
            "choices": None,
            "start": None,
            "layout": None,         # can be: None or pack|grid|place
            "layout_options": None, # pack_opts|grid_opts|place_opts
            "resizable": "no",      # can be: no|yes|width|height
        },

        "menubutton": {
            "underline": None,
        },

        "optionmenu": {
            #~ "name": None,
            "listvariable": None,
            "variable": None,
            "choices": None,
            "start": None,
            "layout": None,         # can be: None or pack|grid|place
            "layout_options": None, # pack_opts|grid_opts|place_opts
            "resizable": "no",      # can be: no|yes|width|height
        },

        "radiobutton": {
            "underline": None,
        },

        "tkwidget": {
        },

        "ttkbutton": {
            "underline": None,
        },

        "ttkcheckbutton": {
            "underline": None,
        },

        "ttklabel": {
            "underline": None,
        },

        "ttkmenubutton": {
            "underline": None,
        },

        "ttkradiobutton": {
            "underline": None,
        },

        "ttktab": {
            "sticky": "all",
            "underline": -1,
        },

        "widget": {
            #~ "name": None,
            "class": None,
            "args": None,
            "module": None,
            "layout": None,         # can be: None or pack|grid|place
            "layout_options": None, # pack_opts|grid_opts|place_opts
            "resizable": "no",      # can be: no|yes|width|height
        },

        "include": {
            #~ "name": None,
            "src": None,
            "xml_dir": None,
            "xml_filename": None,
            "xml_file_ext": None,
        },

        "module": {
            "from": None,
            "import": None,
            "as": None,
        },

        "configure": {
            "widget": None,
        },

        "layout": {
            "widget": None,
            "layout": "pack",       # can be: pack|grid|place
            "layout_options": None, # pack_opts|grid_opts|place_opts
            "resizable": "no",      # can be: no|yes|width|height
        },

        "event": {
            "signal": None,
            "slot": None,
        },

        "tkevent": {
            "widget": None,
            "bind": "bind", # can be: bind|bind_class|bind_all
            "class": None,
            "seq": None,  # tk event sequence: '<modifier-type-detail>'
            "slot": None, # slot event handler (method or function)
            "add": None,  # can be: None or '+' only
        },

    } # end of ATTRS



    # $ 2014-02-24 RS $
    # new support:
    # now TK and ttk are embedded in predefined classnames;

    CLASSES = {

        # tkinter native classes support

        "button":           "TK.Button",
        "canvas":           "TK.Canvas",
        "checkbutton":      "TK.Checkbutton",
        "entry":            "TK.Entry",
        "frame":            "TK.Frame",
        "label":            "TK.Label",
        "labelframe":       "TK.LabelFrame",
        "listbox":          "TK.Listbox",
        "menu":             "TK.Menu",
        "menubutton":       "TK.Menubutton",
        "message":          "TK.Message",
        "optionmenu":       "TK.OptionMenu",
        "panedwindow":      "TK.PanedWindow",
        "radiobutton":      "TK.Radiobutton",
        "scale":            "TK.Scale",
        "scrollbar":        "TK.Scrollbar",
        "spinbox":          "TK.Spinbox",
        "text":             "TK.Text",
        "toplevel":         "TK.Toplevel",

        # ttk additional classes support

        "ttkbutton":        "ttk.Button",
        "ttkcheckbutton":   "ttk.Checkbutton",
        "ttkcombobox":      "ttk.Combobox",
        "ttkentry":         "ttk.Entry",
        "ttkframe":         "ttk.Frame",
        "ttklabel":         "ttk.Label",
        "ttklabelframe":    "ttk.LabelFrame",
        "ttkmenubutton":    "ttk.Menubutton",
        "ttknotebook":      "ttk.Notebook",
        "ttkpanedwindow":   "ttk.PanedWindow",
        "ttkprogressbar":   "ttk.Progressbar",
        "ttkradiobutton":   "ttk.Radiobutton",
        "ttkscale":         "ttk.Scale",
        "ttkscrollbar":     "ttk.Scrollbar",
        "ttkseparator":     "ttk.Separator",
        "ttksizegrip":      "ttk.Sizegrip",
        "ttktab":           "ttk.Frame",
        "ttktreeview":      "ttk.Treeview",

    } # end of CLASSES



    # XML tree root element
    # overrides RADXMLBase.DOCTYPE

    DOCTYPE = "tkwidget"



    # accepted XML child elements for XML container element

    DTD = {

        "ttknotebook": ("ttktab", ),

        "widget": (
            "configure", "event", "include", "layout", "module",
            "style", "tkevent", "tkmenu", "ttkstyle", "ttktheme",
            "widget",
        ) + tuple(CLASSES.keys()),

    } # end of DTD


    # XML file path parts for xml_build() automatic mode
    # overrides RADXMLBase.XML_RC

    XML_RC = {

        "dir": "^/xml/widget",
        # do *NOT* define "filename" here
        "file_ext": ".xml",

    } # end of XML_RC



    # ------------------  XML elements building  -----------------------



    def _build_element_button (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_canvas (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_checkbutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        if xml_element.get("checked"):

            self.WIDGET.select()

        else:

            self.WIDGET.deselect()

        # end if

        return _ok

    # end def



    def _build_element_configure (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element <configure> acts like tkinter.w.configure()

            by parsing XML attributes as if they were

            config options e.g. tkinter.w.configure(**options)

            example:

            <configure widget="w_id" bg="red" relief="@FLAT".../>

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # try to retrieve concerned widget

            _widget = _attributes.get("widget", tk_parent)

            # try to configure widget (True=success, False=failure)

            return self._set_widget_config(_widget, self.TK_CONFIG)

        # end if

        # failed

        return False

    # end def



    def _build_element_entry (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_event (self, xml_tag, xml_element, tk_parent):
        r"""
            XML <event> element implements the code equivalence of

            get_event_manager().events.connect(signal, slot)

            events are always application-wide scope for RADWidgetBase

            subclasses and object children;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # connecting people :-)

            return self.events.connect(

                _attributes.get("signal"), _attributes.get("slot")
            )

        # end if

        # failed

        return False

    # end def



    def _build_element_frame (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_include (self, xml_tag, xml_element, tk_parent):
        r"""
            XML <include> element tries to include external XML file

            def for instant widget building at current insertion point;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # set inclusion widget

            _widget = RADXMLWidget(tk_owner = tk_parent, **_attributes)

            # ensure there won't be any unexpected inclusion /!\

            _widget.XML_RC.clear()

            # $ 2014-02-09 RS $
            # CAUTION:
            # removed self-inclusion security;
            # let Python handle this trap!

            # get XML tree

            _widget.xml_load(_attributes.get("src"))

            # include new XML tree to current one

            xml_element = _widget.get_xml_tree().getroot()

            # free useless memory right now /!\

            del _attributes, _widget

            # build inclusion

            return self._loop_on_children(

                xml_element, tk_parent, accept=self.DTD.get("widget")
            )

        # end if

        # failed

        return False

    # end def



    def _build_element_label (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_labelframe (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_layout (self, xml_tag, xml_element, tk_parent):
        r"""
            tries to set a layout to a given widget;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # try to retrieve concerned widget

            _widget = _attributes.get("widget", tk_parent)

            # set layout

            self._set_layout(_widget, _attributes, tk_parent)

            # succeeded

            return True

            # end if

        # end if

        # failed

        return False

    # end def



    def _build_element_listbox (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.is_tk_parent(tk_parent):

            # widget attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # class constructor args

            _args = str(_attributes.get("args", ""))

            if not _args.startswith("tk_parent"):

                _args = "tk_parent, " + _args

            # end if

            # widget class inits

            _widget = eval("TK.Listbox({args})".format(args = _args))

            # keep a copy aboard

            self._register_object_by_id(_widget, _attributes.get("id"))

            # set widget as class member

            self._set_class_member(_attributes.get("name"), _widget)

            # prepare list of choices

            _widget.delete(0, TK.END)

            # choices inits

            _choices = _attributes.get("choices")

            if _choices:

                # fill up widget's list of choices

                _widget.insert(0, *_choices)

                # startup inits

                _start = _attributes.get("start")

                if tools.is_num(_start):

                    if _start > 0:

                        _start = min(_start, len(_choices) - 1)

                    elif _start < 0:

                        _start = max(0, len(_choices) + _start)

                    # end if

                elif _start in _choices:

                    _start = _choices.index(_start)

                else:

                    _start = -1

                # end if

                # set selected line

                _widget.selection_anchor(_start)

                _widget.selection_set(_start)

                _widget.activate(_start)

                _widget.see(_start)

            # end if

            # tk configure()

            self._set_widget_config(_widget, self.TK_CONFIG)

            # set layout

            self._set_layout(_widget, _attributes, tk_parent)

            # succeeded

            return True

        # unsupported

        else:

            raise TypeError(

                _(
                    "Tkinter '{classname}' object is *NOT* "

                    "insertable into {obj_type} object."

                ).format(

                    classname =

                        xml_element.get("class", self.WIDGET_CLASS),

                    obj_type = repr(tk_parent)
                )
            )

            return False

        # end if

    # end def



    def _build_element_menu (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_element_tkmenu(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_menubutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_message (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_module (self, xml_tag, xml_element, tk_parent):
        r"""
            tries to import python libs along syntactic sugar:

            [from dottedURI ]import dottedURIStar[ as ALIAS]

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            _attrs = {

                "from": tools.str_complete(

                    "from {} ", _attributes.get("from")
                ),

                "import": tools.str_complete(

                    "import {}", _attributes.get("import")
                ),

                "as": tools.str_complete(

                    " as {}", _attributes.get("as")
                ),
            }

            # try to import python libs with global scope

            exec("{from}{import}{as}".format(**_attrs), globals())

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def _build_element_optionmenu (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.is_tk_parent(tk_parent):

            # widget attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # control variable inits

            _cvar = tools.choose(

                _attributes.get("listvariable"),

                # $ 2014-01-11 RS $

                # for retro-compatibility reasons:

                _attributes.get("variable"),

                TK.StringVar(),
            )

            # choices inits

            _choices = tools.choose(

                _attributes.get("choices"),

                [_("<empty>")],

                ["<empty>"],
            )

            # widget class inits

            _widget = TK.OptionMenu(tk_parent, _cvar, *_choices)

            # keep a copy aboard

            self._register_object_by_id(_widget, _attributes.get("id"))

            # set widget as class member

            self._set_class_member(_attributes.get("name"), _widget)

            # startup inits

            _start = _attributes.get("start")

            if tools.is_num(_start):

                if _start > 0:

                    _start = min(_start, len(_choices) - 1)

                elif _start < 0:

                    _start = max(0, len(_choices) + _start)

                # end if

                _start = _choices[_start]

            elif _start not in _choices:

                _start = _choices[0]

            # end if

            _cvar.set(str(_start))

            # set layout

            self._set_layout(_widget, _attributes, tk_parent)

            # succeeded

            return True

        # unsupported

        else:

            raise TypeError(

                _(
                    "Tkinter '{classname}' object is *NOT* "

                    "insertable into {obj_type} object."

                ).format(

                    classname =

                        xml_element.get("class", self.WIDGET_CLASS),

                    obj_type = repr(tk_parent)
                )
            )

            return False

        # end if

    # end def



    def _build_element_panedwindow (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_radiobutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        if xml_element.get("selected"):

            self.WIDGET.select()

        else:

            self.WIDGET.deselect()

        # end if

        return _ok

    # end def



    def _build_element_scale (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_scrollbar (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        # make connections

        _scrollbar = self.WIDGET

        _target = self.TK_CHILD_CONFIG.get("connect")

        if _target and _scrollbar:

            try:

                # connect vertically

                # $ 2014-02-27 RS $
                # bug fix:
                # be careful with w.cget("..."): *NOT* string objects!
                # but rather TclObj.index objects (!)

                if str(_scrollbar.cget("orient")) == "vertical":

                    _target.configure(yscrollcommand = _scrollbar.set)

                    _scrollbar.configure(command = _target.yview)

                # connect horizontally

                else:

                    _target.configure(xscrollcommand = _scrollbar.set)

                    _scrollbar.configure(command = _target.xview)

                # end if

            except:

                raise TypeError(

                    _(
                        "cannot connect widget {w_type} "

                        "of id '{w_id}' to scrollbar."

                    ).format(

                        w_type = type(_target),

                        w_id = xml_element.get("connect")
                    )
                ) from None

        # end if

        return _ok

    # end def



    def _build_element_spinbox (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_style (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widgets style building;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # remove XML attr id from dictionary

            _id = _attributes.pop("id", None)

            # register dictionary for XML attr 'style="style_id"'

            self._register_object_by_id(_attributes, _id)

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def _build_element_text (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_tkevent (self, xml_tag, xml_element, tk_parent):
        r"""
            XML <tkevent> element implements tkinter event bindings

            for a given tkinter widget;

            event binding level can be one of 'bind', 'bind_class' or

            'bind_all';

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # retrieve tkinter widget

            _widget = tools.choose(

                _attributes.get("widget"),

                tk_parent,
            )

            # init bindings

            _bind = tools.choose_str(_attributes.get("bind"))

            _seq = tools.choose_str(_attributes.get("seq"))

            _add = tools.choose_str(_attributes.get("add"))

            _slot = _attributes.get("slot")

            _method = getattr(_widget, _bind)

            # special case

            if _bind == "bind_class":

                _class = tools.choose_str(_attributes.get("class"))

                # bind event

                _method(_class, _seq, _slot, _add)

            else:

                # bind event

                _method(_seq, _slot, _add)

            # end if

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def _build_element_tkmenu (self, xml_tag, xml_element, tk_parent):
        r"""
            tkinter menu defs should be written apart from a classical

            <tkwidget> XML script into a <tkmenu> XML script;

            this method tries to do this for you by emulating

            @xml_element param as if it were a RADXMLMenu

            XML tree root node;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # lib imports

            from . import rad_xml_menu as XM

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # reset element tag

            xml_element.tag = "tkmenu"

            # widget inits

            _widget = XM.RADXMLMenu(tk_owner = tk_parent)

            # register widget

            self._register_object_by_id(_widget, _attributes.get("id"))

            # set widget as class member

            self._set_class_member(_attributes.get("name"), _widget)

            # reset XML tree

            _widget.set_xml_tree(element = xml_element)

            # build menu

            _ok = _widget.xml_build()

            # transfer all newly created stringvars
            # from menu to widget

            self.get_stringvars().update(_widget.get_stringvars())

            # confirm op

            return _ok

        # end if

        # failed

        return False

    # end def



    def _build_element_tkwidget (self, xml_tag, xml_element, tk_parent):
        r"""
            tries to integrate subelements directly in tk_parent

            without creating an intermediate widget;

            does not manage with XML attribute 'class' as

            tk_parent is considered to be already a tkinter

            widget subclass object;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.is_tk_parent(tk_parent):

            # loop on XML element children - build tk child widgets

            # accept only following XML subelements

            return self._loop_on_children(

                xml_element, tk_parent, accept=self.DTD.get("widget"),
            )

        # unsupported

        else:

            raise TypeError(

                _(
                    "Current tkinter object is *NOT* "

                    "insertable into {obj_type} object."

                ).format(obj_type = repr(tk_parent))
            )

            return False

        # end if

    # end def



    def _build_element_toplevel (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter native widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkbutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkcheckbutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        if xml_element.get("checked"):

            self.WIDGET.invoke()

        # end if

        return _ok

    # end def



    def _build_element_ttkcombobox (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkentry (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkframe (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttklabel (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttklabelframe (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkmenubutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttknotebook (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkpanedwindow (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkprogressbar (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkradiobutton (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        if xml_element.get("selected"):

            self.WIDGET.invoke()

        # end if

        return _ok

    # end def



    def _build_element_ttkscale (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkscrollbar (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_element_scrollbar(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkseparator (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttksizegrip (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttkstyle (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widgets style building;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # remove some XML attrs from dictionary

            _attributes.pop("id", None)

            _apply = _attributes.pop("apply", ".")

            # update ttk style defs

            _style = ttk.Style()    # see below /!\

            _style.configure(_apply, **_attributes)

            # CSS-like syntax

            if tools.is_pstr(xml_element.text):

                # CDATA inits

                _cdata = (
                    xml_element.text
                        # strip unwanted chars
                        .strip("\n\t ;")
                        # remove line ends
                        .replace("\n", "")
                        # convert double quotes to single quotes
                        .replace('"', "'")
                )

                # remove /* ... */ comments

                _cdata = re.sub(r"/\*.*?\*/", "", _cdata)

                # ttk root style is '.', CSS is '*'

                _cdata = _cdata.replace("*", ".")

                # get def chunks
                # i.e. elements {**attrs} elements {**attrs} ...

                _cdata = list(
                    filter(
                        None,
                        set(
                            re.split(r"(.*?\{.*?\})", _cdata)
                        )
                    )
                )

                for _def in _cdata:

                    # def chunks init i.e. elements { **attrs }

                    _elements, _attrs = _def.split("{")

                    # filter elements
                    # i.e. element:state:!state, element, ...
                    # element:state, new.old:state, ...

                    _elements = \
                        re.sub(r"[^\w,.!:]+", "", _elements).split(",")

                    # filter and parse XML attrs
                    # i.e. attr_key: value; ...
                    # --> {"attr_key": "value", ...}

                    _attrs = self._parse_xml_attributes(
                        xml_element,
                        tk_parent,
                        xml_attrs = eval(
                            "{{{}}}"
                            .format(
                                re.sub(
                                    r"\s*(\w+)\s*:\s*(.*?)\s*;",
                                    r'"\1":"\2",',
                                    _attrs.strip("{ };") + ";"
                                ).strip(";")
                            )
                        ),
                    )

                    # got attrs?

                    if tools.is_pdict(_attrs):

                        for _element in _elements:

                            # pseudo-format support
                            # i.e. element:state:!state:...

                            _element = _element.split(":")

                            # got mapping?

                            if len(_element) > 1:

                                # inits

                                _states = _element[1:]

                                _element = _element[0]

                                _mattrs = _attrs.copy()

                                for (_key, _value) in _mattrs.items():

                                    _map = _style.map(_element, _key)

                                    _map.insert(
                                        0, tuple(_states + [_value])
                                    )

                                    _mattrs[_key] = _map

                                # end for

                                _style.map(_element, **_mattrs)

                            # got configuring

                            else:

                                _style.configure(_element[0], **_attrs)

                            # end if

                        # end for

                    # end if

                # end for

            # end if

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def _build_element_ttktab (self, xml_tag, xml_element, tk_parent):
        r"""
            <ttktab> XML element is child of <ttknotebook>;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_ttktheme (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk theme building;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # attribute inits

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent
            )

            # use new theme, if any.

            ttk.Style().theme_use(_attributes.get("use"))

            return True

        # end if

        return False

    # end def



    def _build_element_ttktreeview (self, xml_tag, xml_element, tk_parent):
        r"""
            Tkinter ttk widget building;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def _build_element_widget (self, xml_tag, xml_element, tk_parent,
    **kw):
        r"""
            XML element <widget .../> is the generic XML declaration

            for any user-defined subclass of a native tkinter widget;

            example:

                <widget name="notepad123" class="MyOwnNotepad" .../>

            is slightly the same as:

                self.notepad123 = MyOwnNotepad(self, ...)

            with 'self' the parent widget (supported if omitted);

            returns True on build success, False otherwise;
        """

        # param controls

        if self.is_tk_parent(tk_parent):

            # widget attribute inits

            kw.update(addon_attrs = self.ATTRS.get("widget"))

            _attributes = self._init_attributes(

                xml_tag, xml_element, tk_parent, **kw
            )

            # widget class inits

            _class = eval("{module}{class}".format(**_attributes))

            _args = _attributes.get("args", "")

            # tk widget parent autocompletion

            if issubclass(_class, (TK.Widget, TK.Tk)) \
                                and not _args.startswith("tk_parent"):

                _args = "tk_parent, " + _args

            # end if

            # create tkinter widget

            _widget = eval("_class({args})".format(args = _args))

            # keep a copy aboard

            self._register_object_by_id(_widget, _attributes.get("id"))

            # keep a copy for specific post-implementations

            self.WIDGET = _widget

            # set widget as class member

            self._set_class_member(_attributes.get("name"), _widget)

            # configure widget

            self._set_widget_config(_widget, self.TK_CONFIG)

            # set layout

            self._set_layout(_widget, _attributes, tk_parent)

            # free useless memory right now /!\

            del _class, _args, self.TK_CONFIG

            # loop on XML element children - build tk child widgets

            _build_ok = self._loop_on_children(

                xml_element, _widget,

                accept = tools.choose(

                    self.DTD.get(xml_tag),

                    self.DTD.get("widget"),
                )
            )

            # widget init() procedure

            _init = _attributes.get("init")

            if callable(_init):

                kw.update(

                    widget = _widget,

                    parent = tk_parent,

                    xml_attributes = _attributes,
                )

                _init(**kw)

            # end if

            # succeeded

            return _build_ok

        # unsupported

        else:

            raise TypeError(

                _(
                    "Tkinter '{classname}' object is *NOT* "

                    "insertable into {obj_type} object."

                ).format(

                    classname =

                        xml_element.get("class", self.WIDGET_CLASS),

                    obj_type = repr(tk_parent)
                )
            )

            return False

        # end if

    # end def



    def _build_tk_native (self, xml_tag, xml_element, tk_parent):
        r"""
            protected method def;

            builds any tkinter native widget along its class name;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # param inits

            _cname = tools.choose_str(

                self.CLASSES.get(xml_tag),

                xml_tag,

                "Frame",
            )

            # $ 2014-02-24 RS $
            # new support:
            # now TK and ttk are embedded in predefined classnames;

            _cname = _cname.strip(".").split(".")

            _module = tools.choose_str(xml_element.get("module"))

            if len(_cname) > 1:

                _module = _cname[0] + "."

            # end if

            # set real classname

            xml_element.set("class", tools.normalize_id(_cname[-1]))

            # must force XML attr module name

            xml_element.set("module", _module)

            # build widget

            return self._build_element_widget(

                xml_tag,  xml_element,  tk_parent,
            )

        # end if

        # failed

        return False

    # end def



    def _ensure_string_value (self, attribute, **kw):
        r"""
            will set attr value at least an empty string of chars;

            no return value (void);
        """

        # param controls

        if self._is_unparsed(attribute):

            # parsed attribute inits

            attribute.value = tools.choose_str(

                attribute.value,

                kw.get("default"),
            )

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _init_attributes (self, xml_tag, xml_element, tk_parent, **kw):
        r"""
            parses @xml_element param XML attributes along @xml_tag

            param constraints and possible @kw["addon_attrs"];

            returns parsed XML attributes in a dict() object;
        """

        # inits

        _dicts = (

            # XML element's mandatory default attrs

            self.ATTRS.get(xml_tag),

            # 'common' XML attrs

            self.ATTRS.get("common"),

            # additional external XML attrs

            kw.get("addon_attrs"),

            # override with real XML attributes
            # (key/value) pairs

            xml_element.attrib,
        )

        _attributes = dict()

        # loop on dicts

        for _dict in _dicts:

            if tools.is_pdict(_dict):

                _attributes.update(_dict)

            # end if

        # end for

        # update keywords (filtered attributes)

        kw["xml_attrs"] = _attributes

        # return parsed XML attributes

        return self._parse_xml_attributes(xml_element, tk_parent, **kw)

    # end def



    def _layout_toplevel (self, widget, attrs, tk_parent):
        r"""
            sets Toplevel main window inits and layouts;

            no return value (void);
        """

        # window state inits

        _wstate = tools.choose_str(attrs.get("visibility"))

        _resizable = tools.choose_str(attrs.get("resizable"))

        # set transient window

        widget.transient(attrs.get("transient"))

        # set window's title

        widget.title(attrs.get("title"))

        # set window's min size

        widget.minsize(

            width = attrs.get("minwidth"),

            height = attrs.get("minheight"),
        )

        # set window's max size

        _maxwidth = attrs.get("maxwidth")

        _maxheight = attrs.get("maxheight")

        widget.maxsize(width = _maxwidth, height = _maxheight)

        # set resizable window

        widget.resizable(

            width = (_resizable in ("yes", "width")),

            height = (_resizable in ("yes", "height")),
        )

        # set window state

        if _wstate == "maximized" and _resizable == "yes" \
                                    and not (_maxwidth or _maxheight):

            widget.deiconify()

            widget.attributes("-zoomed", "1")

        elif _wstate == "minimized":

            widget.iconify()

        elif _wstate == "hidden":

            widget.withdraw()

        else:

            # 'normal' window state (default)

            widget.deiconify()

        # end if

    # end def



    # -----------------------  XML attributes parsing  -----------------



    def _parse_attr__after (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def _parse_attr__before (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def _parse_attr__height (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr__minsize (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr__padx (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr__pady (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr__sticky (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # inits

            _sticky = attribute.value.lower()

            if not set(_sticky).issubset(set(self.STICKY_ALL)):

                _sticky = self.STICKY_ALL

            # end if

            # parsed attribute inits

            attribute.value = _sticky

            kw.update(tk_child_config = True)

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _parse_attr__width (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_activerelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_activestyle (self, attribute, **kw):
        r"""
            must be one of 'underline', 'dotbox', 'none';

            default value is 'underline';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "dotbox",

            values = ("underline", "none"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_add (self, attribute, **kw):
        r"""
            filters XML attr 'add' along authorized values;

            must be at least an empty string of chars;

            no return value (void);
        """

        # param controls

        if tools.is_pstr(attribute.value):

            # force value

            _add = "+"

        else:

            # at least empty string

            _add = ""

        # end if

        # parsed attribute inits

        attribute.value = _add

        # caution: *NO* self._tk_config() by here /!\

    # end def



    def _parse_attr_after (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr__after(attribute, **kw)

    # end def



    def _parse_attr_anchor (self, attribute, **kw):
        r"""
            many location supports;
            supports 'north', 'top' or 'up' for TK.N;
            supports 'south', 'bottom' or 'down' for TK.S;
            supports 'east' or 'right' for TK.E;
            supports 'west' or 'left' for TK.W;
            supports 'center' for TK.CENTER;
            supports any consistent combination of above values  for
            TK.NW, TK.NE, TK.SW and TK.SE, of course, e.g:
            anchor="top left" or anchor="down right", etc;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # inits

            _anchor = attribute.value

            # loop on regexps

            for (_search, _replace) in self.ANCHORS:

                _anchor = _search.sub(_replace, _anchor)

            # end for

            # set inconsistencies to default value: 'center'

            if _anchor not in (TK.N, TK.S, TK.E, TK.W,
                                            TK.NW, TK.NE, TK.SW, TK.SE):

                _anchor = TK.CENTER

            # end if

            # parsed attribute inits

            attribute.value = _anchor

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _parse_attr_apply (self, attribute, **kw):
        r"""
            XML attr for '<ttkstyle apply="newName.oldName".../>';

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = re.sub(r"[^\w\.]+", r"", attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_args (self, attribute, **kw):
        r"""
            class constructor arguments e.g. MyClass(**args);

            replaces "self" or "parent" defs with the correct parent

            definition;

            replaces "@" aliases with module name ref e.g.

            "orient=@VERTICAL" becomes "orient=TK.VERTICAL" in args

            if widget's module name is "TK", of course;

            no return value (void);
        """

        # param controls - force to "" otherwise /!\

        if tools.is_pstr(attribute.value):

            # replace eventual "self" or "parent" by correct param name

            _args = re.sub(

                r"(?i)\b(?:self|parent)\b",

                "tk_parent",

                attribute.value
            )

            # replace "@" alias in value by a ref to widget's module

            _args = self._replace_alias(_args, **kw)

        else:

            # minimal default value

            _args = ""

        # end if

        # parsed attribute inits

        attribute.value = _args

        # caution: *NO* self._tk_config() by here /!\

    # end def



    def _parse_attr_as (self, attribute, **kw):
        r"""
            conforms XML attr 'as' to language specs __identifier__;

            accepts only regexp("\w+") in fact;

            no return value (void);
        """

        # parsed attribute inits

        attribute.value = tools.normalize_id(attribute.value)

        # caution: *NO* self._tk_config() by here /!\

    # end def



    def _parse_attr_aspect (self, attribute, **kw):
        r"""
            attr 'aspect' ratio (integer);

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_autoseparators (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_before (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr__before(attribute, **kw)

    # end def



    def _parse_attr_bind (self, attribute, **kw):
        r"""
            must be one of 'bind', 'bind_class' or 'bind_all';

            default value is 'bind';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "bind",

            values = ("bind_class", "bind_all"),

            # caution: *NO* self._tk_config() by here /!\

            no_tk_config = True,
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_buttonbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_buttoncursor (self, attribute, **kw):
        r"""
            cursor attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cursor_support(attribute, **kw)

    # end def



    def _parse_attr_buttondownrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_buttonup (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_choices (self, attribute, **kw):
        r"""
            changes string list of compound values to a well-formed
            list() of string values;

            string values *MUST* be quoted;

            list of values *MUST* be comma-separated;

            example:

                choices="'hello', 'good people', 123, 456.78"

            will become

                choices = ['hello', 'good people', '123', '456.78']

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = list(

                map(

                    str,

                    eval(

                        "[{}]".format(attribute.value.strip("()[]{}"))
                    )
                )
            )

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_class (self, attribute, **kw):
        r"""
            forces XML attr 'class' name to conform to __identifier__

            language semantics def i.e. accept only regexp("\w+");

            no return value (void);
        """

        # param controls - forces value clean-ups

        if self._is_unparsed(attribute):

            # param inits

            _class = tools.choose_str(

                tools.normalize_id(attribute.value),

                self.WIDGET_CLASS,

                "Frame",
            )

            # parsed attribute inits

            attribute.value = _class

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_class_ (self, attribute, **kw):
        r"""
            fake classname for tkinter options database;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _parse_attr_closeenough (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def _parse_attr_columns (self, attribute, **kw):
        r"""
            values attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr_values(attribute, **kw)

    # end def



    def _parse_attr_confine (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_connect (self, attribute, **kw):
        r"""
            scrollbar attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def _parse_attr_default (self, attribute, **kw):
        r"""
            state attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_state_support(attribute, **kw)

    # end def



    def _parse_attr_digits (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_direction (self, attribute, **kw):
        r"""
            sets Menubutton pop-up menu showing up direction;

            must be one of 'above', 'below', 'flush', 'left' or
            'right';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "below",

            values = ("above", "flush", "left", "right"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_disabledbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_displaycolumns (self, attribute, **kw):
        r"""
            values attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr_values(attribute, **kw)

    # end def



    def _parse_attr_elementborderwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_exportselection (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_format (self, attribute, **kw):
        r"""
            sprintf() format e.g. '%02.3f';

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # inits

            _fmt = re.search(

                r"\D*(\d*\.\d+)|\D*(\d*)", attribute.value
            )

            if _fmt:

                _fmt = tools.str_complete(

                    "%{}f",

                    "".join(filter(None, _fmt.groups()))
                )

            # end if

            # parsed attribute inits

            attribute.value = _fmt

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _parse_attr_from (self, attribute, **kw):
        r"""
            from relative.module import ...;

            parse relative.module string value;

            no return value (void);
        """

        # param controls - forces value clean-ups

        if self._is_unparsed(attribute):

            # parsed attribute inits

            attribute.value = \
                tools.normalize_relative_module(attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_from_ (self, attribute, **kw):
        r"""
            starting point float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def _parse_attr_handlepad (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_handlesize (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_height (self, attribute, xml_tag, **kw):
        r"""
            integer/dimension attribute along widget type;

            no return value (void);
        """

        # param controls

        if xml_tag in ("button", "checkbutton", "label", "listbox",
        "menubutton", "radiobutton", "text"):

            # parsed attribute inits

            self._tkRAD_integer_support(attribute, **kw)

        else:

            # parsed attribute inits

            self._tkRAD_dimension_support(attribute, **kw)

        # end if

    # end def



    def _parse_attr_highlightbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_highlightcolor (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_highlightthickness (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_import (self, attribute, **kw):
        r"""
            from ... import module;

            parses module string value;

            no return value (void);
        """

        # param controls - forces value clean-ups

        if self._is_unparsed(attribute):

            # parsed attribute inits

            attribute.value = tools.normalize_import(attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_increment (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def _parse_attr_indicatorcolor (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_indicatoron (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_init (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_insertbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_insertborderwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_insertofftime (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_insertontime (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_insertwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_invalidcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_jump (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_justify (self, attribute, **kw):
        r"""
            must be one of 'left', 'right', 'center';

            default value is 'center';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "center",

            values = ("left", "right"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_label (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def _parse_attr_labelanchor (self, attribute, **kw):
        r"""
            anchor attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr_anchor(attribute, **kw)

    # end def



    def _parse_attr_labelwidget (self, attribute, **kw):
        r"""
            widget attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def _parse_attr_layout (self, attribute, **kw):
        r"""
            must be one of 'pack', 'grid', 'place' or 'none';

            default value is 'none' (no layout);

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "none",

            values = ("pack", "grid", "place"),

            # caution: *NO* self._tk_config() by here /!\

            no_tk_config = True,
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_layout_options (self, attribute, **kw):
        r"""
            'pack', 'grid' or 'place' layout options;

            no return value (void);
        """

        # param controls

        if self._is_unparsed(attribute):

            _lopts = attribute.value

            if tools.is_pstr(_lopts):

                # replace "@" alias by a ref to widget's module

                _lopts = self._replace_alias(_lopts, **kw)

                # layout options must be a dict() of options

                # for self._set_layout() and self._set_resizable()

                _lopts = eval("dict({})".format(_lopts.strip("()[]{}")))

            elif not tools.is_pdict(_lopts):

                # minimal default value

                _lopts = dict()

            # end if

            # parsed attribute inits

            attribute.value = _lopts

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_length (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_listvariable (self, attribute, **kw):
        r"""
            control variable attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cvar_support(attribute, **kw)

    # end def



    def _parse_attr_maxheight (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_maximum (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_maxundo (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_maxwidth (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_minheight (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_minsize (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr__minsize(attribute, **kw)

    # end def



    def _parse_attr_minwidth (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_mode (self, attribute, **kw):
        r"""
            must be one of 'indeterminate', 'determinate';

            default value is 'determinate';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "determinate",

            values = ("indeterminate", ),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_module (self, attribute, **kw):
        r"""
            tries to determine module's correct alias name;

            no return value (void);
        """

        # $ 2014-01-09 RS $
        # bug fix:
        # @attribute may be None sometimes;

        if self._is_new(attribute):

            # module id inits

            _module = attribute.value.lstrip(".")

            # predefined module name?

            if _module.endswith("."):

                # init module name

                _name = _module

            # XML source module id

            else:

                # init module name

                _name = ""

                # try to get <module> element for more info

                _module = self.get_element_by_id(_module)

                # found corresponding <module> element?

                if self.is_element(_module):

                    # attribute inits

                    _import = \
                        tools.normalize_import(_module.get("import"))

                    # choose between attrs

                    if _import != "*":

                        _name = tools.choose_str(

                            tools.normalize_id(_module.get("as")),

                            _import,

                        ) + "."

                    # end if

                # module not found

                else:

                    raise KeyError(
                        _(
                            "module of id '{mid}' has *NOT* been found."

                        ).format(mid = attribute.value)
                    )

                # end if

            # end if

            # parsed attribute inits

            attribute.value = _name.lstrip(".")

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_offrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_opaqueresize (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_orient (self, attribute, attrs, xml_tag, **kw):
        r"""
            must be one of 'vertical', 'horizontal';

            default value is 'vertical';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "vertical",

            values = ("horizontal", ),
        )

        self._fix_values(attribute, **kw)

        # $ 2014-02-27 RS $
        # special case for ttk.PanedWindow

        if xml_tag == "ttkpanedwindow" and "args" in attrs:

            # in a ttk.PanedWindow object:
            # must init 'orient' attr in class constructor's 'args'
            # because 'orient' is *READ-ONLY* in configure()

            _args = tools.choose_str(attrs["args"]).split(",")

            _args.append("orient='{}'".format(attribute.value))

            attrs["args"] = ",".join(filter(None, _args))

            self.TK_CONFIG.pop("orient", None)

        # end if

    # end def



    def _parse_attr_overrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_padding (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_padx (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_pady (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_readonlybackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_repeatdelay (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_repeatinterval (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_resizable (self, attribute, **kw):
        r"""
            must be one of 'yes', 'no', 'width', 'height';

            default value is 'no';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "no",

            values = ("yes", "width", "height"),

            # caution: *NO* self._tk_config() by here /!\

            no_tk_config = True,
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_resolution (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def _parse_attr_sashpad (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_sashrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_sashwidth (self, attribute, **kw):
        r"""
            dimension attribute

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_scrollregion (self, attribute, **kw):
        r"""
            must be a 4-tuple of integers;

            values are (left, top, right, bottom);

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = tuple(

                map(

                    tools.ensure_int,

                    eval(

                        "[{}]".format(attribute.value.strip("(){}[]"))
                    )
                )
            )

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _parse_attr_selectbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_selectborderwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_selectforeground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_selectmode (self, attribute, xml_tag, **kw):
        r"""
            must be one of 'browse', 'single', 'multiple', 'extended';

            default value is 'browse';

            no return value (void);
        """

        # parsed attribute inits

        # $ 2014-02-27 RS $
        # new support:
        # ttk.Treeview hasn't
        # the same point of view!

        if xml_tag == "ttktreeview":

            kw.update(

                default = "extended",

                values = ("none", "browse"),
            )

        else:

            kw.update(

                default = "browse",

                values = ("single", "multiple", "extended"),
            )

        # end if

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_seq (self, attribute, **kw):
        r"""
            admits simplified tkinter.Event sequence (no <>);

            e.g. seq="Control-s" instead of seq="&lt;Control-s&gt;";

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # inits - stri

            _seq = attribute.value.replace("<", "", 1)

            _seq = _seq.replace(">", "", 1)

            # parsed attribute inits

            attribute.value = "<" + _seq + ">"

            # CAUTION: *NO* self.tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_show (self, attribute, xml_tag, **kw):
        r"""
            password echo character to show in entry box;

            headings/tree ttk.Treeview display off mode;

            no return value (void);
        """

        # parsed attribute inits

        # $ 2014-02-27 RS $
        # new support:
        # ttk.Treeview hasn't
        # the same point of view!

        if xml_tag == "ttktreeview":

            kw.update(

                default = "headings",

                values = ("tree", ),
            )

            self._fix_values(attribute, **kw)

        else:

            self._tkRAD_any_value_support(attribute, **kw)

        # end if

    # end def



    def _parse_attr_showhandle (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_showvalue (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_signal (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._ensure_string_value(attribute, **kw)

    # end def



    def _parse_attr_sliderlength (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_sliderrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_slot (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_spacing1 (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_spacing2 (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_spacing3 (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_src (self, attribute, **kw):
        r"""
            normalizes path in XML attr 'src';

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = path.normalize(attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_start (self, attribute, **kw):
        r"""
            defines starting point for attr 'choices' items list;

            can be either litteral value or '@integer' list index
            position;

            admits negative index values;

            example: start="@0" will indicate choices[0];

            example: start="@-1" will indicate choices[-1];

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # starting point inits

            _start = attribute.value

            # got indexed integer value?

            if _start.startswith("@"):

                _start = tools.ensure_int(_start.lstrip("@"))

            else:

                # make some string clean-ups

                _start = re.sub(r"\\([@'])", r"\1", _start)

            # end if

            # parsed attribute inits

            attribute.value = _start

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_state (self, attribute, xml_tag, **kw):
        r"""
            must be one of 'normal' or 'disabled';

            must be one of 'normal', 'disabled' or 'readonly' when
            XML element is one of 'entry', 'spinbox';

            default value is 'normal';

            no return value (void);
        """

        # $ 2014-01-16 RS $
        # new support:
        # special case for '<entry>' and '<spinbox>':

        if xml_tag in ("entry", "spinbox"):

            _values = ("disabled", "readonly", )

        else:

            _values = ("disabled", )

        # end if

        # parsed attribute inits

        kw.update(default = "normal", values = _values)

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_sticky (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr__sticky(attribute, **kw)

    # end def



    def _parse_attr_style (self, attribute, **kw):
        r"""
            tkinter/ttk XML attr style def;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # style id inits

            _style = attribute.value

            if "." not in _style:

                _style = self.get_object_by_id(_style, _style)

            # end if

            # parsed attribute inits

            attribute.value = _style

            self._tk_config(attribute)

        # end if

    # end def



    def _parse_attr_tabs (self, attribute, **kw):
        r"""
            choices attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr_choices(attribute, **kw)

        self._tk_config(attribute, **kw)

    # end def



    def _parse_attr_takefocus (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_text (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def _parse_attr_textvariable (self, attribute, **kw):
        r"""
            control variable attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cvar_support(attribute, **kw)

    # end def



    def _parse_attr_tickinterval (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def _parse_attr_title (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def _parse_attr_to (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def _parse_attr_transient (self, attribute, **kw):
        r"""
            widget attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def _parse_attr_troughcolor (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_undo (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_use (self, attribute, **kw):
        r"""
            must be one of ttk.Style().theme_use() list;

            default value is 'default';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "default",

            values = ttk.Style().theme_names(),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_validate (self, attribute, **kw):
        r"""
            must be one of 'focus', 'focusin', 'focusout', 'key',
            'all' or 'none';

            default value is 'none';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "none",

            values = ("focus", "focusin", "focusout", "key", "all"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_validatecommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_values (self, attribute, **kw):
        r"""
            choices attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._parse_attr_choices(attribute, **kw)

        self._tk_config(attribute, **kw)

    # end def



    def _parse_attr_visibility (self, attribute, **kw):
        r"""
            must be one of 'normal', 'maximized', 'minimized' or
            'hidden';

            default value is 'normal';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            no_tk_config = True,

            default = "normal",

            values = ("maximized", "minimized", "hidden"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_weight (self, attribute, **kw):
        r"""
            ttk.PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_width (self, attribute, xml_tag, **kw):
        r"""
            integer/dimension attribute along widget type;

            no return value (void);
        """

        # param controls

        if xml_tag in ("button", "checkbutton", "entry", "label",
        "listbox", "menubutton", "radiobutton", "spinbox", "text"):

            # parsed attribute inits

            self._tkRAD_integer_support(attribute, **kw)

        else:

            # parsed attribute inits

            self._tkRAD_dimension_support(attribute, **kw)

        # end if

    # end def



    def _parse_attr_wrap (self, attribute, xml_tag, **kw):
        r"""
            boolean attribute;

            must be 'char', 'word' or 'none' if XML element is 'text';

            no return value (void);
        """

        # parsed attribute inits

        if xml_tag == "text":

            kw.update(

                default = "none",

                values = ("char", "word"),
            )

            self._fix_values(attribute, **kw)

        else:

            self._tkRAD_boolean_support(attribute, **kw)

        # end if

    # end def



    def _parse_attr_wraplength (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_xml_dir (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            no_tk_config = True,

            default = self.XML_RC.get("dir")
        )

        self._ensure_string_value(attribute, **kw)

    # end def



    def _parse_attr_xml_file_ext (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            no_tk_config = True,

            default = self.XML_RC.get("file_ext")
        )

        self._ensure_string_value(attribute, **kw)

    # end def



    def _parse_attr_xml_filename (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._ensure_string_value(attribute, **kw)

    # end def



    def _parse_attr_xscrollcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_xscrollincrement (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_yscrollcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_yscrollincrement (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _replace_alias (self, str_value, attrs, **kw):
        r"""
            protected method def;

            tries to retrieve widget's module alias name and

            replaces '@' module alias in XML attribute's value;

            returns parsed string of chars on success,

            empty string otherwise;
        """

        # param controls

        if tools.is_pstr(str_value):
            r"""
                $ 2013-12-18 RS $
                new support: attrs = RADXMLAttributesDict by now;
            """

            # try to get widget's module

            self._parse_attr_module(attrs.get_item("module"), **kw)

            # replace "@" alias in string of chars
            # by a ref to widget's module

            return str_value.replace("@", attrs.get("module", ""))

        # end if

        # unsupported - empty string

        return ""

    # end def



    def _set_layout (self, widget, attrs, tk_parent):
        r"""
            protected method def;

            pack(), grid() or place() tkinter widget;

            supports XML attribute 'resizable' horizontally, vertically

            or both axis;

            no return value (void);
        """

        # $ 2014-01-17 RS $
        # special case of Toplevel window

        if isinstance(widget, TK.Toplevel):

            # Toplevel window layout inits

            self._layout_toplevel(widget, attrs, tk_parent)

        # $ 2014-02-27 RS $
        # special case of ttk.Notebook children

        elif isinstance(tk_parent, ttk.Notebook):

            # add child instead of laying it out

            tk_parent.add(

                widget,

                **tools.dict_only_keys(
                    attrs, "compound", "image", "padding", "sticky",
                    "text", "underline",
                )
            )

        # $ 2014-02-27 RS $
        # special case of ttk.PanedWindow children

        elif isinstance(tk_parent, ttk.PanedWindow):

            # add child instead of laying it out

            tk_parent.add(

                widget, weight=self.TK_CHILD_CONFIG.get("weight")
            )

        # $ 2014-01-15 RS $
        # special case of PanedWindow children

        elif isinstance(tk_parent, TK.PanedWindow):

            # got to lay out?

            if attrs.get("layout") in ("pack", "grid", "place"):

                # init resizable

                _sticky = {

                    "width": TK.E + TK.W,

                    "height": TK.N + TK.S,

                    "yes": TK.N + TK.S + TK.E + TK.W,

                }.get(attrs.get("resizable"))

                self.TK_CHILD_CONFIG.setdefault("sticky", _sticky)

                # add child instead of laying it out

                tk_parent.add(widget, **self.TK_CHILD_CONFIG)

            # end if

        # widget exists and layout is asked?

        elif hasattr(widget, str(attrs.get("layout"))):

            # try to make widget resizable along params

            self._set_resizable(widget, attrs, tk_parent)

            # lay widget out

            exec("widget.{layout}(**{layout_options})".format(**attrs))

        # end if

    # end def



    def _set_resizable (self, widget, attrs, tk_parent):
        r"""
            protected method def;

            tries to set up tkinter widget's layout resizable along

            XML attribute 'resizable' either horizontally, vertically

            or both axis;

            no return value (void);
        """

        # param inits

        _resizable = tools.choose_str(

            attrs.get("resizable"),

            "no",

        ).lower()

        # layout method init

        _layout = attrs.get("layout")

        # layout options init

        _lopts = attrs.get("layout_options", dict())

        # param controls

        if _layout and _resizable in ("yes", "width", "height"):

            # pack() method

            if _layout == "pack":

                # option inits

                _lopts.update(

                    {

                        "yes": dict(expand=1, fill=TK.BOTH),

                        "width": dict(expand=0, fill=TK.X),

                        "height": dict(expand=1, fill=TK.Y),

                    }.get(_resizable)
                )

            # grid() method

            elif _layout == "grid":

                # option inits

                _lopts["sticky"] = {

                    "width": TK.W + TK.E,

                    "height": TK.N + TK.S,

                }.get(_resizable, self.STICKY_ALL)

                # column configure

                if _resizable in ("yes", "width"):

                    # make parent's column resizable

                    tk_parent.columnconfigure(

                        tools.ensure_int(_lopts.get("column", 0)),

                        weight = 1
                    )

                # end if

                # row configure

                if _resizable in ("yes", "height"):

                    # make parent's row resizable

                    tk_parent.rowconfigure(

                        tools.ensure_int(_lopts.get("row", 0)),

                        weight = 1
                    )

                # end if

            # place() method

            elif _layout == "place":

                # option inits

                _lopts.update(

                    {

                        "yes": dict(relwidth=1, relheight=1),

                        "width": dict(relwidth=1, relheight=None),

                        "height": dict(relwidth=None, relheight=1),

                    }.get(_resizable)
                )

            # end if

        # end if

        # update layout options

        attrs["layout_options"] = _lopts

    # end def



    def _set_widget_config (self, widget, config):
        r"""
            protected method def;

            tries to set up tkinter @widget's attributes along with
            @config param;

            returns True on success, False otherwise;
        """

        # param controls

        if hasattr(widget, "configure") and isinstance(config, dict):

            # $ 2014-02-25 RS $
            # New support:
            # style profile default inits

            _attrs = config.get("style")

            if not tools.is_pdict(_attrs):

                _attrs = dict()

            # end if

            # override with XML element specific XML attr defs

            _attrs.update(config)

            # got tk configure() attrs?

            if tools.is_pdict(widget.configure()):

                # filter TK attrs along with configure() keys

                _attrs = tools.dict_only_keys(

                    _attrs, *widget.configure().keys()
                )

            # end if

            # configure widget

            widget.configure(**_attrs)

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def


# end class RADXMLWidget
