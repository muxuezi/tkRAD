<!-- encoding: UTF-8 -->


## CONTRIBUTORS

    RS    Raphaël SEBAN


## CHANGELOG


### $ 2014-01-13 RS $

* updated `RADXMLWidget`:

    * in `parse_attr_xscrollincrement()`:

        * now fully implemented;

    * in `parse_attr_yscrollincrement()`:

        * now fully implemented;

    * in `parse_attr_wraplength()`:

        * now fully implemented;

    * in `parse_attr_takefocus()`:

        * now fully implemented;

    * in `parse_attr_sliderlength()`:

        * now fully implemented;

    * in `parse_attr_troughcolor()`:

        * now fully implemented;

    * in `parse_attr_tickinterval()`:

        * now fully implemented;

    * in `parse_attr_resolution()`:

        * now fully implemented;

    * in `parse_attr_to()`:

        * now fully implemented;

    * in `parse_attr_from_()`:

        * now fully implemented;

    * in `parse_attr_showvalue()`:

        * now fully implemented;

    * in `parse_attr_readonlybackground()`:

        * now fully implemented;

    * in `parse_attr_pady()`:

        * now fully implemented;

    * in `parse_attr_padx()`:

        * now fully implemented;

    * in `parse_attr_orient()`:

        * now fully implemented;

    * in `parse_attr_offrelief()`:

        * now fully implemented;

    * in `parse_attr_length()`:

        * now fully implemented;

    * in `parse_attr_insertwidth()`:

        * now fully implemented;

    * in `parse_attr_insertborderwidth()`:

        * now fully implemented;

    * in `parse_attr_insertbackground()`:

        * now fully implemented;

    * in `parse_attr_indicatoron()`:

        * now fully implemented;

    * in `parse_attr_highlightthickness()`:

        * now fully implemented;

    * in `parse_attr_highlightcolor()`:

        * now fully implemented;

    * in `parse_attr_highlightbackground()`:

        * now fully implemented;

    * in `parse_attr_height()`:

        * now fully implemented;

    * in `parse_attr_exportselection()`:

        * now fully implemented;

    * in `parse_attr_elementborderwidth()`:

        * now fully implemented;

    * in `parse_attr_disabledbackground()`:

        * now fully implemented;

    * in `parse_attr_digits()`:

        * now fully implemented;

    * in `parse_attr_buttondownrelief()`:

        * now fully implemented;

    * in `parse_attr_buttonbackground()`:

        * now fully implemented;

    * in `parse_attr_module()`:

        * now module `id` *NOT* found raises `KeyError`;

    * in `parse_attr_sliderrelief()`:

        * now fully implemented along `parse_attr_relief()`;

    * in `parse_attr_sashrelief()`:

        * now fully implemented along `parse_attr_relief()`;

    * in `parse_attr_overrelief()`:

        * now fully implemented along `parse_attr_relief()`;

    * in `parse_attr_activerelief()`:

        * now fully implemented along `parse_attr_relief()`;

* updated `RADXMLWidgetBase`:

    * added new `_tkRAD_boolean_support()`:

        * now fully implemented;

    * in `parse_attr_relief()`:

        * now fully implemented;


### $ 2014-01-12 RS $

* updated `RADXMLBase`:

    * in `get_correct_id()`:

        * fixed bug on already existing names while creating default
        'objectXXX' id names;

    * in `_get_object_id()`:

        * fixed bug on already existing names while creating default
        '{classname}XXX' id names;

    * added new `_get_unique_id (self, radix)`:

        * tries to retrieve a new and unique indexed 'id' name along
        `@radix` param;

* updated `RADXMLMenu`:

    * added new `DTD`:

        * added `DTD.menu` constraints;

        * added `DTD.tkmenu` constraints;

    * in `build_element_tkmenu()`:

        * now supports direct inclusion into a `tkwidget` doctype
        XML tree document;

        * now supports all menu item childs `<command>`,
        `<checkbutton>`, `<radiobutton>` and `<separator>` when
        `menu handler` is *NOT* of type `tkinter.Tk` (topmenu
        handler);

* updated `RADXMLWidget`:

    * in `parse_attr_direction()`:

        * now fully implemented;

    * in `DTD`:

        * added support for `tkmenu` in `DTD.widget`;

    * added new `build_element_tkmenu()`:

        * now fully implemented;

    * kept old `build_element_menu()` for compatibility;


