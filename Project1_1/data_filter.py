#!/usr/bin/env python3
import os
import re
import sys
import gzip
import numpy as np
from PercentDecoder import decode as decoder
import readjson


def filtdata(line, dic):
    regex = re.compile('\s+')
    strs = decoder(line)
    spstr = regex.split(strs)
    language = spstr[0]
    if language == 'en' or language == 'en.m':
        key = spstr[1]
        if key in dic:
            value = int(spstr[2])
            dic[key] = dic[key] + value
        elif filter_extension(key):
            if is_valid(key):
                if json_block(key):
                    if special_pages(key):
                        if disambiguation(key):
                            value = int(spstr[2])
                            dic[key] = value


def filter_extension(key):
    blacklist = ['.png', '.gif', '.jpg', '.jepg', '.tiff', '.tif', '.xcf',
                 'mid', 'ogg', 'ogv', '.svg', '.djvu', '.oga', '.flac',
                 '.opus', '.wav', '.webm', '.ico', '.txt']
    strs = key.split('.')
    ext = '.' + strs[len(strs) - 1]
    if ext in blacklist:
        return False
    else:
        return True


def is_valid(key):
    return (key[0].isupper() or key[0].isdigit())

def json_block(key):
    for i in readjson.blocklist:
        if i in key.lower():
            return False
    return True

def special_pages(key):
    special = ['404.php', 'Main_Page', '-']
    if key in special:
        return False
    else:
        return True

def disambiguation(key):
    ambiguation = '_(disambiguation)'
    if ambiguation in key:
        return False
    else:
        return True


if __name__ == '__main__':
    filteddic = {}
    while True:
        try:
            line = input()
            filtdata(line, filteddic)
        except:
            break
    outfilepath = 'output'
    outfile = open(outfilepath, 'wt', encoding='utf-8', newline='\n')
    outfile.seek(0)
    outfile.truncate()
    for i in filteddic:
        outfile.write(i + '\t' + str(filteddic[i]) + '\n', )
    outfile.close()
