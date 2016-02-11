#!/bin/sh

if [ $UID -ne 0 ]; then
    >&2 echo "must be root"
    exit 1
fi

MAPPING=$1

umount /mnt/$MAPPING && dmsetup remove $MAPPING
