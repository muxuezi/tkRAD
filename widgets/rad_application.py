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

from ..core import checkups

from ..core import i18n

from ..core import path

from ..core import tools



class RADApplication:
    r"""
        Rapid Application Development (RAD) base application class for

        GUI and non-GUI implementations;

        feel free to subclass it in order to meet your needs;
    """



    APP = {

        "name": _("My Application"),

        "version": _("0.1a"),

        "title": _("My Application is wonderful!"),

        "author": _("my name <email@domain.org>"),

        "copyright": _("(c) YEAR author name."),

        "license": _("""
            This program is free software: you can redistribute it
            and/or modify it under the terms of the GNU General
            Public License as published by the Free Software
            Foundation, either version 3 of the License, or (at your
            option) any later version.

            This program is distributed in the hope that it will be
            useful, but WITHOUT ANY WARRANTY; without even the
            implied warranty of MERCHANTABILITY or FITNESS FOR A
            PARTICULAR PURPOSE. See the GNU General Public License
            for more details.

            You should have received a copy of the GNU General Public
            License along with this program.

            If not, see: http://www.gnu.org/licenses/
        """),

        "license_uri": _("http://www.gnu.org/licenses/"),

    } # end of APP



    DIRECTORIES = (

        #~ "etc", "lib", "locale", "xml",

    ) # end of DIRECTORIES



    PYTHON = {

        "version": "3.2",

        "strict": False,

    } # end of PYTHON



    RC_OPTIONS = {

        "user_file": "myapp.rc",

        "user_dir": "~/.config/myapp",

        "app_file": "app.rc",

        "app_dir": "^/etc",

    } # end of RC_OPTIONS



    def __init__ (self, **kw):
        r"""
            class constructor;

            no return value (void);
        """

        # application-wide inits

        self._check_python(**kw)

        self._init_members(**kw)

        self._init_service(**kw)

        self._init_root_dir(**kw)

        self._init_options(**kw)

        self._init_i18n(**kw)

        self._parse_sys_argv(**kw)

        self._check_dependencies(**kw)

    # end def



    def _check_dependencies (self, **kw):
        r"""
            protected method def;

            checks up for app-vital directories and other dependencies;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # notice: failed checkups will raise exception

        if not kw.get("no_dependencies"):

            checkups.check_directories(

                tools.choose_str(

                    kw.get("app_root_dir"),

                    path.get_app_root_dir(),
                ),

                *kw.get("check_dirs", self.DIRECTORIES)
            )

        # end if

    # end def




    def _check_python (self, **kw):
        r"""
            protected method def;

            checks up Python language version number

            for compatibility with this application;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # inits

        _python = {

            "version": tools.choose_str(

                kw.get("python_version"),

                self.PYTHON.get("version"),

                "3.2",
            ),

            "strict": tools.choose(

                kw.get("python_strict"),

                self.PYTHON.get("strict"),

                False,
            ),
        }

        # notice: failed checkups will raise exception and exit()

        checkups.python_require(**_python)

    # end def



    def _init_i18n (self, **kw):
        r"""
            protected method def;

            inits internationalization (i18n);

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # inits

        i18n.install(

            lc_dir = tools.choose_str(

                kw.get("lc_dir"),

                self.options["app"].get("lc_dir"),

                "^/locale",
            ),

            lc_lang = tools.choose_str(

                kw.get("lc_lang"),

                self.options["app"].get("lc_lang"),
            ),
        )

    # end def



    def _init_members (self, **kw):
        r"""
            protected method def;

            inits class members;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # member inits

        self._set_run_mode(tools.choose_str(kw.get("run_mode"), "GUI"))

        self.__kw = kw

    # end def



    def _init_options (self, **kw):
        r"""
            protected method def;

            inits all internal app rc options;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # lib imports

        from ..core import options as OPT

        # init user options

        self.user_options = OPT.get_option_manager()

        self.user_options.set_config_dir(

            tools.choose_str(

                kw.get("rc_dir"),

                self.RC_OPTIONS.get("user_dir"),
            )
        )

        self.user_options.set_config_file(

            tools.choose_str(

                kw.get("rc_file"),

                self.RC_OPTIONS.get("user_file"),
            )
        )

        # get a private option manager for this class /!\

        self.options = OPT.OptionManager()

        self.options.set_config_dir(

            tools.choose_str(

                kw.get("app_rc_dir"),

                self.RC_OPTIONS.get("app_dir"),
            )
        )

        self.options.set_config_file(

            tools.choose_str(

                kw.get("app_rc_file"),

                self.RC_OPTIONS.get("app_file"),
            )
        )

        # init default values

        self.options.set_sections("app")

        # get application rc options

        self.options.load()

        # member inits

        self._set_run_mode(

            tools.choose_str(

                self.options["app"].get("run_mode"),

                self._run_mode(**kw),
            )
        )

    # end def



    def _init_root_dir (self, **kw):
        r"""
            protected method def;

            inits application's root directory;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # lib imports

        import inspect

        path.set_app_root_dir(

            tools.choose_str(

                kw.get("app_root_dir"),

                inspect.stack()[-1][1],
            )
        )

        # free some useless memory right now /!\

        del inspect

    # end def



    def _init_service (self, **kw):
        r"""
            protected method def;

            registers this app class as an app-wide service;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # lib imports

        from ..core import services as SM

        # member inits

        self.services = SM.get_service_manager()

        # will raise KeyError if service name already registered

        self.services.register_service(

            tools.choose_str(kw.get("app_service"), "app"),

            self
        )

        # force service name to be this class /!\

        self.services.register_service(

            "application",

            self,

            silent_mode = True,
        )

    # end def



    def _parse_sys_argv (self, **kw):
        r"""
            protected method def;

            parses sys.argv CLI parameters;

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        # lib imports

        import argparse as AP

        # sys.argv[] argument parser

        _parser = AP.ArgumentParser(

            description = _(

                "{classname} class console argument parser."

            ).format(classname = self.__class__.__name__)
        )

        # init CLI arguments

        _parser.add_argument(

            "-m", "--run-mode",

            nargs = 1,

            default = ["gui"],

            type = str,

            choices = ["gui", "GUI", "cli", "CLI"],

            help = _(

                "determines whether application should run "

                "in Graphical User Interface mode (GUI) or "

                "in Command-Line Interface mode (CLI - console)."
            ),
        )

        # console help asked?

        if kw.get("help"):

            _parser.print_help()

        # end if

        # parse sys.argv[] arguments

        self.sys_argv = _parser.parse_args()

        # member inits

        self._set_run_mode(

            tools.choose_str(

                kw.get("run_mode"),

                self.sys_argv.run_mode[0],

                "GUI",
            )
        )

        # free some useless memory right now /!\

        del AP

    # end def



    def _run_mode (self, **kw):
        r"""
            protected method def;

            run_mode property getter;

            should return only "GUI" or "CLI" char strings;
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        return self.__run_mode

    # end def



    def _set_run_mode (self, mode):
        r"""
            protected method def;

            run_mode property setter;

            must be either 'CLI' or 'GUI';

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        mode = str(mode).upper()

        if mode != "CLI":

            mode = "GUI"

        # end if

        self.__run_mode = mode

    # end def



    def _start_cli (self, **kw):
        r"""
            protected method def;

            starts non-GUI implementation of this application;

            CLI: Command-Line Interface (shell console);

            no return value (void);
        """

        # this is a minimal example
        # feel free to put here your
        # own code in subclasses /!\

        print(

            _(
                "\n[INFO] this is the non-GUI implementation of your "

                "application program.\n\nFeel free to implement it "

                "at your taste in subclasses."

                "\n\n*** Program end ***"
            )
        )

    # end def



    def _start_gui (self, **kw):
        r"""
            protected method def;

            starts GUI implementation of this application;

            no return value (void);
        """

        # this is a specific example
        # feel free to put here your
        # own code in subclasses /!\

        # lib imports

        from ..xml import rad_xml_mainwindow as MW

        self.mainwindow = MW.RADXMLMainWindow(**kw)

        try:

            if kw.get("xml_menu"):

                self.mainwindow.topmenu.xml_build(kw.get("xml_menu"))

            # end if

            self.mainwindow.mainframe.xml_build(kw.get("xml"))

            self.mainwindow.connect_statusbar("show_statusbar")

            self.mainwindow.run()

        except FileNotFoundError:

            if not self.mainwindow.mainframe.winfo_children():

                self.mainwindow.mainframe.xml_build(
                    r"""
                    <tkwidget>
                        <frame
                            layout="pack"
                            resizable="yes"
                        />
                        <label
                            text="this should better work with:"
                            layout="pack"
                        />
                        <label
                            text="{path}"
                            fg="red"
                            layout="pack"
                        />
                        <label
                            text="/!\ don't forget to create missing directories /!\"
                            layout="pack"
                        />
                        <button
                            text="Quit"
                            command="@quit"
                            layout="pack"
                        />
                        <frame
                            layout="pack"
                            resizable="yes"
                        />
                    </tkwidget>
                    """
                    .format(

                        path = self.mainwindow.mainframe.get_xml_path()
                    )
                )

                self.mainwindow.run()

            else:

                raise

            # end if

        # end try

    # end def



    def run (self, **kw):
        r"""
            starts up GUI or non-GUI implementation of this

            application along @kw param, sys.argv params and rc
            options;

            no return value (void);
        """

        # param inits

        self.__kw.update(kw)

        kw = self.__kw

        # determine run mode

        if "GUI" in str(self._run_mode(**kw)).upper():

            # run in Graphical User Interface (GUI) mode

            self._start_gui(**kw)

        else:

            # run in Command-Line Interface (CLI) mode

            self._start_cli(**kw)

        # end if

    # end def


# end class RADApplication
