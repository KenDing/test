#!/usr/bin/env python
# encoding: utf-8

import argparse
import sys
import struct

sys.path.append("..")

from patch import Patch

class BitCodePatch(Patch):
    def patch_aes_symbol(self, symbol, pattern=None):
        if pattern is None:
            pat = self.aes_symbol_to_pattern(symbol)
        else:
            pat = pattern

        p = []
        for i in xrange(0, len(pat), 4):
            s = struct.unpack("<I", pat[i:i+4])[0]
            s = "i32 %d" % s
            p.append(s)
        pat = ", ".join(p)


        new_data = self.read_file(symbol)
        p = []
        for i in xrange(0, len(new_data), 4):
            s = struct.unpack("<i", new_data[i:i+4])[0]
            s = "i32 %d" % s
            p.append(s)
        new_data = ", ".join(p)


        if pat in self.file_data:
            l = len(pat)
            self.patch_data(new_data, self.file_data.find(pat), l)

    def patch_rsa_symbol(self, symbol, pattern=None):
        import random
        if pattern is None:
            pat = self.rsa_symbol_to_pattern(symbol)
        else:
            pat = pattern
        if pat in self.file_data:
            print pat
            d = self.file_data[self.file_data.find(pat):]
            l = d.find("\"")+1
            new_data = self.read_file(symbol)
            t =  {"K_MA":2048, "K2MA":2048, "E_MA":16}
            if symbol in t.keys():
                while len(new_data) < t[symbol]:
                    new_data += chr(random.randint(0, 255))
            new_data = "".join(map(lambda c:"\\%02X" % ord(c), new_data)) + "\""
            self.patch_data(new_data, self.file_data.find(pat), l)

def main():
    parser = argparse.ArgumentParser(description="aes and rsa(private and public) keygen")
    parser.add_argument("input", help="the static library to be patched")
    parser.add_argument("output", help="output library file name")
    parser.add_argument("--aes-enc", default=None, help="specify aes key file (encryption)", required=False)
    parser.add_argument("--aes-dec", default=None, help="specify aes key file (decryption)", required=False)
    parser.add_argument("--rsa-private", default=None, help="rsa private key file (der file format)", required=False)
    parser.add_argument("--rsa-public", default=None, help="rsa public key file (der file format)", required=False)
    args = parser.parse_args()

    patcher = BitCodePatch(args.input, args.output, \
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
