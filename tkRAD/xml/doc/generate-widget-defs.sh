#!/bin/bash

cd $(dirname "$0")

pwd

ATTRLIST="tkinter-widget-specific-attributes.txt"

TEMPLATE="parse-attr-template.py"

OUTFILE="rad_xml_widget-parse_attr-defs.py"

echo > "$OUTFILE"

for ATTR in $(cat "$ATTRLIST")

    do
        cat "$TEMPLATE" | sed -e "s/{attr_name}/$ATTR/" >> $OUTFILE

    done

cat $OUTFILE

exit 0
