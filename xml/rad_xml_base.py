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

import os.path as OP

import traceback

import xml.etree.ElementTree as ET

import tkinter as TK

from tkinter import messagebox as MB

from . import rad_xml_attribute as XA

from . import rad_xml_attributes_dict as XD

from ..core import uri

from ..core import tools

from ..widgets import rad_widget_base as RW



class RADXMLBase (RW.RADWidgetBase):
    r"""
        base class for generic XML building processor;

        supports XML file management;

        supports generic XML element building;

        supports generic XML attribute parsing;

        supports tkinter control variables management;

        supports created objects direct access along XML attribute id

        i.e. self.get_object_by_id('obj_id');

        and some other generic functions;
    """



    # XML attribute parser method pattern

    ATTRIBUTE_PARSER = "parse_{xml_element}_attr_{xml_attr}"



    # XML element builder method pattern

    ELEMENT_BUILDER = "build_element_{xml_element}"



    # param defs

    KEYWORD = {

        "dir": "xml_dir",

        "filename": "xml_filename",

        "file_ext": "xml_file_ext",

    } # end of KEYWORD



    RC_OPTIONS = {

        "dir": "default_xml_dir",

        "filename": "default_xml_filename",

        "file_ext": "default_xml_file_ext",

    } # end of RC_OPTIONS



    # should be overridden in subclass

    XML_RC = {

        "dir": "^/xml",

        #~ /!\ "filename" will be redef'd in __init__() /!\

        "file_ext": ".xml",

    } # end of XML_RC



    # Object instance counter

    __OI_COUNT = 1



    def __init__ (self, tk_owner = None, **kw):
        r"""
            class constructor;
        """

        # XML member inits

        self.__xml_tree = None

        self.__objects = dict()

        self.set_xml_dir(kw.get(self.KEYWORD["dir"]))

        self.set_xml_filename(kw.get(self.KEYWORD["filename"]))

        self.set_xml_file_ext(kw.get(self.KEYWORD["file_ext"]))

        # XML_RC redefs

        _classname = self.__class__.__name__.lower()

        self.XML_RC["filename"] = _classname

        self.RC_OPTIONS.setdefault("section", _classname)

        # tkinter member inits

        self.__tk_variables = {

            "doublevar": dict(),

            "intvar": dict(),

            "stringvar": dict(),

        }

        # super inits

        RW.RADWidgetBase.__init__(self, tk_owner, **kw)

    # end def



    def _before_building_element(self, **kw):
        r"""
            virtual method to be overridden in subclass;

            allows some inits before building XML elements;
        """

        # make some inits - should be overridden in subclass

        pass

    # end def



    def _before_parsing_attribute(self, **kw):
        r"""
            virtual method to be overridden in subclass;

            allows some inits before parsing XML attributes;
        """

        # make some inits - should be overridden in subclass

        pass

    # end def



    def _build_element (self, xml_element, tk_parent):
        r"""
            delegates the widget building of an XML element to

            a specific element builder, as each XML element has

            its own behaviour and constraints;

            this method should not be modified for element build

            methods naming as it suffices to reset self.ELEMENT_BUILDER

            in subclass to the desired naming rule;

            raises TypeError if @xml_element has no supported

            building method in any case;

            returns True on element building success, False otherwise;
        """

        # param controls

        if not self.cast_element(xml_element):

            return False

        # end if

        # inits

        _tag = self.canonize_tag(xml_element)

        _elt_builder = tools.canonize_id(

            str(self.ELEMENT_BUILDER).format(xml_element = _tag)
        )

        # supported XML tag?

        if hasattr(self, _elt_builder):

            # real member inits

            _elt_builder = getattr(self, _elt_builder)

            # try to call builder

            if callable(_elt_builder):

                # element building inits

                self._before_building_element(

                    xml_tag = _tag,

                    xml_element = xml_element,

                    tk_parent = tk_parent,
                )

                # route element building

                return _elt_builder(_tag, xml_element, tk_parent)

            # end if

        # unsupported tag

        else:

            raise TypeError(

                _("Unsupported XML tag <{xml_tag}>.")

                .format(xml_tag = _tag)
            )

        # end if

        # failure

        return False

    # end def



    def _get_object_id (self, built_object, attr_id = None):
        r"""
            protected method def;
        """

        # param inits

        attr_id = tools.canonize_id(attr_id)

        # no id?

        if not tools.is_pstr(attr_id):

            # set default id along object's classname

            attr_id = str(

                "{classname}{index}"

                .format(

                    classname = built_object.__class__.__name__,

                    index = self._get_oi_count_str(),
                )
            )

        # end if

        # get built object id

        return attr_id.lower()

    # end def



    def _get_oi_count_str (self):
        r"""
            gets object instance (oi) counter as a string of chars;

            increments counter AFTER giving back its current value;

            returns object instance count as a char string;
        """

        # inits

        _str = str(self.__OI_COUNT)

        # update object instance counter

        self.__OI_COUNT += 1

        # return string of __OI_COUNT

        return _str

    # end def



    def _reset_oi_count (self, value = 1):
        r"""
            resets object instance (oi) counter to a given value;

            default value (if not given) is one (1);

            no return value (void);
        """

        # inits

        self.__OI_COUNT = max(1, tools.ensure_int(value))

    # end def



    def canonize_tag (self, xml_element):
        r"""
            returns a lowercased char string of @xml_element.tag;
        """

        return str(xml_element.tag).lower()

    # end def



    def cast_element (self, xml_element):
        r"""
            casts @xml_element param to see if it is a real

            xml.etree.ElementTree.Element object;

            raises TypeError on failure;

            returns True on success, False otherwise;
        """

        if self.is_element(xml_element):

            return True

        else:

            raise TypeError(

                _(
                    "XML element must be of type "

                    "'{obj_type}' not '{cur_type}'."

                ).format(

                    obj_type = repr(ET.Element),

                    cur_type = repr(xml_element)
                )
            )

            return False

        # end if

    # end def



    def cast_tree (self, tree_object):
        r"""
            casts @tree_object param to see if it is a real

            xml.etree.ElementTree object;

            raises TypeError on failure;

            returns True on success, False otherwise;
        """

        if self.is_tree(tree_object):

            return True

        else:

            raise TypeError(

                _(
                    "XML tree must be of type "

                    "'{obj_type}' not '{cur_type}'."

                ).format(

                    obj_type = repr(ET.ElementTree),

                    cur_type = repr(tree_object)
                )
            )

            return False

        # end if

    # end def



    def delete_dict_items (self, dict_object, *args):
        r"""
            strips all keys listed in args from a dict() object;

            shallow copy: keeps original dict() object UNTOUCHED /!\

            returns new modified dict() object;
        """

        # inits

        _dict = dict_object.copy()

        # loop on args

        for _key in args:

            _dict.pop(_key, None)

        # end for

        return _dict

    # end def



    def get_correct_id(self, value):
        r"""
            always provide a correct id name

            whatever @value param is at the beginning;

            returns canonized (filtered) value if exists,

            returns numbered unique 'objectxxx' otherwise;
        """

        # param inits

        value = tools.canonize_id(value)

        # no id?

        if not tools.is_pstr(value):

            # new value inits

            value = "object" + self._get_oi_count_str()

        # end if

        # return filtered value

        return value

    # end def



    def get_cvar (self, vartype, varname):
        r"""
            tries to retrieve a tkinter control variable @varname;

            @vartype param must be one of 'StringVar', 'IntVar' or

            'DoubleVar' (param is case-insensitive);

            raises TypeError otherwise;

            returns control variable on success, None otherwise;
        """

        # param inits

        vartype = str(vartype).lower()

        if vartype in self.__tk_variables:

            return self.__tk_variables[vartype].get(varname, None)

        else:

            raise TypeError(

                _(
                    "Tkinter control variable must be one of type "

                    "'DoubleVar', 'IntVar' or 'StringVar' "

                    "(case insensitive)."
                )
            )

            return None

        # end if

    # end def



    def get_cvars (self):
        r"""
            returns dict() object of all created control vars;

            may affect internal dict() object;
        """

        return self.__tk_variables

    # end def



    def get_doublevar (self, varname):
        r"""
            tries to retrieve a tkinter.DoubleVar() named @varname;

            returns control variable on success, None otherwise;
        """

        return self.__tk_variables["doublevar"].get(varname, None)

    # end def



    def get_doublevars (self):
        r"""
            returns dict() object of all created DoubleVars;

            may affect internal dict() object;
        """

        return self.__tk_variables["doublevar"]

    # end def



    def get_element_by_id (self, attr_id, xml_tree = None):
        r"""
            returns an xml.etree.ElementTree.Element from

            an xml.etree.ElementTree @xml_tree param along an

            XML id attribute @attr_id param or None in case of failure;

            if @xml_tree param is not given, uses the internal

            XML tree data structure instead;
        """

        # param inits

        attr_id = tools.canonize_id(attr_id)

        # param controls

        if tools.is_pstr(attr_id):

            # param controls

            if not self.is_tree(xml_tree):

                xml_tree = self.__xml_tree

            # end if

            return xml_tree.find(

                ".//*[@id='{value}']".format(value = attr_id)
            )

        # end if

        # failure

        return None

    # end def



    def get_intvar (self, varname):
        r"""
            tries to retrieve a tkinter.IntVar() named @varname;

            returns control variable on success, None otherwise;
        """

        return self.__tk_variables["intvar"].get(varname, None)

    # end def



    def get_intvars (self):
        r"""
            returns dict() object of all created IntVars;

            may affect internal dict() object;
        """

        return self.__tk_variables["intvar"]

    # end def



    def get_object_by_id (self, attr_id, default = None):
        r"""
            this is the counterpart of register_object_by_id() method;

            returns object tagged by @attr_id param on success;

            returns @default object on failure;
        """

        return self.__objects.get(

            tools.canonize_id(attr_id).lower(),

            default
        )

    # end def



    def get_objects (self):
        r"""
            returns all the (id: object) pairs in a dict() object;

            does not affect internal dict of objects as it returns

            only a shallow copy of the original objects dict;
        """

        return self.__objects.copy()

    # end def



    def get_stringvar (self, varname):
        r"""
            tries to retrieve a tkinter.StringVar() named @varname;

            returns control variable on success, None otherwise;
        """

        return self.__tk_variables["stringvar"].get(varname, None)

    # end def



    def get_stringvars (self):
        r"""
            returns dict() object of all created StringVars;

            may affect internal dict() object;
        """

        return self.__tk_variables["stringvar"]

    # end def



    def get_xml_dir (self):
        r"""
            returns internal XML directory def;
        """

        return self.__xml_dir

    # end def



    def get_xml_file_ext (self):
        r"""
            returns internal XML file extension def;
        """

        return self.__xml_file_ext

    # end def



    def get_xml_filename (self):
        r"""
            returns internal XML filename radix def;
        """

        return self.__xml_filename

    # end def



    def get_xml_tree (self):
        r"""
            returns current internal XML tree data structure;
        """

        return self.__xml_tree

    # end def



    def get_xml_uri (self, filename = None):
        r"""
            tries to retrieve a valid URI from several cases;

            @filename param can either be a filename radix to be

            automagically rebuilt or a complete file path (URI);

            raises OSError if unable to build a correct URI;

            returns final URI on success, None otherwise;
        """

        # param controls

        if tools.is_pstr(filename):

            # @filename param may be a URI

            _uri = uri.canonize(filename)

            if OP.isfile(_uri):

                return _uri

            # end if

        # end if

        # param inits

        filename = tools.choose_str(

            filename,

            self.get_xml_filename(),

            self.options[self.RC_OPTIONS["section"]]
                .get(self.RC_OPTIONS["filename"]),

            self.XML_RC.get("filename"),
        )

        # strip eventual file exts

        filename = re.sub(r"\..*$", r"", filename.lstrip("."))

        # failed to retrieve a valid XML filename

        if not filename:

            raise OSError(

                _("Unable to determine a valid XML filename.")
            )

            return None

        # end if

        # retrieve file ext

        _ext = tools.choose_str(

            self.get_xml_file_ext(),

            self.options[self.RC_OPTIONS["section"]]
                .get(self.RC_OPTIONS["file_ext"]),

            self.XML_RC.get("file_ext"),
        )

        # got a file ext?

        if _ext:

            # filename completion

            filename += "." + _ext.lstrip(".")

        # end if

        # retrieve XML directory

        _dir = tools.choose_str(

            self.get_xml_dir(),

            self.options[self.RC_OPTIONS["section"]]
                .get(self.RC_OPTIONS["dir"]),

            self.XML_RC.get("dir"),
        )

        # failed to retrieve a valid XML directory

        if not _dir:

            raise OSError(

                _("Unable to determine a valid XML directory.")
            )

            return None

        # end if

        # return rebuilt XML URI

        return OP.join(uri.canonize(_dir), filename)

    # end def



    def is_element (self, xml_element):
        r"""
            determines if @xml_element param is a real

            xml.etree.ElementTree.Element object;

            returns True on success, False otherwise;
        """

        return isinstance(xml_element, ET.Element)

    # end def



    def is_tree (self, tree_object):
        r"""
            determines if @tree_object param is a real

            xml.etree.ElementTree object;

            returns True on success, False otherwise;
        """

        return isinstance(tree_object, ET.ElementTree)

    # end def



    def loop_on_children (self, xml_element, tk_parent, accept = None):
        r"""
            loops on @xml_element param XML subelements with

            @tk_parent param as tkinter parent widget;

            @accept param sets up a list of admitted XML tags

            as subelements of @xml_element param;

            tries to build all accepted subelements;

            raises TypeError on unwanted subelements;

            returns True on overall success, False otherwise;
        """

        # param controls

        if self.cast_element(xml_element):

            # parent tag inits

            _ptag = self.canonize_tag(xml_element)

            # return value inits

            _ret = True

            # loop on child XML elements

            for _xml_child in xml_element:

                # child tag inits

                _ctag = self.canonize_tag(_xml_child)

                # is child element into 'accept' element list?

                if not accept or _ctag in accept:

                    # build child elements into tk_parent object

                    _ret = self._build_element(_xml_child, tk_parent) \
                                                                and _ret

                # unwanted child element

                else:

                    raise TypeError(

                        _(
                            "XML child element <{child_tag}> is *NOT* "

                            "accepted inside <{parent_tag}> element."

                        ).format(child_tag = _ctag, parent_tag = _ptag)
                    )

                    return False

                # end if

            # end for

            # return final success/failure

            return _ret

        # end if

        # failed (bad XML element)

        return False

    # end def



    def parse_xml_attributes (self, xml_element, tk_parent, **kw):
        r"""
            parses dict() attributes of an XML ET.Element

            and dispatches to optional specific parsers;

            this method should not be modified for parsing attribute

            methods naming as it suffices to reset self.ATTRIBUTE_PARSER

            in subclass to the desired naming rule;

            if kw["xml_attrs"] filtered attributes exist,

            they replace XML ET.Element.attrib dict() in parsing;

            genuine dicts are kept UNTOUCHED thanks to shallow copying;

            returns new dict() of parsed attributes or None on failure;
        """

        # param controls

        if self.cast_element(xml_element):

            # XML tag inits

            _tag = self.canonize_tag(xml_element)

            # XML attribute inits

            _attrs = kw.get("xml_attrs", xml_element.attrib)

            r"""
                $ 2013-12-16 RS $
                new support: work with RADXMLAttribute objects by now;

                $ 2013-12-18 RS $
                new support: work with RADXMLAttributesDict by now;

                notice:
                XA.reset_attributes() provides dict() shallow copy;
            """

            _attrs = XD.RADXMLAttributesDict(

                XA.reset_attributes(_attrs, xml_element)
            )

            # loop on RADXMLAttribute attributes list

            for (_attr_name, _attr_object) in _attrs.items():

                # canonize attribute

                _attr_name = str(_attr_name).lower()

                # attribute specific parser

                _parser = tools.canonize_id(

                    str(self.ATTRIBUTE_PARSER)

                    .format(xml_element = _tag, xml_attr = _attr_name)
                )

                # optional parser

                if hasattr(self, _parser):

                    # real member inits

                    _parser = getattr(self, _parser)

                    # try to call specific parser

                    if callable(_parser):

                        # update keywords

                        kw.update(

                            tk_parent = tk_parent,

                            xml_element = xml_element,

                            xml_tag = _tag,

                            xml_attr = _attr_name,
                        )

                        # attribute parsing inits

                        self._before_parsing_attribute(

                            attribute = _attr_object,

                            attrs = _attrs,

                            **kw
                        )

                        # call parser

                        _parser(_attr_object, _attrs, **kw)

                        r"""
                            $ 2013-12-16 RS $
                            new support: using RADXMLAttribute by now;
                        """

                        # update parsing counter

                        _attr_object.parsed = True

                    # end if

                # not implemented

                else:

                    print(

                        _(
                            "[WARNING] RADXMLBase::"

                            "parse_xml_attributes: optional parser "

                            "'{parser}()' is *NOT* implemented."

                        ).format(parser = _parser)
                    )

                # end if

            # end for

            r"""
                $ 2013-12-18 RS $
                new support: using RADXMLAttributesDict by now;

                notice:
                flatten() provides a 'flat' dict() object containing
                simple (key, value) pairs;
                all RADXMLAttribute extra data are lost at this point;
            """

            # return parsed attributes

            return _attrs.flatten()

        # end if

        # failure

        return None

    # end def



    def register_object_by_id (self, built_object, attr_id):
        r"""
            registers newly created or existing object with the

            XML attribute 'id' which defined it in XML data source;

            this is the counterpart of get_object_by_id() method;

            no return value (void);
        """

        _id = self._get_object_id(built_object, attr_id)

        if _id not in self.__objects:

            self.__objects[_id] = built_object

        else:

            raise KeyError(

                _(
                    "cannot override existing object of id '{obj_id}'"

                ).format(obj_id = _id)
            )

        # end if

    # end def



    def set_cvar (self, vartype, varname):
        r"""
            creates (if not already exists) a tkinter control variable

            'DoubleVar', 'IntVar' or 'StringVar' for a given @varname;

            returns the already existing or the newly created object

            for that given @varname param;

            raises TypeError and returns None if type mismatch;
        """

        # param inits

        vartype = str(vartype).lower()

        if vartype in self.__tk_variables:

            # efficient memory management - do not use .setdefault()

            if varname not in self.__tk_variables[vartype]:

                _cvar = {

                    "doublevar": TK.DoubleVar,

                    "intvar": TK.IntVar,

                    "stringvar": TK.StringVar,

                }.get(vartype)

                self.__tk_variables[vartype][varname] = _cvar()

            # end if

            # return already existing or newly created cvar

            return self.__tk_variables[vartype].get(varname, None)

        else:

            raise TypeError(

                _(
                    "Tkinter control variable must be one of type "

                    "'DoubleVar', 'IntVar' or 'StringVar' "

                    "(case insensitive)."
                )
            )

            return None

        # end if

    # end def



    def set_doublevar (self, varname):
        r"""
            tries to create a tkinter.DoubleVar() named @varname;

            if @varname already exists, keeps the original untouched;

            returns control variable on success, None otherwise;
        """

        return self.set_cvar("doublevar", varname)

    # end def



    def set_intvar (self, varname):
        r"""
            tries to create a tkinter.IntVar() named @varname;

            if @varname already exists, keeps the original untouched;

            returns control variable on success, None otherwise;
        """

        return self.set_cvar("intvar", varname)

    # end def



    def set_stringvar (self, varname):
        r"""
            tries to create a tkinter.StringVar() named @varname;

            if @varname already exists, keeps the original untouched;

            returns control variable on success, None otherwise;
        """

        return self.set_cvar("stringvar", varname)

    # end def



    def set_xml_dir (self, value):
        r"""
            sets internal XML directory def;
        """

        self.__xml_dir = value

    # end def



    def set_xml_file_ext (self, value):
        r"""
            sets internal XML file extension def;
        """

        self.__xml_file_ext = value

    # end def



    def set_xml_filename (self, value):
        r"""
            sets internal XML filename radix def;
        """

        self.__xml_filename = value

    # end def



    def set_xml_tree (self, **kw):
        r"""
            sets internal XML tree along @kw param keywords;

            keywords should be either 'element' or 'file' as in

            xml.etree.ElementTree() constructor proto;

            no return value (void);
        """

        # reset XML tree

        self.__xml_tree = ET.ElementTree(**kw)

    # end def



    def xml_build (self, filename = None, silent_mode = False):
        r"""
            public entry point of XML widget building;

            @filename param can either be a filename radix to be

            automagically rebuilt, a complete file path (URI) or

            an XML source string of chars;

            returns True on overall success, False, otherwise;
        """

        # try to build widgets

        try:

            # verify XML tree before processing

            if tools.is_pstr(filename) or \
                                        not self.is_tree(self.__xml_tree):

                # try to load once

                self.xml_load(filename)

            # end if

            # start XML widget building

            return self._build_element(

                self.__xml_tree.getroot(),

                self.tk_owner
            )

        except:

            if not silent_mode:

                MB.showerror(

                    _("Caught exception"),

                    _(
                        "An exception has occurred "

                        "during XML widget building:"

                        "\n\n{msg}\n"

                        "Please, check your XML code before "

                        "contacting tkRAD software maintainers for "

                        "bug fixes.\nThank you."

                    ).format(msg = traceback.format_exc(limit = 0))
                )

            # end if

            raise

            exit(1)

        # end try

    # end def



    def xml_load (self, arg = None):
        r"""
            loads and parses XML data;

            @arg param can either be a filename radix to be

            automagically rebuilt, a complete file path (URI) or

            an XML source string of chars;

            no return value (void);
        """

        try:

            # XML tag detected?

            if tools.is_pstr(arg) and re.search(r"<[^>]*>", arg) != None:

                # parse XML char string source

                self.set_xml_tree(element = ET.fromstring(arg))

            # should be a filename or URI

            else:

                # XML parse file URI

                self.__xml_tree = ET.parse(self.get_xml_uri(arg))

            # end if

        except ET.ParseError:

            raise RuntimeError(

                _("XML source code may contain some errors.")

            ) from None

            exit(1)

        # end try

        # reset object instance counter

        self._reset_oi_count()

    # end def



    def xml_save (self, filename = None):
        r"""
            writes internal XML tree data structure into a file;

            @filename param can either be a filename radix to be

            automagically rebuilt or a complete file path (URI);

            no return value (void);
        """

        # verify XML tree before processing

        if self.cast_tree(self.__xml_tree):

            self.__xml_tree.write(

                self.get_xml_uri(filename),

                encoding = "utf-8",

                xml_declaration = True,

                method = "xml"
            )

        # end if

    # end def


# end class RADXMLBase
