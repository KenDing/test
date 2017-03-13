#!/usr/bin/env python
# encoding: utf-8

import os
import argparse
import sys

sys.path.append("..")

from patch import Patch

class JSPatch(Patch):
    def encode(self, data):
        rst = ','.join(map(lambda x: str(ord(x)), data))
        return rst

    def aes_symbol_to_pattern(self, symbol):
        pat = self.encode((symbol[:3] + symbol[-1]) * 61)
        return pat

    def patch_pattern(self, pattern, new_data, isRsa = False):
        new_data = self.encode(new_data)
        offsets = self.pattern_offset(pattern)

        assert len(offsets) in [0, 1]
        if len(offsets) == 0:
            return
        offset = offsets[0]

        print "pattern \"%s\" offset: %08x" % (pattern, offset)
        if not isRsa:
            self.patch_data(new_data, offset, len(pattern))
        else:
            tempdata = self.file_data
            count = new_data.count(",")
            start = offset
            for x in xrange(count):
                start = tempdata.find(',', start)+1
            start1 = tempdata.find(',', start)
            start2 = tempdata.find(']', start)
            start = start2
            if start1 > 0 and start1 < start2:
                start = start1
            assert start > 0
            self.patch_data(new_data, offset, start-offset)



    def patch_rsa_symbol(self, symbol, pattern=None):
        if pattern is None:
            #pat = self.rsa_symbol_to_pattern(symbol)
            return
        else:
            pat = self.encode(pattern)
        new_data = self.read_file(symbol)
        self.patch_pattern(pat, new_data, True)

def main():
    parser = argparse.ArgumentParser(description="aes and rsa(private and public) keygen")
    parser.add_argument("input", help="the static library to be patched")
    parser.add_argument("output", help="output library file name")
    parser.add_argument("--aes-enc", default=None, help="specify aes key file (encryption)", required=False)
    parser.add_argument("--aes-dec", default=None, help="specify aes key file (decryption)", required=False)
    parser.add_argument("--rsa-private", default=None, help="rsa private key file (der file format)", required=False)
    parser.add_argument("--rsa-public", default=None, help="rsa public key file (der file format)", required=False)
    args = parser.parse_args()

    patcher = JSPatch(args.input, args.output, \
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
