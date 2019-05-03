#!/usr/bin/python
#
# dicodocus - Password dictionary generator
# 
# By Cr1sc0d3r, v0.1 02/05/2019
#

import os
import getopt
import sys
from string import ascii_lowercase


#
# Globals
#

flag_case_substitution = 0
flag_character_substitution = 0
min_length = 8
max_length = 8

pattern_list = []
character_set = ""
character_substitutions = {}
patterns = {}


#
# Functions
#

def showUsage():
    print("dicodocus [-c] [-s] [-l <min_length>] [-L <max_length>] [-p <pattern_1>[,<pattern_2[..,<pattern_N>]]] [-C \"<characters>\"]")
    print("    -c: enables case substitution")
    print("    -s: enables character substitution")
    print("    -l: minimum password length")
    print("    -L: maximum password length")
    print("    -p: comma-separated list of patterns to be included in password")
    print("    -C: characters set to be used apart from patterns")
    print("")
    print("    Note: at least one of pattern list or character set must be defined")


def print_pattern(prefix, pattern):
    if len(pattern) > 0:
        c = pattern[0]
        if c in character_substitutions:
            for n in character_substitutions[c]:
                aux_pattern = list(pattern)
                aux_pattern[0] = n
                new_pattern = ''.join(aux_pattern)
                print_pattern(prefix + new_pattern[0], new_pattern[1:])
        else:
            print_pattern(prefix + pattern[0], pattern[1:])
    else:
        print(prefix)


def build_patterns(original_pattern, prefix, pattern):
    if len(pattern) > 0:
        c = pattern[0]
        if c in character_substitutions:
            for n in character_substitutions[c]:
                aux_pattern = list(pattern)
                aux_pattern[0] = n
                new_pattern = ''.join(aux_pattern)
                build_patterns(original_pattern, prefix + new_pattern[0], new_pattern[1:])
        else:
            build_patterns(original_pattern, prefix + pattern[0], pattern[1:])
    else:
        if original_pattern in patterns:
            patterns[original_pattern].append(prefix)
        else:
            patterns[original_pattern] = [ prefix ]



#
# Main
#

options, remainder = getopt.getopt(sys.argv[1:], 
                                   'csl:L:p:C:', 
                                   ['flag_case_substitution',
                                    'flag_character_substitution',
                                    'min_length=',
                                    'max_length=',
                                    'pattern_list=',
                                    'character_set='
                                    ])

try:
    for opt, arg in options:
        if opt in ("-c"):
            flag_case_substitution = 1
        if opt in ("-s"):
            flag_character_substitution = 1
        elif opt in ("-l"):
            min_length = arg
        elif opt in ("-L"):
            max_length = arg
        elif opt in ("-p"):
            pattern_list = arg.split(",")
        elif opt in ("-c"):
            character_set = arg
except getopt.GetoptError:
    showUsage()
    sys.exit(2)
except:
    showUsage()
    sys.exit(2)

if len(pattern_list) == 0 and character_set == "":
    showUsage()
    sys.exit(3)

if flag_case_substitution == 1:
    for c in ascii_lowercase:
        character_substitutions[c] = [ c, c.upper() ]
        character_substitutions[c.upper()] = [ c.upper(), c ]

if flag_character_substitution == 1:
    character_substitutions['1'] = ['1', '!']

    if flag_case_substitution == 1:
        character_substitutions['a'].append('4')
        character_substitutions['a'].append('@')
        character_substitutions['e'].append('3')
        character_substitutions['i'].append('1')
        character_substitutions['l'].append('1')
        character_substitutions['o'].append('0')
        character_substitutions['s'].append('$')
        character_substitutions['A'].append('4')
        character_substitutions['A'].append('@')
        character_substitutions['E'].append('3')
        character_substitutions['I'].append('1')
        character_substitutions['L'].append('1')
        character_substitutions['O'].append('0')
        character_substitutions['S'].append('$')
    else:
        character_substitutions['a'] = ['a', '4', '@']
        character_substitutions['e'] = ['e', '3']
        character_substitutions['i'] = ['i', '1']
        character_substitutions['l'] = ['l', '1']
        character_substitutions['o'] = ['o', '0']
        character_substitutions['s'] = ['s', '$']
        character_substitutions['A'] = ['A', '4', '@']
        character_substitutions['E'] = ['E', '3']
        character_substitutions['I'] = ['I', '1']
        character_substitutions['L'] = ['L', '1']
        character_substitutions['O'] = ['O', '0']
        character_substitutions['S'] = ['S', '$']

if len(pattern_list) > 0:
    for pattern in pattern_list:
        build_patterns(pattern, "", pattern)
print(patterns)
