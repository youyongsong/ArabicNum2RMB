#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A simple module which implements an algorithm that can convert
an Arabic number to RMB.
'''

__author__ = 'YouYongsong'

import os
import logging
import re

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), 
                    level = logging.WARNING)

# 将整数部分每4位数为1个列表分切割为3个字符列表
# 950356721 => (['0', '0', '0', '9'],
#               ['5', '0', '3', '5'],
#               ['6', '7', '2', '1'])
_integer = (['0', '0', '0', '0'], ['0', '0', '0', '0'],
            ['0', '0', '0', '0'])
# 将小数部分切割为两个字符存于一个列表中
_demical = ['0', '0']
_digit_table = {
    '0' : u'零', '1' : u'壹', '2' : u'贰', '3' : u'叁', '4' : u'肆',
    '5' : u'伍', '6' : u'陆', '7' : u'柒', '8' : u'捌', '9' : u'玖'
    }
_integer_levels = (u'亿', u'万', u'')
_demical_levels = (u'角', u'分')
_integer_unit_levels = (u'仟', u'佰', u'拾', u'')


# 主功能函数，完成将阿拉伯数字转换为人民币形式的字符串的功能
def convert(num):
    ''' Return a unicode string
    convert() recive an Arabic number, and will return a unicode
    string which represents RMB
    '''
    _divideNum(num)
    intStr = _dealIntZeros(_makeIntStr())
    demStr = _makeDemStr()
    if _isDemical():
        if intStr:
            return intStr + u'圆' + demStr
        else:
            return demStr
    else:
        if intStr:
            return intStr + u'圆整'
        else:
            return u'零圆整'

# 将阿拉伯数字转换为字符串后，再将对应的字符填入_integer和_demical中
def _divideNum(num):
    '''
    _divideNum() recive an Arabic number, and divide it into
    chars, then fill the _integer and _demical with these chars.
    '''
    if not (isinstance(num, int) or isinstance(num, float)):
        raise TypeError('num should be a int or float')
    if num < 0 or num - 1e9 > 0:
        raise ValueError('num value should be 1~1e9')

    strNum = '{0:015.2f}'.format(num)

    # 填写_integer
    for i in range(3):
        for j in range(4):
            _integer[i][j] = strNum[i*4 + j]
    # 填写_demical
    _demical[0] = strNum[-2]
    _demical[1] = strNum[-1]

# 根据_integer中的字符通过查表的方式转换为中文，并为其添加适当的单位，将
# 转换后的中文合成一个字符串并返回
# (['0','0','0','0'],['3','0','1','0'],['3','0','3','0']) =>
# 零零零零叁仟零壹拾零叁仟零叁拾零
def _makeIntStr():
    ''' Return a unicode string
    _makeIntStr() will translate chars in _integer into Chinese.
    '''
    intStr = u''
    for i in range(3):
        isZero = True
        for j in range(4):
            intStr += _digit_table[_integer[i][j]]
            if _integer[i][j] != '0':  # 如果数字不为零则添加单位
                isZero = False
                intStr += _integer_unit_levels[j]
        if not isZero:  # 如果一个单元(4个数为1单元)全不为零，则添加单位
            intStr += _integer_levels[i]
    return intStr

# 去除整数部分中文字符串中的多余零，将前导零和后缀零删除，将剩余的连续零替换为1个零
# 前导零：以'亿''万'开头的零，和字符串开头的零
# 后缀零：以'亿''万'结尾的零，和字符串结尾的零
def _dealIntZeros(intStr):
    '''
    _dealIntZeros() recive a unicode string, and will remove the
    excess u'零'
    '''
    # 匹配前导'零'和后缀'零'
    pat1 = re.compile(ur'(?<=^)零+|(?<=[亿万])零+|零+(?=[亿万])|零+(?=$)')
    intStr = re.sub(pat1, u'', intStr)
    # 匹配剩余的连续的'零'
    pat2 = re.compile(ur'零{2,}')
    intStr = re.sub(pat2, u'零', intStr)
    return intStr

def _isDemical():
    ''' Reutrn a Boolean
    _isDemical() determines whether the number is a decimal, if it
    is return True, else return False.
    '''
    if _demical[0] == '0' and _demical[1] == '0':
        return False
    else:
        return True

# 根据_demical中的字符通过查表的方式转换为中文，并为其添加适当的单位，将
# 转换后的中文合成一个字符串并返回
# ['0', '1'] => u'壹分'
# ['1', '0'] => u'壹角'
def _makeDemStr():
    ''' Return a unicode string
    _makeDemStr() will translate chars in _demical into Chinese.
    '''
    demStr = u''
    for i in range(2):
        if _demical[i] != '0':
            demStr += _digit_table[_demical[i]] + _demical_levels[i]
    return demStr


if __name__ == '__main__':
    # 整数
    test1 = 0
    test2 = 123
    test3 = 4560789
    test4 = 578090123
    # 小数
    test5 = 0.23
    test6 = 123.789
    test7 = 30476.01
    test8 = 30476.10
    # 非法字符
    test9 = 'abcd'
    test10 = '1234'
    # 非范围内的数字
    test11 = -1
    test12 = 1000000001

    test = (test1, test2, test3, test4, test5, test6,
            test7, test8, test9, test10, test11, test12)
    for case in test:
        try:
            result = convert(case).encode('utf-8')
            print '{0:13!r} : {1!s}'.format(case, result)
        except ValueError, e:
            logging.exception(e)
        except TypeError, e:
            logging.exception(e)