### $ 2014-01-11 RS $

* updated `RADXMLWidget`:

    * in `build_element_optionmenu()`:

        * now renamed XML attr `variable` to `listvariable` in order
        to match with `<listbox>` XML tk_config attr `listvariable`;

        * XML attr `variable` is *STILL KEPT AVAILABLE* for
        retro-compatibility reasons;

        * this will ease XML scripting/switching between `<listbox>`
        and `<optionmenu>` in testing session;

        * rebounded `start` XML attr so as it might never trap out
        of list bounds;

    * in `parse_attr_choices()`:

        * fixed bug on selecting numeric values;

    * in `parse_attr_listvariable()`:

        * now fully implemented along `parse_attr_variable()`;

    * in `build_element_listbox()`:

        * now fully implemented and debugged specific code;

    * in `ATTRS`:

        * renamed `optionmenu.variable` to `optionmenu.listvariable`
        for XML scripting comfort and easiness;

        * XML attr `<optiomenu variable=""/>` is *STILL KEPT
        AVAILABLE* for retro-compatibility reasons;

        * added `listbox` default XML attrs;


### $ 2014-01-10 RS $

* updated `RADXMLWidget`:

    * in `ATTRS`:

        * added `optionmenu` default XML attrs;

    * in `build_element_optionmenu()`:

        * now fully implemented and debugged specific code;

    * added new `parse_attr_choices()`:

        * now fully implemented and debugged;

    * added new `parse_attr_start()`:

        * now fully implemented and debugged;


### $ 2014-01-09 RS $

* updated `RADXMLWidgetBase`:

    * in `parse_attr_widget()`:

        * now raises `KeyError` if widget `id` is *NOT* found;

    * in `_is_new()`:

        * fixed bug: `@attribute` param may be `None` sometimes;

* added new file `TODO.md`;

* updated `RADXMLWidget`:

    * in `parse_attr_module()`:

        * fixed bug: `@attribute` param may be `None` sometimes;

    * in `build_element_optionmenu()`:

        * disabled faulty generic code;

        * must implement *SPECIFIC CODE* for this object /!\;


### $ 2014-01-08 RS $

* updated `RADXMLWidget`:

    * in `parse_attr_labelanchor()`:

        * now fully implemented along `parse_attr_anchor()`;

        * CAUTION: will *NOT* accept values such as 'wn', 'ws', 'en'
        and 'es' (dummy values?);

    * in `parse_attr_labelwidget()`:

        * now fully implemented along `parse_attr_widget()`;

    * in `parse_attr_slot()`:

        * tkRAD.command.support is now fully implemented;

        * allows EventName aliasing;

* now working on an `ASUS R500VD-SX173H` laptop, Intel QuadCore
i5-3210M @ 2.5 GHz, HDD 500GB, RAM 4GB, widescreen 17.3" 16:9,
turbo'ed by an awesome Ubuntu 13.10 Saucy Salamander distro;


### $ 2014-01-06 RS $

* updated `RADXMLWidget`:

    * in `build_element_include()`:

        * new XML tree is now fully included into current XML tree;

        * all internal cvars, objects, `id` references, etc, are now
        entirely respected;

        * no more extra widget building with extra hassle;

* updated `RADXMLBase`:

    * in `xml_load()`:

        * minor change - no border effect;


### $ 2014-01-04 RS $

* updated `RADXMLWidget`:

    * in `ATTRS`:

        * added `button`, `checkbutton`, `label`, `menubutton`,
        `radiobutton` dict() attrs;

    * in `build_element_widget()`:

        * now supports external keywords (**kw) for XML attr inits;

    * in `_build_tk_native()`:

        * now supports specific XML attrs for tk natives;

    * in `parse_attr_textvariable()`:

        * now fully implemented;

    * in `parse_attr_text()`:

        * now linked to `_tkRAD_label_support()`;

* updated `RADXMLMenu`:

    * in `parse_attr_label()`:

        * now linked to `_tkRAD_label_support()`;

* updated `RADXMLWidgetBase`:

    * added `_tkRAD_label_support (self, attribute, attrs, **kw)`;

* moved file `widget_template.xml` from `tkRAD/xml` to `tkRAD/xml/doc`;


### $ 2014-01-02 RS $

* updated `CHANGES`:

    * moved file from `CHANGES` to `CHANGES.md`;

    * rewritten text to best suit MarkDown (.md) syntax;


### $ 2013-12-31 RS $

