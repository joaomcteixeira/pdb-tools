#!/usr/bin/env python

"""
Concatenates PDB files ordering chains according to input.

Residue names are maintained and HETATMS are written at the end
keeping information on the chain they belong.

usage: python pdb_concat.py <pdb files> 
example:
    python pdb_concat.py 1.pdb 2.pdb 3.pdb > new.pdb
    python pdb_concat *.pdb > new.pdb

Author: {0} ({1})

This program is part of the PDB tools distributed with HADDOCK
or with the HADDOCK tutorial. The utilities in this package
can be used to quickly manipulate PDB files, with the benefit
of 'piping' several different commands. This is a rewrite of old
FORTRAN77 code that was taking too much effort to compile. RIP.
"""

import os
import sys
import re
import string
import itertools as it

__author__ = "Joao M.C. Teixeira"
__email__ = "joaomcteixeira@gmail.com"

USAGE = __doc__.format(__author__, __email__)

def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    """
    
    if not len(args):
        sys.stderr.write(USAGE)
        sys.exit(1)
    elif len(args) >= 1:
        for file_name in args:
            if not os.path.isfile(file_name):
                sys.stderr.write('File not found: ' + file_name + '\n')
                sys.stderr.write(USAGE)
                sys.exit(1)
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)
    
    return args

def _concatenate_pdbs(pdbfnlh):
    """
    Concatenates PDBs in a single PDB file.
    
    PDBs with multiple chains are also read.
    
    Parameters:
        - pdbfnlh (list of str): list of file names to process.
    """
    # to assign chain names
    upercase = string.ascii_uppercase
    # cycles chain letters
    chain_counter = it.cycle(upercase)
    # reads only ATOM and HETATOM lines
    coord_re = re.compile('^(ATOM|HETATM)')
    # initiates atom counter
    atom_num=0
    # initiates HETATM list to store HETATM strings
    hetatms = list()
    
    for file_name in pdbfnlh:
        
        pdb_file = open(file_name, 'rU')
        curr_chain = next(chain_counter)
        line_counter = 0
        
        for line in pdb_file:
            
            # initiates ter_line, necessary for multiple chain PDBs
            ter_line = ""
            
            if coord_re.match(line):
                
                line_counter += 1
                line_chain = line[21]
                
                # if chain changes within the same file...
                if line_counter > 1 and line_chain != prev_chain:
                    atom_num += 1
                    # ends the previous chain
                    ter_line  = \
                        "TER    " \
                        + "{:>5}".format(atom_num) \
                        + 5*" " \
                        + last_line[17:26] \
                        + "\n"
                    curr_chain = next(chain_counter)
                
                # ATOM and HETATM need to be separated because HETATMs
                # go at the end of file
                if line.startswith('ATOM'):
                    
                    atom_num += 1
                    # defines the new line
                    new_line = \
                        line[:7] \
                        + "{:>5}".format(atom_num) \
                        + line[12:21] \
                        + curr_chain \
                        + line[22:]
                    # registers the name of previous chain
                    prev_chain = line_chain
                    last_line = new_line
                    yield ter_line + new_line
                
                elif line.startswith('HETATM'):
                    # defines the new line
                    # here atom number is not changed
                    # it will be changed after the for cycle
                    new_line = \
                        line[:12] \
                        + line[12:21] \
                        + curr_chain \
                        + line[22:]
                    
                    # creates a list of hetatms strings
                    hetatms.append(new_line)
                    prev_chain = line_chain
        
        else:
            # when the file ends, ends the chain
            atom_num += 1
            ter_line  = \
                "TER    " \
                + "{:>5}".format(atom_num) \
                + 5*" " \
                + last_line[17:26] \
                + "\n"
            pdb_file.close()
            yield ter_line
    
    else:
        # initiates HETATM string block
        hetatm_block = ""
        
        for hetatm_line in hetatms:
        
            atom_num += 1
            hetatm_line = "{}{}{}".format(
                hetatm_line[:7],
                "{:>5}".format(atom_num),
                hetatm_line[12:]
                )
            hetatm_block += hetatm_line
        
        else:
            hetatm_block += "END\n"
        
        yield hetatm_block

if __name__ == '__main__':

    # Check Input
    # PDB file list handler
    pdbfnlh = check_input(sys.argv[1:])

    # Do the job
    new_pdb = _concatenate_pdbs(pdbfnlh)

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
    sys.exit(0)

