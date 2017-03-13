#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import platform

class Patch:
    def __init__(self, input_file, output_file, rsa_private_key=None, rsa_public_key=None, aes_enc=None, aes_dec=None):
        self.filename = input_file
        self.output_file = output_file
        self.rsa_private_key = rsa_private_key
        self.rsa_public_key = rsa_public_key
        self.aes_enc = aes_enc
        self.aes_dec = aes_dec

        self.file_data = self.read_file(self.filename)

    def __del__(self):
        self.save_file(self.output_file, self.file_data)

    def clean_aes(self):
        os.system("rm enc_* dec_*")

    def clean_rsa(self):
        os.system("rm *_MA n__* d__* DPMA DQMA BPMA")

    @staticmethod
    def choose_keygen(name):
        rst = name
        rst += '.' + platform.system()
        rst += '.' + platform.architecture()[0][:2]
        return rst

    @staticmethod
    def read_file(filename):
        fd = open(filename, 'rb')
        data = fd.read()
        fd.close()
        return data

    @staticmethod
    def save_file(filename, data):
        fd = open(filename, 'wb')
        fd.write(data)
        fd.close()

    def patch_data(self, value, offset, pattern_length=None):
        assert (offset <= len(self.file_data) and (offset + len(value)) <= len(self.file_data))
        if pattern_length is None:
            pattern_length = len(value)
        self.file_data = self.file_data[:offset] + value + self.file_data[offset+pattern_length:]

    def pattern_offset(self, pattern):
        offsets = []
        offset = self.file_data.find(pattern)
        while offset != -1:
            offsets.append(offset)
            offset = self.file_data.find(pattern, offset+1)
        return offsets

    def patch_pattern(self, pattern, new_data):
        offsets = self.pattern_offset(pattern)
        for offset in offsets:
            print "pattern \"%s\" offset: %08x" % (pattern, offset)
            self.patch_data(new_data, offset)

    #########################################
    #   patch
    #########################################
    def aes_symbol_to_pattern(self, symbol):
        return (symbol[:3] + symbol[-1]) * 61
    def rsa_symbol_to_pattern(self, symbol):
        return (symbol[:4]) * 2

    def patch_aes_symbol(self, symbol, pattern=None):
        if pattern is None:
            pat = self.aes_symbol_to_pattern(symbol)
        else:
            pat = pattern
        new_data = self.read_file(symbol)
        self.patch_pattern(pat, new_data)

    def patch_rsa_symbol(self, symbol, pattern=None):
        if pattern is None:
            pat = self.rsa_symbol_to_pattern(symbol)
        else:
            pat = pattern
        new_data = self.read_file(symbol)
        self.patch_pattern(pat, new_data)

    def patch_aes_enc(self):
        if self.aes_enc is not None:
            keygen = self.choose_keygen("../bin/aes_keygen")
            os.system("%s %s" % (keygen, self.aes_enc))

            self.patch_aes_symbol("enc_key_g0")
            self.patch_aes_symbol("enc_key_g1")

            self.clean_aes()

    def patch_aes_dec(self):
        if self.aes_dec is not None:
            keygen = self.choose_keygen("../bin/aes_keygen")
            os.system("%s %s" % (keygen, self.aes_dec))

            self.patch_aes_symbol("dec_key_g0")
            self.patch_aes_symbol("dec_key_g1")

            self.clean_aes()

    def patch_rsa_private(self):
        if self.rsa_private_key is not None:
            keygen = self.choose_keygen("../bin/rsa_keygen")
            os.system("%s %s" % (keygen, self.rsa_private_key))

            #self.patch_rsa_symbol("n__0")
            #self.patch_rsa_symbol("n__1")
            self.patch_rsa_symbol("d__0")
            self.patch_rsa_symbol("d__1")
            self.patch_rsa_symbol("K_MA", "K_MAK_MA")
            self.patch_rsa_symbol("N_MA", "N_MAN_MA")
            self.patch_rsa_symbol("E_MA", "E_MAE_MA")
            self.patch_rsa_symbol("P_MA", "P_MAP_MA")
            self.patch_rsa_symbol("Q_MA", "Q_MAQ_MA")
            self.patch_rsa_symbol("DPMA", "DPMADPMA")
            self.patch_rsa_symbol("DQMA", "DQMADQMA")
            self.patch_rsa_symbol("BPMA", "BPMABPMA")

            self.clean_rsa()

    def patch_rsa_public(self):
        if self.rsa_public_key is not None:
            keygen = self.choose_keygen("../bin/rsa_keygen")
            os.system("%s %s" % (keygen, self.rsa_public_key))

            self.patch_rsa_symbol("n__0")
            self.patch_rsa_symbol("n__1")
            #self.patch_rsa_symbol("d__0")
            #self.patch_rsa_symbol("d__1")
            self.patch_rsa_symbol("K_MA", "K2MAK2MA")
            self.patch_rsa_symbol("N_MA", "N2MAN2MA")
            #self.patch_rsa_symbol("E_MA")
            #self.patch_rsa_symbol("D_MA")

            self.clean_rsa()

