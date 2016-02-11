#!/bin/sh

if [ $UID -ne 0 ]; then
    >&2 echo "must be root"
    exit 1
fi

MAPPING=$1
DEVICE=$2

tcplay --map=$MAPPING --device=$DEVICE && mount /dev/mapper/$MAPPING /mnt/$MAPPING
