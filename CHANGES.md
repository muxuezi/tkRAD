<!-- encoding: UTF-8 -->


## CONTRIBUTORS

    RS    Raphaël SEBAN


## CHANGELOG

### $ 2014-01-04 RS $

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
