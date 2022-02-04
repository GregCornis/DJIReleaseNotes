#!/bin/bash

function notify() { 
    input="$(cat)"
    osascript -e "display notification \"$input\" with title \"DJI Releases\""
}

~/.bin/DJIReleaseNotes/scrap_dji_releases.py | notify 2>&1 | tee ~/dji.log