<!-- encoding: UTF-8  -->

# tkRAD

Tkinter Rapid Application Development (RAD) library.


## DESCRIPTION

`tkRAD` is a **Python3.2+** library designed to enable really Rapid
Application Development (RAD) process by using predefined classes to
derive in your own subclasses, with quite useful embedded services
such as dynamic **Tkinter XML widget** building, service manager,
events manager, RC configuration manager and so on.

`tkRAD` is a deliberately **short-made API** designed for comfort,
easiness and simplicity.

`tkRAD` provides the necessary **core tools** to quickly start up an
application development or for Tkinter widget testing through
`tkRAD.easy.builder` module - see '[BASIC USAGE](#basic-usage)'
examples below.


## LICENSE

tkRAD - tkinter Rapid Application Development library.

(c) 2013+ Raphaël SEBAN - e-mail: <motus@laposte.net>

This project is licensed under the **GNU LGPL v3** Lesser General
Public License.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.

If not, see http://www.gnu.org/licenses/


## FEATURES

The current public release of `tkRAD` supports at least:

* **Application frame** with `tkRAD.widgets.RADApplication` class;

* **Lightweight MainWindow** with `tkRAD.widgets.RADMainWindow` class;

* More complex **Tkinter XML widget factory** embedded in
`tkRAD.xml.RADXMLMainWindow` class;

* **Automagic XML menu** / submenu cascade handling with direct access
to submenus through `get_object_by_id()` class method, event-driven
commands support, automatic menu label underlining support and
keyboard accelerator support;

* **Tkinter XML widget** building through `tkRAD.xml.RADXMLFrame`
generic widget container class;

* Tkinter XML widget building for **easy TESTING** through
`tkRAD.easy.builder` module - see '[BASIC USAGE](#basic-usage)' below;

* some innovative and really **useful programming tools** in
`tkRAD.core` package modules;

Since `tkRAD` has been designed for subclassing, if you don't meet
your needs, just create your own implementations derived from
`tkRAD.xml` generic classes such as `RADXMLBase`, `RADXMLWidgetBase`
and `RADXMLWidget`.


## DEVELOPMENT STATUS

Classifier:

    Development Status :: 5 - Production/Stable

At this time, `tkRAD` library has been:

* Linux:

  * **TESTED OK** under Lubuntu, Xubuntu and Ubuntu;

  * should work quite fine under any Linux distribution;

* macOS:

  * **NOT YET TESTED**;

* MS-Windows:

  * **TESTED OK** under MS-Windows 8 with **Python v3.3.3**;

  * `tkRAD.easy.builder2` has been **TESTED OK** for **Python v2.7+**;

  * Code is very few platform-dependent and should remain STABLE in
  time between each release;

Any platform users feedback is still the welcome.


## CHANGES

Please, refer to `CHANGES.md` file for more detail.


## DOCUMENTATION

`tkRAD` is self-documented in its own source code;

feel free to use:

    $ pydoc3 -b

in a UNIX-like console terminal set in the closest parent directory
of `tkRAD/` e.g.:

    $ cd ~/tmp      # where you have ~/tmp/tkRAD/ copied in;

    $ pydoc3 -b

and study generated autodoc in your favourite internet browser;


## WIKI WIKI

Please, feel free to visit `tkRAD` internationalized (i18n) wiki
documentation for more detailed explanations, tips and tricks and
source code examples.

Last known URL: https://github.com/tarball69/tkRAD/wiki


## INSTALLATION

`tkRAD` package library does *NOT* really need to be installed.

