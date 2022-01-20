import binascii
import os


class Config(object):
    SECRET_KEY = binascii.hexlify(os.urandom(24))
