#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    tkRAD - Tkinter Rapid Application Development library

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



# ====================   /!\ STANDALONE MODULE /!\   ===================



# lib imports

import re

import traceback

import xml.etree.ElementTree as ET

import Tkinter as TK

import tkMessageBox as MB



# simple widget building function

def build (xml, master = None):
    r"""
        easy widget building function;

        @xml param can be either an XML string of chars or a file URI;

        if @master param is None, built-in widgets will pop up

        into a Tk() toplevel window for demo testing;

        returns a tkinter.Frame widget containing XML built-in

        tkinter widgets;

        examples:

            # testing XML widgets from char string

            from tkRAD.easy import builder

            xml = \"""

                <root>

                    <label text="hello good people!"/>

                    <button text="OK" command="self.quit"/>

                </root>

            \"""

            builder.build(xml)

            # testing from file URI

            from tkRAD.easy import builder

            builder.build("./test.xml")

            # testing with a parent widget

            import tkinter as TK

            from tkRAD.easy import builder

            root = TK.Tk()

            my_window = TK.Frame(root)

            my_widget = builder.build("./test.xml", my_window)

            my_window.pack()

            root.mainloop()
    """

    return Builder(master).build(xml)

# end def



class Builder (TK.Frame):
    r"""
        /!\ tkRAD.easy.builder is a STANDALONE module /!\

        you can pick it up and use it *as is* in your own project;

        lightweight XML to tkinter widget building class;

        this class implements the very minimal needs for very simple

        tkinter widget generation sourced from an XML file or

        from an XML string of chars;

        for better XML widget building in large applications,

        please use tkRAD.xml.RADXMLWidget() object instead;

        examples:

            # testing XML widgets from char string

            from tkRAD.easy import builder as B

            xml = \"""

                <root>

                    <label text="hello good people!"/>

                    <button text="OK" command="self.quit"/>

                </root>

            \"""

            B.Builder().build(xml)

            # testing from file URI

            from tkRAD.easy import builder as B

            B.Builder().build("./test.xml")

            # testing with a parent widget

            import tkinter as TK

            from tkRAD.easy import builder as B

            root = TK.Tk()

            my_window = TK.Frame(root)

            my_widget = B.Builder(my_window).build("./test.xml")

            my_window.pack()

            root.mainloop()

        see also build() module function def

        for much easier use of widget building than this;
    """



    # attributes parser method pattern def

    ATTRIBUTE_PARSER = "_parse_attr_{attr}"



    # object instance (oi) counter def

    OI_COUNT = 1



    PACK_OPTIONS = {

        "side": TK.TOP,

        "expand": 1,

        "fill": TK.BOTH,

        "padx": 0,

        "pady": 0,

    } # end of PACK_OPTIONS



    TK_CLASSES = {

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

    } # end of TK_CLASSES



    def __init__ (self, master = None, **kw):
        r"""
            class contructor;

            resets master = Tk() if master is None

            and prepares for testing session auto running;

            no return value (void);
        """

        # member inits

        self.__autorun = False

        # set autorun session if needed

        if not master:

            # reset master for testing session

            master = TK.Tk()

            # set flag on

            self.__autorun = True

        # end if

        # super class inits

        TK.Frame.__init__(self, master, **kw)

        # member inits

        self.master = master

        self.xml_tree = None

        self.objects = dict()

    # end def



    # --------------------- protected method defs ----------------------



    def _build_element (self, xml_element, tk_parent):
        r"""
            builds an XML element along its class name

            and a parent tkinter widget;

            recurse on XML element's children to build them too;

            no return value (void);
        """

        # get xml element's tag name

        _tag = xml_element.tag

        _tagl = _tag.lower()

        # XML root node?

        if _tagl in ("root", "tkwidget"):

            # widget already exists!

            _widget = tk_parent

        # create tkinter widget

        else:

            # parse some minimal XML attributes

            self._parse_xml_attributes(xml_element, tk_parent)

            # XML attribute 'id' is *NOT* a tk config option /!\

            _id = xml_element.attrib.pop("id", None)

            # search for correct class name

            _classname = self.TK_CLASSES.get(_tagl, _tag)

            # create widget

            r"""
                $ 2014-01-25 RS $
                caution: people may use ttk or PWM
                do *NOT* prefix {_class} with 'TK.' /!\
            """

            _widget = eval(

                "{_class}(tk_parent, **xml_element.attrib)"

                .format(_class = _classname)
            )

            # register newly created object by its XML id

            self._register_object_by_id(_widget, _id)

            # layout inits

            _widget.pack(**self.PACK_OPTIONS)

        # end if

        # search for widget's children

        for _child in xml_element:

            # create new child widget

            self._build_element(_child, _widget)

        # end for

    # end def



    def _get_correct_id (self, attr_id):
        r"""
            canonizes XML attribute @attr_id param;

            resets to numbered unique 'objectxxxx' if incorrect id;

            always return a normalized id;
        """

        # param inits

        attr_id = self.canonize_id(attr_id)

        # incorrect id name?

        if not self.is_pstr(attr_id):

            # reset id name

            attr_id = self._get_unique_id("object")

        # end if

        # return normalized id

        return attr_id

    # end def



    def _get_unique_id (self, radix):
        r"""
            tries to find a new and unique indexed 'id' name along
            @radix param name;

            returns new unique 'id' name on success, None otherwise;
        """

        # param controls

        if self.is_pstr(radix):

            # this prevents from counting overflow /!\

            while self.OI_COUNT:

                # set new indexed 'id' name

                _uid = radix + str(self.OI_COUNT)

                self.OI_COUNT += 1

                # got unique 'id' name?

                if _uid not in self.objects:

                    return _uid

                # end if

            # end while

        # end if

        return None

    # end def



    def _init_xml_tree (self, arg):
        r"""
            determines if @arg param is a valid file URI,

            tries to parse XML source string of chars otherwise;

            raises TypeError if @arg is not at least a string of chars;

            no return value (void);
        """

        # internal XML tree init

        self.xml_tree = None

        # reset object instance (oi) counter

        self.OI_COUNT = 1

        # param controls - arg must be XML string or file URI

        if self.is_pstr(arg):

            # argument is a file URI?

            if "<" not in arg:

                # internal XML tree init

                self.xml_tree = ET.parse(arg)

            # try to parse XML string of chars

            else:

                # internal XML tree init

                self.xml_tree = ET.ElementTree(

                        element = ET.fromstring(arg)
                )

            # end if

        # unsupported type

        else:

            raise TypeError(

                "XML argument must be a string of chars."
            )

        # end if

    # end def



    def _parse_attr_command (self, value, attrs, **kw):
        r"""
            parses XML attribute 'command';

            makes its string value become a real method def link;

            no return value (void);
        """

        # XML parsed attribute inits

        attrs["command"] = eval(value)

    # end def



    def _parse_attr_id (self, value, attrs, **kw):
        r"""
            parses XML attribute 'id';

            normalizes it to match __identifier__ standard language def;

            no return value (void);
        """

        # XML parsed attribute inits

        attrs["id"] = self._get_correct_id(value)

    # end def



    def _parse_xml_attributes (self, xml_element, tk_parent):
        r"""
            parses at least some very essential XML attributes

            such as 'command' which needs to link to real method defs;

            no return value (void);
        """

        # init keywords

        _kw = {

            "xml_element": xml_element,

            "tk_parent": tk_parent,
        }

        # attributes init

        _attrs = xml_element.attrib

        # loop on attributes

        for (_attr, _value) in _attrs.items():

            # parser init

            _parser = (

                str(self.ATTRIBUTE_PARSER).format(attr = _attr.lower())
            )

            # attribute parsing is OPTIONAL /!\

            _parser = getattr(self, _parser, None)

            # callable parser?

            if callable(_parser):

                # call parser with good params

                _parser(_value, _attrs, **_kw)

            # end if

        # end for

    # end def



    def _register_object_by_id (self, built_object, attr_id):
        r"""
            counterpart of get_object_by_id() method def;

            registers newly created objects along their XML id name;

            no return value (void);
        """

        self.objects[self._get_correct_id(attr_id)] = built_object

    # end def



    # --------------------- public method defs ----------------------



    def build (self, arg):
        r"""
            tries to build tkinter widgets from a char string or

            from a file URI;

            will pop-up a message box with a traceback message

            if any exception raises;

            returns 'self' as a widget container of all built-in

            tkinter widgets for further use in your own program;
        """

        try:

            # param controls - arg must be XML string or file URI

            self._init_xml_tree(arg)

            # build XML element as tkinter widget

            self._build_element(self.xml_tree.getroot(), self)

            # layout inits

            self.pack(**self.PACK_OPTIONS)

            # need an autorun testing session?

            if self.__autorun:

                # run testing session

                self.winfo_toplevel()\
                    .protocol("WM_DELETE_WINDOW", self.quit)

                self.mainloop()

                self.winfo_toplevel().withdraw()

            # end if

            # return 'this' pointer

            # containing all built-in widgets

            return self

        except:

            MB.showerror(

                "Caught exception",

                "An exception has raised:\n\n{msg}"

                .format(msg = traceback.format_exc(limit = 1)),
            )

            raise

        # end try

        # failed

        return None

    # end def



    def canonize_id (self, attr_id):
        r"""
            sets @attr_id param in conformance with __identifier__

            language def (allows only regexp("\w+") in id naming);

            returns canonized id name or empty string otherwise;
        """

        # param controls

        if self.is_pstr(attr_id):

            return re.sub(r"\W+", r"", attr_id)

        # end if

        # unsupported

        return ""

    # end def



    def get_object_by_id (self, attr_id):
        r"""
            tries to retrieve the object created through its definition

            into an XML element declared with id='@attr_id' param

            while dynamically generated;

            returns the concerned object if 'id' matches @attr_id param,

            returns None otherwise;
        """

        return self.objects.get(self.canonize_id(attr_id))

    # end def



    def hide_widgets (self):
        r"""
            unpacks all children widgets in order to pack(), grid() or

            place() them in a specific user-defined way;

            no return value (void);
        """

        # loop on child widgets

        for _widget in self.winfo_children():

            _widget.pack_forget()

            _widget.grid_forget()

            _widget.place_forget()

        # end for

    # end def



    def is_pstr (self, arg):
        r"""
            determines if @arg param is of plain string type or not;
        """

        return arg and isinstance(arg, str)

    # end def



    def set_pack_options (self, **kw):
        r"""
            sets specific w.pack() options for widget building;

            no return value (void);
        """

        self.PACK_OPTIONS = kw

    # end def


# end class Builder



# testing this STANDALONE module

if __name__ == "__main__":

    # XML string of chars init

    xml = """
        <root>
            <label text="hello good people!"/>
            <button text="OK" command="self.quit"/>
        </root>
    """

    # build widgets in automagic toplevel window

    build(xml)

    build("builder-example.xml")

    # uncomment the followings to try them

    """
    Builder().build(xml)

    Builder().build("builder-example.xml")

    root = TK.Tk()

    my_window = TK.Frame(root)

    my_widget = Builder(my_window).build("builder-example.xml")

    my_window.pack()

    root.mainloop()
    """

# end if
