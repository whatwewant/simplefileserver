#!/usr/bin/env python
# coding=utf-8

import sys
from .server_side import server

def main():


    if len(sys.argv) == 1:
        server()
    elif len(sys.argv) == 2:
        server(sys.argv[1])
    else:
        print('Usage:\n\t%s ServerPort' % sys.argv[0].split('/').pop())
