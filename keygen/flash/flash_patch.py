#!/usr/bin/env python
# encoding: utf-8

import sys
import argparse

sys.path.append("..")

from patch import Patch

class FlashPatch(Patch):
    def patch_aes_symbol(self, symbol, pattern=None):
        if pattern is None:
            pat = self.aes_symbol_to_pattern(symbol).encode("hex")
        else:
            pat = pattern
        new_data = self.read_file(symbol).encode("hex")
        self.patch_pattern(pat, new_data)

    def patch_rsa_symbol(self, symbol, pattern=None):
        if pattern is None:
            pat = self.rsa_symbol_to_pattern(symbol).encode("hex")
        else:
            pat = pattern
        new_data = self.read_file(symbol).encode("hex")
        self.patch_pattern(pat, new_data)


def main():
    parser = argparse.ArgumentParser(description="aes and rsa(private and public) keygen")
    parser.add_argument("input", help="the static library to be patched")
    parser.add_argument("output", help="output library file name")
    parser.add_argument("--aes-enc", default=None, help="specify aes key file (encryption)", required=False)
    parser.add_argument("--aes-dec", default=None, help="specify aes key file (decryption)", required=False)
    parser.add_argument("--rsa-private", default=None, help="rsa private key file (der file format)", required=False)
    parser.add_argument("--rsa-public", default=None, help="rsa public key file (der file format)", required=False)
    args = parser.parse_args()

    patcher = FlashPatch(args.input, args.output, \
                       rsa_private_key=args.rsa_private,\
                       rsa_public_key=args.rsa_public,\
                       aes_enc=args.aes_enc,
                       aes_dec=args.aes_dec)
    patcher.patch_aes_enc()
    patcher.patch_aes_dec()
    patcher.patch_rsa_private()
    patcher.patch_rsa_public()
    return

if __name__ == "__main__":
    main()
