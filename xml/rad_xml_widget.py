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

from ..core import tools

from ..core import uri

from . import rad_xml_widget_base as RB



class RADXMLWidget (RB.RADXMLWidgetBase):
    r"""
        main class for XML to tkinter widget building;

        this is THE tkinter widget MAIN building processor;

        supports tkinter natives in XML script;

        e.g. <button id="" text="OK" command="@OKClicked" .../>

        supports user-defined specific widgets in XML script;

        e.g. <widget id="" class="MyClassName" .../>

        supports on-the-fly module imports;

        e.g. <module import="tkinter" as="TK"/>

        and many, many other features (see doc for more);
    """



    ANCHORS = (

        (r"(?i)north|top|up", TK.N),
        (r"(?i)south|bottom|down", TK.S),
        (r"(?i)east|right", TK.E),
        (r"(?i)west|left", TK.W),
        (r"\W+", r""),
        (TK.N + "+", TK.N),
        (TK.S + "+", TK.S),
        (TK.E + "+", TK.E),
        (TK.W + "+", TK.W),
        (TK.W + TK.N, TK.NW),
        (TK.E + TK.N, TK.NE),
        (TK.W + TK.S, TK.SW),
        (TK.E + TK.S, TK.SE),
    )



    # overrides RADXMLWidgetBase.ATTRS

    # default XML attribute values

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

            "name": None,

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

            "name": None,

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


        "widget": {

            "name": None,

            "class": None,

            "args": None,

            "module": None,

            "layout": None,         # can be: None or pack|grid|place

            "layout_options": None, # pack_opts|grid_opts|place_opts

            "resizable": "no",      # can be: no|yes|width|height
        },


        "include": {

            "name": None,

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



    CLASSES = {

        "button":           "Button",
        "canvas":           "Canvas",
        "checkbutton":      "Checkbutton",
        "entry":            "Entry",
        "frame":            "Frame",
        "label":            "Label",
        "labelframe":       "LabelFrame",
        "listbox":          "Listbox",
        "menu":             "Menu",
        "menubutton":       "Menubutton",
        "message":          "Message",
        "optionmenu":       "OptionMenu",
        "panedwindow":      "PanedWindow",
        "radiobutton":      "Radiobutton",
        "scale":            "Scale",
        "scrollbar":        "Scrollbar",
        "spinbox":          "Spinbox",
        "text":             "Text",
        "toplevel":         "Toplevel",

    } # end of CLASSES



    # accepted XML child elements for XML key parent element

    DTD = {

        "widget": (

            "module", "widget", "include", "configure",

            "layout", "event", "tkevent", "tkmenu",

        ) + tuple(CLASSES.keys()),

    } # end of DTD



    # overrides RADXMLBase.XML_RC

    XML_RC = {

        "dir": "^/xml/widget",

        "file_ext": ".xml",

    } # end of XML_RC



    # ------------------  XML elements building  -----------------------



    def _build_tk_native (self, xml_tag, xml_element, tk_parent):
        r"""
            protected method def;

            builds any tkinter native widget along its class name;

            returns True on build success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # param inits

            xml_element.set(

                "class",

                self.CLASSES.get(xml_tag, xml_tag.capitalize())
            )

            # already import'ed tkinter as TK for tkinter natives /!\

            xml_element.set("module", xml_element.get("module", "TK."))

            # build widget by faking xml_tag = "widget"

            return self.build_element_widget(

                "widget",  xml_element,  tk_parent,

                addon_attrs=self.ATTRS.get(xml_tag, dict()),
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

        _attributes = self.ATTRS.get(xml_tag, dict()).copy()

        # add 'common' attrs

        _attributes.update(self.ATTRS.get("common", dict()))

        # add more default attrs

        _attributes.update(kw.get("addon_attrs", dict()))

        # override with real XML attributes (key/value) pairs

        _attributes.update(xml_element.attrib)

        # update keywords (filtered attributes)

        kw["xml_attrs"] = _attributes

        # return parsed XML attributes

        return self.parse_xml_attributes(xml_element, tk_parent, **kw)

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

            self.parse_attr_module(attrs.get_item("module"), **kw)

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

        # $ 2014-01-15 RS $
        # special case of PanedWindow

        if isinstance(tk_parent, TK.PanedWindow):

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



    def build_element_button (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <button name="btn_ok" text="OK" bg="red"/>

            is slightly the same as:

                self.btn_ok = Button(self, text="OK", bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_canvas (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <canvas name="my_canvas" bg="red"/>

            is slightly the same as:

                self.my_canvas = Canvas(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_checkbutton (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <checkbutton name="my_chkbtn" bg="red"/>

            is slightly the same as:

                self.my_chkbtn = Checkbutton(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        if hasattr(self.WIDGET, "select") \
                                        and xml_element.get("checked"):

            self.WIDGET.select()

        # end if

        return _ok

    # end def



    def build_element_configure (self, xml_tag, xml_element, tk_parent):
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

            # widget exists and is configurable?

            if hasattr(_widget, "configure"):

                # configure widget

                _widget.configure(**self.TK_CONFIG)

                # succeeded

                return True

            # end if

        # end if

        # failed

        return False

    # end def



    def build_element_entry (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <entry name="my_entry" bg="red"/>

            is slightly the same as:

                self.my_entry = Entry(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_event (self, xml_tag, xml_element, tk_parent):
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



    def build_element_frame (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <frame name="my_frame" bg="red"/>

            is slightly the same as:

                self.my_frame = Frame(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_include (self, xml_tag, xml_element, tk_parent):
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

            # be careful of infinite self-inclusion (recursions) /!\

            _src = _attributes.get("src")

            if self.get_xml_uri() == _widget.get_xml_uri(_src):

                raise OSError(

                    _(
                        "XML file self-inclusion is *NOT* allowed. "

                        "Will cause infinite recursions."
                    )
                )

                return False

            # end if

            # get XML tree

            _widget.xml_load(_src)

            # include new XML tree to current one

            xml_element = _widget.get_xml_tree().getroot()

            # free useless memory right now /!\

            del _attributes, _widget, _src

            # build inclusion

            return self.loop_on_children(

                xml_element, tk_parent, accept=self.DTD.get("widget")
            )

        # end if

        # failed

        return False

    # end def



    def build_element_label (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <label name="my_label" bg="red"/>

            is slightly the same as:

                self.my_label = Label(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_labelframe (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <labelframe name="my_lf" bg="red"/>

            is slightly the same as:

                self.my_lf = LabelFrame(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_layout (self, xml_tag, xml_element, tk_parent):
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



    def build_element_listbox (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <listbox name="my_listbox" bg="red"/>

            is slightly the same as:

                self.my_listbox = Listbox(self, bg="red")

            with 'self' the parent widget;

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

            self.register_object_by_id(_widget, _attributes.get("id"))

            # set widget as parent class member

            exec("tk_parent.{name} = _widget".format(**_attributes))

            # tk configure()

            if self.TK_CONFIG:

                _widget.configure(**self.TK_CONFIG)

            # end if

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



    def build_element_menu (self, xml_tag, xml_element, tk_parent):
        r"""
            tkinter menu defs should be written apart from a classical

            <tkwidget> XML script into a <tkmenu> XML script;

            this method tries to do this for you by emulating

            @xml_element param as if it were a RADXMLMenu

            XML tree root node;

            returns True on build success, False otherwise;
        """

        return self.build_element_tkmenu(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_menubutton (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <menubutton name="my_mb" bg="red"/>

            is slightly the same as:

                self.my_mb = Menubutton(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_message (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <message name="my_msg" bg="red"/>

            is slightly the same as:

                self.my_msg = Message(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_module (self, xml_tag, xml_element, tk_parent):
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



    def build_element_optionmenu (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is QUITE SPECIFIC by here;

            example:

                <optionmenu
                    name="my_om"
                    variable="myvar"
                    choices="'hello', 'good people', 123, 456.78"
                    start="@2"
                />

            will do the same as:

                _cvar = get_stringvar("myvar")

                _choices = get_choices()

                parent.my_om = OptionMenu(parent, _cvar, *_choices)

                _cvar.set(str(_choices[2]))

            with 'parent' the parent widget;

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

            self.register_object_by_id(_widget, _attributes.get("id"))

            # set widget as parent class member

            exec("tk_parent.{name} = _widget".format(**_attributes))

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



    def build_element_panedwindow (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <panedwindow name="my_pw" bg="red"/>

            is slightly the same as:

                self.my_pw = PanedWindow(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_radiobutton (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <radiobutton name="my_rb" bg="red"/>

            is slightly the same as:

                self.my_rb = Radiobutton(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        _ok = self._build_tk_native(xml_tag, xml_element, tk_parent)

        if hasattr(self.WIDGET, "select") \
                                        and xml_element.get("selected"):

            self.WIDGET.select()

        # end if

        return _ok

    # end def



    def build_element_scale (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <scale name="my_scale" bg="red"/>

            is slightly the same as:

                self.my_scale = Scale(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_scrollbar (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <scrollbar name="my_scrollbar" bg="red"/>

            is slightly the same as:

                self.my_scrollbar = Scrollbar(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_spinbox (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <spinbox name="my_spbx" bg="red"/>

            is slightly the same as:

                self.my_spbx = Spinbox(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_text (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <text name="my_text" bg="red"/>

            is slightly the same as:

                self.my_text = Text(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_tkevent (self, xml_tag, xml_element, tk_parent):
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

            _widget = _attributes.get("widget", tk_parent)

            # special case

            if _attributes.get("bind") == "bind_class":

                _bind = "{bind}('{class}', '{seq}', {slot}, '{add}')"

            else:

                _bind = "{bind}('{seq}', {slot}, '{add}')"

            # end if

            # try to bind event sequence

            exec("_widget." + _bind.format(**_attributes))

            # succeeded

            return True

        # end if

        # failed

        return False

    # end def



    def build_element_tkmenu (self, xml_tag, xml_element, tk_parent):
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

            self.register_object_by_id(_widget, _attributes.get("id"))

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



    def build_element_tkwidget (self, xml_tag, xml_element, tk_parent):
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

            return self.loop_on_children(

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



    def build_element_toplevel (self, xml_tag, xml_element, tk_parent):
        r"""
            XML element definition is almost the same as

            tkinter's native widget of the same (lowercased)

            class name;

            example:

                <toplevel name="my_toplevel" bg="red"/>

            is slightly the same as:

                self.my_toplevel = Toplevel(self, bg="red")

            with 'self' the parent widget;

            returns True on build success, False otherwise;
        """

        return self._build_tk_native(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_widget (self, xml_tag, xml_element, tk_parent,
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

            self.register_object_by_id(_widget, _attributes.get("id"))

            # keep a copy for specific post-implementations

            self.WIDGET = _widget

            # set widget as parent class member

            exec("tk_parent.{name} = _widget".format(**_attributes))

            # configure widget

            if hasattr(_widget, "configure") and self.TK_CONFIG:

                _widget.configure(**self.TK_CONFIG)

            # end if

            # set layout

            self._set_layout(_widget, _attributes, tk_parent)

            # free useless memory right now /!\

            del _attributes, _class, _args, self.TK_CONFIG

            # loop on XML element children - build tk child widgets

            return self.loop_on_children(

                xml_element, _widget, accept=self.DTD.get(xml_tag),
            )

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



    # -----------------------  XML attributes parsing  -----------------



    def parse_attr__after (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def parse_attr__before (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def parse_attr__height (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr__minsize (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr__padx (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr__pady (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr__sticky (self, attribute, **kw):
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



    def parse_attr__width (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(tk_child_config = True)

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_activerelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_activestyle (self, attribute, **kw):
        r"""
            must be one of 'underline', 'dotbox', 'none';

            default value is 'underline';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "underline",

            values = ("dotbox", "none"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def parse_attr_add (self, attribute, **kw):
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



    def parse_attr_after (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self.parse_attr__after(attribute, **kw)

    # end def



    def parse_attr_anchor (self, attribute, **kw):
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

                _anchor = re.sub(_search, _replace, _anchor)

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



    def parse_attr_args (self, attribute, **kw):
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



    def parse_attr_as (self, attribute, **kw):
        r"""
            conforms XML attr 'as' to language specs __identifier__;

            accepts only regexp("\w+") in fact;

            no return value (void);
        """

        # parsed attribute inits

        attribute.value = tools.canonize_id(attribute.value)

        # caution: *NO* self._tk_config() by here /!\

    # end def



    def parse_attr_aspect (self, attribute, **kw):
        r"""
            attr 'aspect' ratio (integer);

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_autoseparators (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_before (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self.parse_attr__before(attribute, **kw)

    # end def



    def parse_attr_bind (self, attribute, **kw):
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



    def parse_attr_buttonbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_buttoncursor (self, attribute, **kw):
        r"""
            cursor attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cursor_support(attribute, **kw)

    # end def



    def parse_attr_buttondownrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_buttonup (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_choices (self, attribute, **kw):
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



    def parse_attr_class (self, attribute, **kw):
        r"""
            forces XML attr 'class' name to conform to __identifier__

            language semantics def i.e. accept only regexp("\w+");

            no return value (void);
        """

        # param controls - forces value clean-ups

        if self._is_unparsed(attribute):

            # param inits

            _class = tools.choose_str(

                tools.canonize_id(attribute.value),

                self.WIDGET_CLASS,

                "Frame",
            )

            # parsed attribute inits

            attribute.value = _class

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_class_ (self, attribute, **kw):
        r"""
            fake classname for tkinter options database;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def parse_attr_closeenough (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def parse_attr_confine (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_default (self, attribute, **kw):
        r"""
            state attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_state_support(attribute, **kw)

    # end def



    def parse_attr_digits (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_direction (self, attribute, **kw):
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



    def parse_attr_disabledbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_elementborderwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_exportselection (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_format (self, attribute, **kw):
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



    def parse_attr_from (self, attribute, **kw):
        r"""
            from relative.module import ...;

            parse relative.module string value;

            no return value (void);
        """

        # param controls - forces value clean-ups

        if self._is_unparsed(attribute):

            # parsed attribute inits

            attribute.value = \
                tools.canonize_relative_module(attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_from_ (self, attribute, **kw):
        r"""
            starting point float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def parse_attr_handlepad (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_handlesize (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_height (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_highlightbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_highlightcolor (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_highlightthickness (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_import (self, attribute, **kw):
        r"""
            from ... import module;

            parses module string value;

            no return value (void);
        """

        # param controls - forces value clean-ups

        if self._is_unparsed(attribute):

            # parsed attribute inits

            attribute.value = tools.canonize_import(attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_increment (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def parse_attr_indicatoron (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_insertbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_insertborderwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_insertofftime (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_insertontime (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_insertwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_jump (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_justify (self, attribute, **kw):
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



    def parse_attr_label (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def parse_attr_labelanchor (self, attribute, **kw):
        r"""
            anchor attribute;

            no return value (void);
        """

        self.parse_attr_anchor(attribute, **kw)

    # end def



    def parse_attr_labelwidget (self, attribute, **kw):
        r"""
            widget attribute;

            no return value (void);
        """

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def parse_attr_layout (self, attribute, **kw):
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



    def parse_attr_layout_options (self, attribute, **kw):
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



    def parse_attr_length (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_listvariable (self, attribute, **kw):
        r"""
            control variable attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cvar_support(attribute, **kw)

    # end def



    def parse_attr_maxundo (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_minsize (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self.parse_attr__minsize(attribute, **kw)

    # end def



    def parse_attr_module (self, attribute, **kw):
        r"""
            tries to determine module's correct alias name;

            no return value (void);
        """

        # $ 2014-01-09 RS $
        # bug fix:
        # @attribute may be None sometimes;

        # Tk natives: if module id is 'TK.' -> no need to go further;

        if self._is_new(attribute) and attribute.value != "TK.":

            # module name inits

            _name = ""

            # try to get <module> element for more info

            _module = self.get_element_by_id(attribute.value)

            # found corresponding <module> element?

            if self.is_element(_module):

                # attribute inits

                _import = tools.canonize_import(_module.get("import"))

                # choose between attrs

                if _import != "*":

                    _name = tools.choose_str(

                        tools.canonize_id(_module.get("as")),

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

            # parsed attribute inits

            attribute.value = _name.lstrip(".")

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_offrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_opaqueresize (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_orient (self, attribute, **kw):
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

    # end def



    def parse_attr_overrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_padx (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_pady (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_readonlybackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_repeatdelay (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_repeatinterval (self, attribute, **kw):
        r"""
            integer attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_resizable (self, attribute, **kw):
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



    def parse_attr_resolution (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def parse_attr_sashpad (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_sashrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_sashwidth (self, attribute, **kw):
        r"""
            dimension attribute

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_scrollregion (self, attribute, **kw):
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



    def parse_attr_selectbackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_selectborderwidth (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_selectforeground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_selectmode (self, attribute, **kw):
        r"""
            must be one of 'browse', 'single', 'multiple', 'extended';

            default value is 'browse';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "browse",

            values = ("single", "multiple", "extended"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def parse_attr_seq (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._ensure_string_value(attribute, **kw)

    # end def



    def parse_attr_show (self, attribute, **kw):
        r"""
            password echo character to show in entry box;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def parse_attr_showhandle (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_showvalue (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_signal (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._ensure_string_value(attribute, **kw)

    # end def



    def parse_attr_sliderlength (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_sliderrelief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def parse_attr_slot (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def parse_attr_spacing1 (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_spacing2 (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_spacing3 (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_src (self, attribute, **kw):
        r"""
            canonizes URI in XML attr 'src';

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = uri.canonize(attribute.value)

            # caution: *NO* self._tk_config() by here /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_start (self, attribute, **kw):
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



    def parse_attr_state (self, attribute, **kw):
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

        if kw.get("xml_tag") in ("entry", "spinbox"):

            _values = ("disabled", "readonly", )

        else:

            _values = ("disabled", )

        # end if

        # parsed attribute inits

        kw.update(default = "normal", values = _values)

        self._fix_values(attribute, **kw)

    # end def



    def parse_attr_sticky (self, attribute, **kw):
        r"""
            PanedWindow child configuration attr;

            no return value (void);
        """

        # parsed attribute inits

        self.parse_attr__sticky(attribute, **kw)

    # end def



    def parse_attr_tabs (self, attribute, **kw):
        r"""
            choices attribute;

            no return value (void);
        """

        # parsed attribute inits

        self.parse_attr_choices(attribute, **kw)

        self._tk_config(attribute, **kw)

    # end def



    def parse_attr_takefocus (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_text (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def parse_attr_textvariable (self, attribute, **kw):
        r"""
            control variable attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cvar_support(attribute, **kw)

    # end def



    def parse_attr_tickinterval (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def parse_attr_to (self, attribute, **kw):
        r"""
            float attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_float_support(attribute, **kw)

    # end def



    def parse_attr_troughcolor (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def parse_attr_undo (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_validate (self, attribute, **kw):
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



    def parse_attr_validatecommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def parse_attr_values (self, attribute, **kw):
        r"""
            choices attribute;

            no return value (void);
        """

        # parsed attribute inits

        self.parse_attr_choices(attribute, **kw)

        self._tk_config(attribute, **kw)

    # end def



    def parse_attr_width (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def parse_attr_wrap (self, attribute, **kw):
        r"""
            boolean attribute;

            must be 'char', 'word' or 'none' if XML element is 'text';

            no return value (void);
        """

        # parsed attribute inits

        if kw.get("xml_tag") == "text":

            kw.update(

                default = "none",

                values = ("char", "word"),
            )

            self._fix_values(attribute, **kw)

        else:

            self._tkRAD_boolean_support(attribute, **kw)

        # end if

    # end def



    def parse_attr_wraplength (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_xml_dir (self, attribute, **kw):
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



    def parse_attr_xml_file_ext (self, attribute, **kw):
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



    def parse_attr_xml_filename (self, attribute, **kw):
        r"""
            must be at least an empty string of chars;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._ensure_string_value(attribute, **kw)

    # end def



    def parse_attr_xscrollcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def parse_attr_xscrollincrement (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_yscrollcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def parse_attr_yscrollincrement (self, attribute, **kw):
        r"""
            dimension attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def


# end class RADXMLWidget
