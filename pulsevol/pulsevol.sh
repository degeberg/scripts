#!/bin/bash

STEP='2dB'

default_sink=$(pacmd list-sinks | awk '/* index:/{ print $3 }')
muted=$(pacmd list-sinks | grep -A 15 '* index' |awk '/muted:/{ print $2 }')
volume=$(pacmd list-sinks | grep -A 15 '* index' | awk '/volume: front/{ print $7 }')

case "$1" in
    "up")
        if [ $volume == "-inf" ]; then
            pactl set-sink-volume $default_sink "0dB"
            pactl set-sink-volume $default_sink -- "-60dB"
        else
            pactl set-sink-volume $default_sink -- "+$STEP"
        fi
        ;;
    "down")
        pactl set-sink-volume $default_sink -- "-$STEP"
        ;;
    "set-volume")
        pactl set-sink-volume $default_sink $2
        ;;
    "mute")
        pactl set-sink-mute $default_sink 1
        ;;
    "unmute")
        pactl set-sink-mute $default_sink 0
        ;;
    "mute-toggle")
        pactl set-sink-mute $default_sink toggle
        ;;
    "muted")
        echo $muted
        ;;
    "volume")
        echo "$volume dB"
        ;;
    "volume-xmobar")
            if [ $muted == "no" ]; then
                echo "Vol: <fc=green>$volume</fc> dB"
            else
                echo "Vol: $volume dB"
            fi
        ;;
esac

