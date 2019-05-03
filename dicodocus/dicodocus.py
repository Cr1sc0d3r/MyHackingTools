#!/usr/bin/python
#
# dicodocus - Password dictionary generator
# 
# By Cr1sc0d3r, v0.1 03/05/2019
#

import os
import getopt
import itertools
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
character_substitutions = {}
patterns = {}
pattern_permutations = []
combined_patterns = []
passwords = []


#
# Functions
#

def showUsage():
    print("dicodocus [-c] [-s] [-l <min_length>] [-L <max_length>] -p <pattern_1>[,<pattern_2[..,<pattern_N>]]")
    print("    -c: enables case substitution")
    print("    -s: enables character substitution")
    print("    -l: minimum password length (default = 8, must be > 1 and <= maximum password length)")
    print("    -L: maximum password length (default = 8, must be >= minimum password length and <= 24)")
    print("    -p: comma-separated list of patterns to be included in password")
    print("")


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
                                    'pattern_list='
                                    ])

try:
    for opt, arg in options:
        if opt in ("-c"):
            flag_case_substitution = 1
        if opt in ("-s"):
            flag_character_substitution = 1
        elif opt in ("-l"):
            min_length = int(arg)
        elif opt in ("-L"):
            max_length = int(arg)
        elif opt in ("-p"):
            pattern_list = arg.split(",")
        elif opt in ("-c"):
            character_set = arg
except getopt.GetoptError:
    showUsage()
    sys.exit(2)
except:
    showUsage()
    sys.exit(3)

if len(pattern_list) == 0:
    showUsage()
    sys.exit(4)

if (min_length < 4) or (min_length > max_length):
    showUsage()
    print(min_length)
    print(max_length)
    sys.exit(5)

if max_length > 24 or max_length < min_length:
    showUsage()
    sys.exit(6)

if flag_case_substitution == 1:
    for c in ascii_lowercase:
        character_substitutions[c] = [ c, c.upper() ]
        character_substitutions[c.upper()] = [ c.upper(), c ]

if flag_character_substitution == 1:
    character_substitutions['1'] = ['1', '!']
    character_substitutions['^'] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

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


for pattern in pattern_list:
    build_patterns(pattern, "", pattern)

for R in range(0, len(pattern_list) + 1):
    for permutation in itertools.permutations(pattern_list, R):
        if len(permutation) > 0:
            pattern_permutations.append(permutation)

for permutation in pattern_permutations:
    compound_list = []
    for original_pattern in permutation:
        compound_list.append(patterns[original_pattern])
    
    res = list(itertools.product(*compound_list)) 
    for r in res:
        combined_pattern = ""
        for e in r:
            combined_pattern = combined_pattern + e
        combined_patterns.append(combined_pattern)

L = min_length
while L <= max_length:
    for pattern in combined_patterns:
        if len(pattern) < L:
            continue
        elif len(pattern) > L:
            reduced_pattern = pattern[:L-1]
        else:
            reduced_pattern = pattern
        if reduced_pattern not in passwords:
            passwords.append(reduced_pattern)
    L = L + 1

for password in passwords:
    print(password)

