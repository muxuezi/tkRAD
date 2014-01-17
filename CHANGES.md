<!-- encoding: UTF-8 -->


## CONTRIBUTORS

    RS    Raphaël SEBAN


## CHANGELOG


### $ 2014-01-17 RS $

* updated `RADXMLWidgetBase`:

    * in `_tkRAD_widget_support()`:

        * added new aliases in attr value:

            * `@top` for `tk_owner.winfo_toplevel()` widget;

            * `@parent` for `tk_parent` widget;

* updated `RADXMLWidget`:

    * added
    new `parse_attr_maxheight()`,
    new `parse_attr_maxwidth()`,
    new `parse_attr_minheight()`,
    new `parse_attr_minwidth()`,
    new `parse_attr_transient()`:

        * now fully implemented;

        * specific attributes for `<toplevel>` XML element;

    * added new `_layout_toplevel()`:

        * now fully implemented;

        * Toplevel window special layouts and inits;

    * updated
    `_set_layout()`,
    `parse_attr_height()`,
    `parse_attr_width()`:

        * now handles special support for `tkinter.Toplevel` widget
        case;

    * added new `parse_attr_title()`:

        * now fully implemented;

        * specific attr for `<toplevel>` XML element;

    * added new `parse_attr_visibility()`:

        * now fully implemented;

        * must be one of 'normal', 'maximized', 'minimized',
        'hidden' fixed values;

        * specific attr for `<toplevel>` XML element;

    * in `parse_attr_seq()`:

        * new implementation;

        * now admits simplified notation e.g. `seq="Control-s"`
        instead of `seq="&lt;Control-s&gt;"` for more comfort;

    * in `build_element_tkevent()`:

        * fixed many bugs;


### $ 2014-01-16 RS $

* updated `RADXMLMenu`:

    * revised/optimized code almost anywhere;

    * updated all `parse_attr_*()` protos along real needs;

* updated `RADXMLBase`:

    * added new `element_get_id(self, xml_element)`:

        * now fully implemented;

    * in `parse_xml_attributes()`:

        * now assumes larger anonymous parser protos `parser(**kw)`;

* updated `RADXMLAttribute`:

    * added new `update_xml_element(self, value=None)`:

        * updates inner XML element's attribute of `attribute.name`
        name along a given `@value` param or inner `attribute.value`
        if `@value` param is `None` or omitted;

        * now fully implemented;

* updated `RADXMLWidgetBase`:

    * revised/optimized code almost anywhere;

    * added
    new `_tkRAD_bitmap_support()`,
    new `_tkRAD_image_support()`:

        * CAUTION: to be implemented;

    * added
    new `_tkRAD_state_support()`,
    new `_tkRAD_cursor_support()`,
    new `_tkRAD_widget_support()`,
    new `_is_unparsed()`,
    new `_tkRAD_command_support()`,
    new `_tkRAD_font_support()`,
    new `_tkRAD_relief_support()`,
    new `_tkRAD_cvar_support()`:

        * now fully implemented;

    * updated all `parse_attr_*()` protos along real needs;

    * in `_fix_values()`, `parse_attr_id()`:

        * now supports `attribute.update_xml_element()`;

    * in `parse_attr_checked()`, `parse_attr_selected()`:

        * now implemented along `_tkRAD_boolean_support()`;

    * in `_tkRAD_boolean_support()`:

        * now supports `attribute.update_xml_element()`;

        * now admits logical values such as '1', '0', 'yes', 'no',
        'true', 'false' or `attribute name` itself (W3C compliant)
        e.g. `selected="selected"`;

* updated `RADXMLWidget`:

    * revised/optimized code almost anywhere;

    * updated all `parse_attr_*()` protos along real needs;

    * in `parse_attr_wrap()`:

        * now supports fixed values 'char', 'word', 'none' for XML
        element `<text>`;

        * still supports default boolean values '0', '1' for other
        XML elements;


### $ 2014-01-15 RS $

* updated `RADXMLWidgetBase`:

    * removed `_tk_child_config()`:

        * now merged into `_tk_config(**kw)` with
        `kw.get("tk_child_config")` keyword flag instead;

    * added new `_tkRAD_dimension_support()`:

        * now fully implemented;

    * in `_tk_child_config()`:

        * added support for `_` discriminator in attr `_name` in
        order to avoid `tkinter` TK_CONFIG attrs conflict;