* updated `RADMainWindow`:

    * in `connect_statusbar()`:

        * now only connects `self.statusbar` if it is of type
        `RADStatusBar` as devs may redefine `self.statusbar` to meet
        their own needs;

        * devs should override this method if they implement their
        own `MyStatusBar` type in `self.statusbar`;

* updated `RADXMLBase`:

    * in `get_xml_uri()`:

        * fixed ugly URI construction on faulty paths;

        * now `FileNotFoundError` exception traceback is clearer;


### $ 2013-12-30 RS $

* updated `RADStatusBar`:

    * in `toggle()`:

        * fixed bug when `self.toggle_var` is *NOT* set up;

        * added `[WARNING]` message to help developers know about it;


### $ 2013-12-29 RS $

* updated `RADXMLBase`:

    * in `register_object_by_id()`:

        * made it safer: objects of same `id` now raise `KeyError`;

        * no more faulty overridings;

* updated `RADXMLWidgetBase`:

    * `parse_attr_checked()` and `parse_attr_selected()` are now
    fully implemented;

    * in `_before_building_element()`:

        * added `self.WIDGET` for post-implementations of last built
        widget e.g. see `RADXMLWidget.build_element_checkbutton()`
        and `RADXMLWidget.build_element_radiobutton()` for more;

* updated `RADXMLWidget`:

    * in `build_element_checkbutton()`:

        * fixed attr `checked="checked"` bug due to `tkinter`
        inconsistencies --> must set `object.select()` rather than
        `cvar value` which is the exact opposite behaviour of
        `Menu.Checkbutton` menu item /!\;

    * in `build_element_radiobutton()`:

        * fixed attr `selected="selected"` bug due to `tkinter`
        inconsistencies --> must set `object.select()` rather than
        `cvar value` which is the exact opposite behaviour of
        `Menu.Radiobutton` menu item /!\;


### $ 2013-12-28 RS $

* updated `RADMainWindow`:

    * in `connect_statusbar()`:

        * fixed bug: `self.topmenu` and `self.mainframe` may *NOT*
        have attr `get_stringvar()` if user-defined otherwise;


### $ 2013-12-27 RS $

* updated `RADXMLWidgetBase`:

    * in `parse_attr_command()`:

        * event support now works along `Menu.tearoffcommand` 2 args;

* updated `RADXMLMenu`:

    * in `build_element_menu()`:

        * added restriction to `loop_on_child()`: menu now accepts
        only `<menu>`, `<command>`, `<checkbutton>`, `<radiobutton>`
        and `<separator>` XML subelements;


### $ 2013-12-25 RS $

* updated `RADStatusBar`:

    * added `toggle_var_set (self, value)`;

* updated `RADMainWindow`:

    * added `connect_statusbar (self, stringvarname)`;

* updated `RADXMLBase`:

    * added `get_cvars (self)`;

    * added `get_doublevars (self)`;

    * added `get_intvars (self)`;

    * added `get_stringvars (self)`;

* updated `RADXMLWidget`:

    * in `build_element_menu()`:

        * created menu widget is now registered with
        `register_object_by_id()`;

        * menu `stringvars` are now transferred to widget's
        `stringvars` collection;

* updated `RADXMLMenu`:

    * in `RADXMLMenu.ATTRS`:

        * commented all non-essential XML attrs to be init'ed;


### $ 2013-12-23 RS $

* fixed `WM_DELETE_WINDOW` bug @ easy.builder[2];


### $ 2013-12-22 RS $

* upgraded `tkRAD.easy.builder[2]` modules;

* now support `<tkwidget>` XML root node for testing;

* still support `<root>` XML root node for testing;

* rewritten some portions of code with no border effects;


### $ 2013-12-21 RS $

* updated `README.md` file to best suit to Markdown (.md) syntax;


### $ 2013-12-20 RS $

* set up first public release of `tkRAD` library;

* this is the first official version number: **2013.12.20b**;

* release name: **"Christmas Gift"**;

* prepared git repository on `GitHub`:

    git://github.com/tarball69/tkRAD.git

* cloned repository in:

    file://home/rs/apps/official/git/

* expanded GNU GPL v3 license ---> LGPL v3;

* filled with previous project files;

* written entire new `README` file;

* written entire new `CHANGES` file;

* updated license terms in all `*.py` file headers in the project;

* Merry Christmas you all!

===   END OF FILE   ===
