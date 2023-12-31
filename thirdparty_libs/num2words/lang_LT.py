# -*- encoding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA
"""
>>> from textwrap import fill

>>> ' '.join([str(i) for i in splitby3('1')])
'1'
>>> ' '.join([str(i) for i in splitby3('1123')])
'1 123'
>>> ' '.join([str(i) for i in splitby3('1234567890')])
'1 234 567 890'

>>> print(' '.join([n2w(i) for i in range(10)]))
nulis vienas du trys keturi penki šeši septyni aštuoni devyni

>>> print(fill(' '.join([n2w(i+10) for i in range(10)])))
dešimt vienuolika dvylika trylika keturiolika penkiolika šešiolika
septyniolika aštuoniolika devyniolika

>>> print(fill(' '.join([n2w(i*10) for i in range(10)])))
nulis dešimt dvidešimt trisdešimt keturiasdešimt penkiasdešimt
šešiasdešimt septyniasdešimt aštuoniasdešimt devyniasdešimt

>>> print(n2w(100))
šimtas
>>> print(n2w(101))
šimtas vienas
>>> print(n2w(110))
šimtas dešimt
>>> print(n2w(115))
šimtas penkiolika
>>> print(n2w(123))
šimtas dvidešimt trys
>>> print(n2w(1000))
tūkstantis
>>> print(n2w(1001))
tūkstantis vienas
>>> print(n2w(2012))
du tūkstančiai dvylika

>>> print(fill(n2w(1234567890)))
milijardas du šimtai trisdešimt keturi milijonai penki šimtai
šešiasdešimt septyni tūkstančiai aštuoni šimtai devyniasdešimt

>>> print(fill(n2w(215461407892039002157189883901676)))
du šimtai penkiolika naintilijonų keturi šimtai šešiasdešimt vienas
oktilijonas keturi šimtai septyni septilijonai aštuoni šimtai
devyniasdešimt du sikstilijonai trisdešimt devyni kvintilijonai du
kvadrilijonai šimtas penkiasdešimt septyni trilijonai šimtas
aštuoniasdešimt devyni milijardai aštuoni šimtai aštuoniasdešimt trys
milijonai devyni šimtai vienas tūkstantis šeši šimtai septyniasdešimt
šeši

>>> print(fill(n2w(719094234693663034822824384220291)))
septyni šimtai devyniolika naintilijonų devyniasdešimt keturi
oktilijonai du šimtai trisdešimt keturi septilijonai šeši šimtai
devyniasdešimt trys sikstilijonai šeši šimtai šešiasdešimt trys
kvintilijonai trisdešimt keturi kvadrilijonai aštuoni šimtai dvidešimt
du trilijonai aštuoni šimtai dvidešimt keturi milijardai trys šimtai
aštuoniasdešimt keturi milijonai du šimtai dvidešimt tūkstančių du
šimtai devyniasdešimt vienas

# TODO: fix this:
>>> print(fill(n2w(1000000000000000000000000000000)))
naintilijonas

>>> print(to_currency(1.0, 'LTL'))
vienas litas, nulis centų

>>> print(to_currency(1234.56, 'LTL'))
tūkstantis du šimtai trisdešimt keturi litai, penkiasdešimt šeši centai

>>> print(to_currency(-1251985, cents = False))
minus dvylika tūkstančių penki šimtai devyniolika litų, 85 centai
"""


ZERO = ('nulis',)

ONES = {
    1: ('vienas',),
    2: ('du',),
    3: ('trys',),
    4: ('keturi',),
    5: ('penki',),
    6: ('šeši',),
    7: ('septyni',),
    8: ('aštuoni',),
    9: ('devyni',),
}

TENS = {
    0: ('dešimt',),
    1: ('vienuolika',),
    2: ('dvylika',),
    3: ('trylika',),
    4: ('keturiolika',),
    5: ('penkiolika',),
    6: ('šešiolika',),
    7: ('septyniolika',),
    8: ('aštuoniolika',),
    9: ('devyniolika',),
}

