#!/usr/bin/env python
# encoding: utf-8

import argparse
import sys

sys.path.append("..")

from patch import Patch

class MachoPatch(Patch):
    pass

def main():
    parser = argparse.ArgumentParser(description="aes and rsa(private and public) keygen")
    parser.add_argument("input", help="the static library to be patched")
    parser.add_argument("output", help="output library file name")
    parser.add_argument("--aes-enc", default=None, help="specify aes key file (encryption)", required=False)
    parser.add_argument("--aes-dec", default=None, help="specify aes key file (decryption)", required=False)
    parser.add_argument("--rsa-private", default=None, help="rsa private key file (der file format)", required=False)
    parser.add_argument("--rsa-public", default=None, help="rsa public key file (der file format)", required=False)
    args = parser.parse_args()

    patcher = MachoPatch(args.input, args.output, \
                       rsa_private_key=args.rsa_private,\
                       rsa_public_key=args.rsa_public,\
                       aes_enc=args.aes_enc,
                       aes_dec=args.aes_dec)
    patcher.patch_aes_enc()
    patcher.patch_aes_dec()
    patcher.patch_rsa_private()
    patcher.patch_rsa_public()

if __name__ == "__main__":
    main()
