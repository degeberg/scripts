#!/bin/sh

function disk_status {
    DISKS=("/mnt/tc1"
           "/mnt/tc2"
           "/mnt/tc3"
           "/mnt/tc4"
           "/mnt/tc5")
    SOME=0
    ALL=1
    L="$1"

    for d in "${DISKS[@]}"; do
        mountpoint --quiet $d
        if [ $? -eq 0 ]; then
            SOME=1
        else
            ALL=0
        fi
    done

    if [ $ALL -eq 1 ]; then
        echo -n "<fc=green>$L</fc>"
    elif [ $ALL -eq 0 ] && [ $SOME -eq 1 ]; then
        echo -n "<fc=orange>$L</fc>"
    else
        echo -n "<fc=red>$L</fc>"
    fi
}

function display {
    if [ $? -eq 0 ]; then
        echo -n "<fc=green>$1</fc>"
    else
        echo -n "<fc=red>$1</fc>"
    fi
}

function prog {
    p="$1"
    out="$2"
    pgrep -c $p > /dev/null
    display $out
}

function systemd_service {
    service="$1.service"
    out="$2"
    systemctl --quiet is-active $service
    display $out
}

H=$(hostname)

if [ "$H" == "daniel-thinkpad" ] || [ "$H" == "daniel-desktop" ]; then
    systemd_service crashplan       B
fi

if [ "$H" == "daniel-desktop" ]; then
    disk_status                     E
    systemd_service plexmediaserver P
    prog            nzbget          N
    systemd_service sonarr          S
    systemd_service couchpotato     C
    systemd_service deluged         D
fi
