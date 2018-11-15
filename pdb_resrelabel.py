#!/usr/bin/env python

"""
Changes a residue label to another.

usage:
    python pdb_resrelabel.py [-ORIGINAL_LABEL] [-NEW_LABEL] <file.pdb>
    
    Residue labels should have a maximum of 3 chars.
    If label contains a ' character, a explicit string should be passed,
        for example:
        -"D5'"
    
example:
    python pdb_resrelabel.py -DA5 -DA 1CTF.pdb
    python pdb_resrelabel.py -"DA'" -DA 1CTF.pdb

Author: {0} ({1})

This program is part of the PDB tools distributed with HADDOCK
or with the HADDOCK tutorial. The utilities in this package
can be used to quickly manipulate PDB files, with the benefit
of 'piping' several different commands. This is a rewrite of old
FORTRAN77 code that was taking too much effort to compile. RIP.
"""
__author__ = "Joao MC Teixeira"
__email__ = "joaomcteixeira@gmail.com"

import os
import sys

USAGE = __doc__.format(__author__, __email__)

def check_input(args):
    
    if not len(args):
        sys.stderr.write(USAGE)
        sys.exit(1)

    elif len(args) < 3:
        # Pipe?
        if not sys.stdin.isatty():
            pdbfh = sys.stdin
        else:
            emsg = 'ERROR!! No data to process!\n'
            sys.stderr.write(emsg)
            sys.stderr.write(USAGE)
            sys.exit(1)
        
    elif len(args) == 3 and sys.stdin.isatty():
        if not os.path.isfile(args[-1]):
            emsg = 'ERROR!! File not found or not readable: \'{}\'\n'
            sys.stderr.write(emsg.format(args[-1]))
            sys.stderr.write(USAGE)
            sys.exit(1)
        
        pdbfh = open(args[-1], 'r')
        
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    if not(args[0].startswith("-")):
        emsg = "ERROR!! '{}' is not an option!\n"
        sys.stderr.write(emsg.format(args[0]))
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    elif not(args[1].startswith("-")):
        emsg = "ERROR!! '{}' is not an option!\n"
        sys.stderr.write(emsg.format(args[1]))
        sys.stderr.write(USAGE)
        sys.exit(1)
        
    old_label = args[0].strip("-")
    new_label = args[1].strip("-")
    
    if len(old_label) > 3 or len(new_label) > 3:
        sys.stderr.write('Residue identifier too long, maximum allowed is 3 chars.\n')
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    return (pdbfh, old_label, new_label)

def _relabels_residue(pdbfh, old_label, new_label):
    
    for line in pdbfh:
        if line.startswith(("ATOM", "HETATM")) \
                and line.split()[3] == old_label:
            
            new_line = line[:17] + "{:^3}".format(new_label) + line[20:]
            
            yield new_line
        
        else:
            yield line

def main():
    # Check Input
    pdbfh, old_label, new_label = check_input(sys.argv[1:])
    
    # Do the job
    new_pdb = _relabels_residue(pdbfh, old_label, new_label)

    try:
        sys.stdout.write(''.join(new_pdb))
        sys.stdout.flush()
    except IOError:
        # This is here to catch Broken Pipes
        # for example to use 'head' or 'tail' without
        # the error message showing up
        pass

    # last line of the script
    # We can close it even if it is sys.stdin
    pdbfh.close()
    sys.exit(0)

if __name__ == '__main__':
    
    main()