Just [grab a zipped copy]
(https://github.com/tarball69/tkRAD/wiki/En%3Ainstall)
of `tkRAD/` directory into your own application's source library
and start using `tkRAD` by importing classes in your own code.

Since `tkRAD` library may evolve rapidly and thus might become less
compatible with your ongoing code development, it is a rather
relevant practice to keep your favourite `tkRAD` version copied into
your own application's source library.

### REQUIREMENTS

#### Mandatory requirements:

* `tkRAD` works fine with **Python v3.2 or later** installed on your
own OS platform;

* at least `tkinter` package must also be installed, which is the
common default case when you install Python;

make sure this package really exists on your system by entering in a
console terminal:

    $ python3

    >>> import tkinter    # case-sensitive /!\

if you get an error message, `tkinter` is *NOT* installed;

use your favourite package manager to solve this issue;

#### Optional requirements:

* only `tkRAD.easy.builder2` needs **Python v2.7 or later**
installed to work fine, since this module has been especially
designed for these early versions of Python;

* if you use `tkRAD.easy.builder2` with Python v2.7+, you must also
have `Tkinter` package installed, which is the common default case
when you install Python2.7+;

make sure this package really exists on your system by entering in a
console terminal:

    $ python

    >>> import Tkinter    # case-sensitive /!\

if you get an error message, `Tkinter` is *NOT* installed;

use your favourite package manager to solve this issue;


## BASIC USAGE

Let's play with `tkRAD`!

For this example series, we'll suppose you're under a UNIX-like
console terminal.

MS-Windows users, please see '[MS-WINDOWS USERS](#ms-windows-users)'
below.

Now [pick up a zipped copy]
(https://github.com/tarball69/tkRAD/wiki/En%3Ainstall)
of `tkRAD/` directory and put it in a temporary directory, let's
say into:

    $ cd ~/tmp

Unzip the archive (replace `xxx` by the real value) and then rename it:

    $ unzip tkRAD-xxx.zip

    $ mv tkRAD-xxx tkRAD

Notice: `$` symbol is the shell command-line prompt, you shall not
type it(!)

You should have something like this:

    $ ls

    tkRAD/
    tkRAD-xxx.zip

Dive into tkRAD's `easy` directory:

    $ cd tkRAD/easy

Call a **Python3.2+** interactive console and type:

    $ python3

    >>> import builder as B

Notice: `>>>` symbol is the Python interpreter prompt, you shall not
type it(!)

Remember it is *NOT* a good programming practice to use:

    >>> from builder import *       # /!\ NO /!\

Now, try the embedded XML example file:

    >>> B.build("builder-example.xml")

And tell your friends what you saw today.

### Another example

Keep your Python interpreter on and type:

    >>> import builder as B

    >>> xml = """

        <root>

            <label text="hello good people!" bg="white" fg="blue" />

            <button text="Quit" command="self.quit" />

        </root>

    """

    >>> B.build(xml)

As you can see, it is possible to check out some XML source code
directly into your Python code without the need of any external XML
file(!)

With **Python2.7+** you can (almost) do the same:

    $ python

    >>> import builder2 as B

    >>> B.build("builder-example.xml")

    And then:

    >>> xml = """

        <root>

            <label text="hello good people!" bg="white" fg="blue" />

            <button text="Quit" command="self.quit" />

        </root>

    """

    >>> B.build(xml)

Good day for programming, isn't it? :-)


## MS-WINDOWS USERS

MS-Windows users may easily try `tkRAD.easy.builder` by following
these steps:

* grab a copy of `tkRAD/` directory on your platform;

* put this copy into a temporary directory on your machine;

* browse with your file manager into `tkRAD/easy` directory;

* double-click on `builder.py` Python file if you have **Python
v3.2+** installed and take a look at the embedded example windows
that should pop-up automatically;

* double-click on `builder2.py` Python file if you have **Python
v2.7+** installed and take a look at the embedded example windows
that should pop-up automatically;

Please remember `tkRAD` library has entirely been designed for
**Python version 3.2** or later, *NOT* for **Python version 2.7** or
later.

**CAUTION: /!\ Only `builder2.py` is Python2.7+ compatible /!\**


## THE LITTLE STORY

For the little story, the very first public release of `tkRAD` was
entirely written with an ASUS 1001PX **NETBOOK**(!) computer, under
a Linux Lubuntu 13.10 distro for the need of a Video Editor: Qut.

It was in December 2013 and it is a TRUE story.

Enjoy!
