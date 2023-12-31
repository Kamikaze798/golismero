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


from .lang_EU import Num2Word_EU

#//TODO: error messages in French
#//TODO: ords
class Num2Word_FR(Num2Word_EU):
    def setup(self):
        self.negword = "moins "
        self.pointword = "virgule"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.errmsg_toobig = "Number is too large to convert to words."
        self.exclude_title = ["et", "virgule", "moins"]
        self.mid_numwords = [(1000, "mille"), (100, "cent"),
                             (80, "quatre-vingts"), (60, "soixante"),
                             (50, "cinquante"), (40, "quarante"),
                             (30, "trente")]
        self.low_numwords = ["vingt", "dix-neuf", "dix-huit", "dix-sept",
                             "seize", "quinze", "quatorze", "treize", "douze",
                             "onze", "dix", "neuf", "huit", "sept", "six",
                             "cinq", "quatre", "trois", "deux", "un", "zéro"]


    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum < 1000000:
                return next
        else:
            if (not (cnum - 80)%100 or not cnum%100) and ctext[-1] == "s":
                ctext = ctext[:-1]
            if (cnum<1000 and nnum != 1000 and ntext[-1] != "s"
            and not nnum%100):
                ntext += "s"

        if nnum < cnum < 100:
            if nnum % 10 == 1 and cnum != 80:
                return ("%s et %s"%(ctext, ntext), cnum + nnum)
            return ("%s-%s"%(ctext, ntext), cnum + nnum)
        elif nnum > cnum:
            return ("%s %s"%(ctext, ntext), cnum * nnum)
        return ("%s %s"%(ctext, ntext), cnum + nnum)


    # Is this right for such things as 1001 - "mille unième" instead of
    # "mille premier"??  "millième"??

    def to_ordinal(self,value):
        self.verify_ordinal(value)
        if value == 1:
            return "premier"
        word = self.to_cardinal(value)
        if word[-1] == "e":
            word = word[:-1]
        return word + "ième"


    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        out = str(value)
        out +=  {"1" : "er" }.get(out[-1], "me")
        return out

    def to_currency(self, val, longval=True, old=False):
        hightxt = "Euro/s"
        if old:
            hightxt="franc/s"
        return self.to_splitnum(val, hightxt=hightxt, lowtxt="centime/s",
                                jointxt="et",longval=longval)

n2w = Num2Word_FR()
to_card = n2w.to_cardinal
to_ord = n2w.to_ordinal
to_ordnum = n2w.to_ordinal_num

def main():
    for val in [ 1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1500, 1701, 3000,
             8280, 8291, 150000, 500000, 1000000, 2000000, 2000001,
             -21212121211221211111, -2.121212, -1.0000100]:
        n2w.test(val)

    n2w.test(1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730)
    print(n2w.to_currency(112121))
    print(n2w.to_year(1996))


if __name__ == "__main__":
    main()