TWENTIES = {
    2: ('dvidešimt',),
    3: ('trisdešimt',),
    4: ('keturiasdešimt',),
    5: ('penkiasdešimt',),
    6: ('šešiasdešimt',),
    7: ('septyniasdešimt',),
    8: ('aštuoniasdešimt',),
    9: ('devyniasdešimt',),
}

HUNDRED = ('šimtas', 'šimtai')

THOUSANDS = {
    1: ('tūkstantis', 'tūkstančiai', 'tūkstančių'),
    2: ('milijonas', 'milijonai', 'milijonų'),
    3: ('milijardas', 'milijardai', 'milijardų'),
    4: ('trilijonas', 'trilijonai', 'trilijonų'),
    5: ('kvadrilijonas', 'kvadrilijonai', 'kvadrilijonų'),
    6: ('kvintilijonas', 'kvintilijonai', 'kvintilijonų'),
    7: ('sikstilijonas', 'sikstilijonai', 'sikstilijonų'),
    8: ('septilijonas', 'septilijonai', 'septilijonų'),
    9: ('oktilijonas', 'oktilijonai', 'oktilijonų'),
    10: ('naintilijonas', 'naintilijonai', 'naintilijonų'),
}

CURRENCIES = {
    'LTL': (('litas', 'litai', 'litų'), ('centas', 'centai', 'centų')),
}

def splitby3(n):
    length = len(n)
    if length > 3:
        start = length % 3
        if start > 0:
            yield int(n[:start])
        for i in range(start, length, 3):
            yield int(n[i:i+3])
    else:
        yield int(n)


def get_digits(n):
    return [int(x) for x in reversed(list(('%03d' % n)[-3:]))]

def pluralize(n, forms):
    n1, n2, n3 = get_digits(n)
    if n2 == 1 or n1 == 0 or n == 0:
        return forms[2]
    elif n1 == 1:
        return forms[0]
    else:
        return forms[1]

def int2word(n):
    if n == 0:
        return ZERO[0]

    words = []
    chunks = list(splitby3(str(n)))
    i = len(chunks)
    for x in chunks:
        i -= 1
        n1, n2, n3 = get_digits(x)

        if n3 > 0:
            if n3 > 1:
                words.append(ONES[n3][0])
                words.append(HUNDRED[1])
            else:
                words.append(HUNDRED[0])

        if n2 > 1:
            words.append(TWENTIES[n2][0])

        if n2 == 1:
            words.append(TENS[n1][0])
        elif n1 > 0 and not (i > 0 and x == 1):
            words.append(ONES[n1][0])

        if i > 0:
            words.append(pluralize(x, THOUSANDS[i]))

    return ' '.join(words)

def n2w(n):
    n = str(n).replace(',', '.')
    if '.' in n:
        left, right = n.split('.')
        return '%s kablelis %s' % (int2word(int(left)), int2word(int(right)))
    else:
        return int2word(int(n))

def to_currency(n, currency='LTL', cents = True):
    if type(n) == int:
        if n < 0:
            minus = True
        else:
            minus = False

        n = abs(n)
        left = n / 100
        right = n % 100
    else:
        n = str(n).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
        else:
            left, right = n, 0
        left, right = int(left), int(right)
        minus = False
    cr1, cr2 = CURRENCIES[currency]

    if minus:
        minus_str = "minus "
    else:
        minus_str = ""

    if cents:
        cents_str = int2word(right)
    else:
        cents_str = "%02d" % right

    return '%s%s %s, %s %s' % (minus_str, int2word(left), pluralize(left, cr1),
                              cents_str, pluralize(right, cr2))

class Num2Word_LT(object):
    def to_cardinal(self, number):
        return n2w(number)

    def to_ordinal(self, number):
        raise NotImplementedError()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
