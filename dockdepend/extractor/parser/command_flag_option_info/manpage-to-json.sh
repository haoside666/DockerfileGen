#!/bin/bash
if [ -n "$2" ]; then  
    find_match_type="$2"  
else  
    find_match_type="0"
fi  
man $1 | grep '^       -' | sed -E 's/^\s+//g' | python3 args-to-json.py $find_match_type
