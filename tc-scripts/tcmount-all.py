#!/usr/bin/env python3

import os
import os.path
import subprocess
import sys
import tempfile

from getpass import getpass

DEVICES=['sdb1', 'sdd1', 'sde1', 'sdf1', 'sdg1']

class TcplayException(Exception):
    pass

def tcmount(password, device, mapping, mountpoint=None):
    if mountpoint is None:
        mountpoint = os.path.join('/mnt', mapping)

    tcplay_args = ['tcplay', '-m', mapping, '-d', device]
    proc = subprocess.Popen(tcplay_args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc.communicate((password + os.linesep).encode('utf-8'))
    res = proc.wait()
    if res != 0:
        raise TcplayException()

    mount_args = ['mount', os.path.join('/dev/mapper', mapping), mountpoint]
    subprocess.check_call(mount_args)

def tcumount(mapping, mountpoint=None):
    if mountpoint is None:
        mountpoint = os.path.join('/mnt', mapping)

    umount_args = ['umount', mountpoint]
    subprocess.check_call(umount_args)

    dmsetup_args = ['dmsetup', 'remove', mapping]
    subprocess.check_call(dmsetup_args)

def mount(device_name, password):
    device      = os.path.join('/dev', device_name)
    tmpdir      = tempfile.mkdtemp(prefix='tcmount_')
    tcinfo_path = os.path.join(tmpdir, 'tcinfo')
    mapping     = os.path.basename(tmpdir)

    tcmount(password, device, mapping, tmpdir)

    tcinfo = ''
    with open(tcinfo_path, 'r') as f:
        tcinfo = f.read().strip()

    tcumount(mapping, tmpdir)
    os.rmdir(tmpdir)

    if len(tcinfo) == 0:
        raise Exception('tcinfo file missing or empty')

    print("{} => {}".format(device, tcinfo))
    tcmount(password, device, tcinfo)

def is_root():
    return os.geteuid() == 0

if __name__ == '__main__':
    if not is_root():
        print("must be root", file=sys.stderr)
        sys.exit(1)

    password = getpass()
    for dev in DEVICES:
        try:
            mount(dev, password)
        except Exception as e:
            print("{} failed".format(dev), file=sys.stderr)
