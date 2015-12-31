#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Michael Liao (askxuefeng@gmail.com)'
import sys

"""
simple_rsa.py - a simple RSA encryption demo.
"""


def generate_keys(p, q):
    numbers = (11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    N = p * q
    C = (p-1) * (q-1)
    e = 0
    for n in numbers:
        if n < C and C % n > 0:
            e = n
            break
    if e==0:
        raise StandardError('e not found')
    # find d: e * d % C == 1
    d = 0
    for n in range(2, C):
        if (e * n) % C == 1:
            d = n
            break
    if d == 0:
        raise StandardError('d not found')
    return (N, e), (N, d)


def encrypt(m, key):
    C, x = key
    return (m ** x) % C


decrypt = encrypt


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pub, pri = generate_keys(47, 79)
    L = range(20, 30)
    C = map(lambda x: encrypt(x, pub), L)
    D = map(lambda x: decrypt(x, pri), C)
    print 'keys:', pub, pri
    print 'message:', L
    print 'encrypt:', C
    print 'decrypt:', D