* updated `RADXMLWidget`:

    * added new `parse_attr__after()`, `parse_attr__before()`,
    `parse_attr__height()`, `parse_attr__minsize()`,
    `parse_attr__padx()`, `parse_attr__pady()`,
    `parse_attr__sticky()`, `parse_attr__width()`:

        * now fully implemented;

        * kept for easiness and comfort: `parse_attr_after()`,
        `parse_attr_before()`, `parse_attr_minsize()`,
        `parse_attr_sticky()`;

    * in `_set_layout()`:

        * now `tkinter.PanedWindow` child layout management fully
        implemented;

        * now attr `resizable` may override attr `sticky` if omitted;


### $ 2014-01-14 RS $

* updated `RADXMLWidgetBase`:

    * updated all `parse_attr_*()` along new `_tkRAD_*_support()`;

    * added new `_tk_child_config()`:

        * now fully implemented;

    * in `_before_building_element()`:

        * added new dict() `TK_CHILD_CONFIG`;

    * moved `ANCHORS` to `RADXMLWidget`;

    * in `parse_attr_compound()`:

        * now fully implemented;

    * in `parse_attr_command()`:

        * in event support: extended number of inner `tkinter` args
        to undefined (*args);

    * added new `_tkRAD_color_support()`,
    new `_tkRAD_float_support()`,
    new `_tkRAD_integer_support()`,
    new `_tkRAD_any_value_support()`:

        * now fully implemented;

* updated `RADXMLWidget`:

    * updated all known and possible `parse_attr_*()` along new
    `_tkRAD_*_support()`;

    * in `parse_attr_layout()`:

        * default value is now `layout="none"` (**no layout**)
        instead of previous **risky** default value `layout="pack"`;

    * in `parse_attr_format()`:

        * now fully implemented;

        * supports `%03.2f` format as in `sprintf()`;

        * accepts simplified `03.2` notation;

    * in `parse_attr_buttonup()`:

        * now implemented along `parse_attr_relief()`;

    * in `parse_attr_class()`:

        * optimized code;

    * in `parse_attr_repeatdelay()`, `parse_attr_repeatinterval()`:

        * now fully implemented;

    * in `parse_attr_confine()`, `parse_attr_jump()`:

        * now implemented along `_tkRAD_boolean_support()`;


### $ 2014-01-13 RS $

* updated `RADXMLWidget`:

    * in `parse_attr_xscrollincrement()`,
    `parse_attr_yscrollincrement()`,
    `parse_attr_wraplength()`,
    `parse_attr_takefocus()`,
    `parse_attr_sliderlength()`,
    `parse_attr_troughcolor()`,
    `parse_attr_tickinterval()`,
    `parse_attr_resolution()`,
    `parse_attr_to()`,
    `parse_attr_from_()`,
    `parse_attr_showvalue()`,
    `parse_attr_readonlybackground()`,
    `parse_attr_pady()`,
    `parse_attr_padx()`,
    `parse_attr_orient()`,
    `parse_attr_offrelief()`,
    `parse_attr_length()`,
    `parse_attr_insertwidth()`,
    `parse_attr_insertborderwidth()`,
    `parse_attr_insertbackground()`,
    `parse_attr_indicatoron()`,
    `parse_attr_highlightthickness()`,
    `parse_attr_highlightcolor()`,
    `parse_attr_highlightbackground()`,
    `parse_attr_height()`,
    `parse_attr_exportselection()`,
    `parse_attr_elementborderwidth()`,
    `parse_attr_disabledbackground()`,
    `parse_attr_digits()`,
    `parse_attr_buttondownrelief()`,
    `parse_attr_buttonbackground()`:

        * now fully implemented;

    * in `parse_attr_module()`:

        * now module `id` *NOT* found raises `KeyError`;

    * in `parse_attr_sliderrelief()`,
    `parse_attr_sashrelief()`,
    `parse_attr_overrelief()`,
    `parse_attr_activerelief()`:

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
