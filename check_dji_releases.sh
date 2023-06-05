#!/bin/bash

# Add `gh` command line
export PATH="$PATH:/opt/homebrew/bin/"

function notify() { 
    input="$(cat)"
    osascript -e "display notification \"$input\" with title \"DJI Releases\""
    echo "$input"
}

~/.bin/DJIReleaseNotes/scrap_dji_releases.py | notify 2>&1 | tee ~/dji.log
