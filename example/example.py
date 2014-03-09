#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------   trying to import   ------------------------

try:

    import tkRAD

except ImportError:

    print(
        "\n[CAUTION] tkRAD is *NOT* installed."
        "\nPlease, refer to README file for installation instructions."
        "\nNow trying to get tkRAD locally (maybe)..."
        "\n"
    )

    import SOS_tkRAD as tkRAD

    import tkinter as TK

    root = TK.Tk()

    root.withdraw()

    TK.messagebox.showwarning(

        "CAUTION",

        "tkRAD library is *NOT* installed. Trying locally.",

        parent = root,
    )

    # CAUTION: these avoid weird future behaviour of tkinter

    root.destroy()

    del root

# unsupported exception

except:

    raise

    exit(1)

# end try

# -----------------------   STARTING demo app   ------------------------

app = tkRAD.RADApplication(xml_menu="topmenu")

app.run()

exit(0)

# that's all, folks!
