#! /usr/bin/env python2.7
import re
import sys

class HackAssembler():
    def __init__(self, filename):
        self.symtable = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 'R0':0, 'R1':1,
                        'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8,
                        'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14,
                        'R15':15, 'SCREEN':16384, 'KBD':24576}
        self.nextaddr = 16
        self.lablesslines = []
        self.hackcode = []
        self.readlabel(filename)
        self.translate()

    def readlabel(self, filename):
        f = open(filename, 'r')
        lnum = 0
        for l in f:
            l = re.sub('\s', '', l.split("//", 1)[0])
            if l != '':
                if l[0] == '(' and l[-1] == ')':
                    label = l[1:-1]
                    self.symtable[label] = lnum
                else:
                    self.lablesslines.append(l)
                    lnum += 1
        f.close()

    def translate(self):
        for l in self.lablesslines:
            if l[0] == '@':
                self.hackcode.append(self.parseAexp(l))
            else:
                self.hackcode.append(self.parseCexp(l))
        # self.symtable = {}

    def parseAexp(self, l):
        if l[1:].isdigit():
            dec = int(l[1:])
        else:
            var = l[1:]
            if var in self.symtable.keys():
                dec = self.symtable[var]
            elif not var[0].isdigit() and re.match('^[\w.$:]*$', var):
                dec = self.nextaddr
                self.nextaddr += 1
                self.symtable[var] = dec
            else:
                raise Exception("Illegal var name: " + var)
        return format(dec, '016b')

    def parseCexp(self, l):
        dest, comp, jump = self.parse(l)
        return "111" + self.ccode(comp) + self.dcode(dest) + self.jcode(jump)

    def parse(self, l):
        tokens = l.split('=')
        if len(tokens) == 2:
            dest = tokens[0]
            l = tokens[1]
        else:
            dest = None
        tokens = l.split(';')
        comp = tokens[0]
        if len(tokens) == 2:
            jump = tokens[1]
        else:
            jump = None
        return dest, comp, jump

    def dcode(self, dest):
        return '000' if dest is None else (('1' if 'A' in dest else '0') +
            ('1' if 'D' in dest else '0') + ('1' if 'M' in dest else '0'))

    def jcode(self, jump):
        if jump is None:
            return '000'
        if jump == "JNE":
            jump = "JLG"
        if jump == "JMP":
            jump = "LEG"
        return ('1' if 'L' in jump else '0') + ('1' if 'E' in jump else '0') + ('1' if 'G' in jump else '0')

    def ccode(self, comp):
        if comp == '0':
            return '0101010'
        if comp == '1':
            return '0111111'
        if comp == '-1':
            return '0111010'
        if comp == 'D':
            return '0001100'
        if comp == 'A':
            return '0110000'
        if comp == '!D':
            return '0001101'
        if comp == '!A':
            return '0110001'
        if comp == '-D':
            return '0001111'
        if comp == '-A':
            return '0110011'
        if comp == 'D+1' or comp == '1+D':
            return '0011111'
        if comp == 'A+1' or comp == '1+A':
            return '0110111'
        if comp == 'D-1':
            return '0001110'
        if comp == 'A-1':
            return '0110010'
        if comp == 'D+A' or comp == 'A+D':
            return '0000010'
        if comp == 'D-A':
            return '0010011'
        if comp == 'A-D':
            return '0000111'
        if comp == 'D&A' or comp == 'A&D':
            return '0000000'
        if comp == 'D|A' or comp == 'A|D':
            return '0010101'
        if comp == 'M':
            return '1110000'
        if comp == '!M':
            return '1110001'
        if comp == '-M':
            return '1110011'
        if comp == 'M+1' or comp == '1+M':
            return '1110111'
        if comp == 'M-1':
            return '1110010'
        if comp == 'D+M' or comp == 'M+D':
            return '1000010'
        if comp == 'D-M':
            return '1010011'
        if comp == 'M-D':
            return '1000111'
        if comp == 'D&M' or comp == 'M&D':
            return '1000000'
        if comp == 'D|M' or comp == 'M|D':
            return '1010101'
        raise Exception("Illegal comp mnemoic: " + comp)

    def writefile(self, filename):
        f = open(filename, 'w')
        for bincode in self.hackcode:
            f.write(bincode + '\n')
        f.close()

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
       print "Usage: ./HackAssembler.py infile outfile"
       exit

    infile = args[1]
    outfile = args[2]

    asm = HackAssembler(infile)
    asm.writefile(outfile)
