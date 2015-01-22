#!/bin/python
# Copyright (c) 2014-2015 Rasmus S. Sorensen, rasmusscholer@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# pylint: disable=C0103,W0142

"""
Usage:
    > python rows_to_table.py rowsfile.txt > tablefile.txt
"""
import sys
import os
import argparse
from itertools import zip_longest

def make_parser():
    """ Generate main parser. """
    parser = argparse.ArgumentParser()
    parser.description = "Transform lines in a file to a table structure."
    parser.add_argument('files', nargs='*')
    parser.add_argument('--stdin', '-', action='store_true')
    parser.add_argument('--nrows', '-r', type=int, default=2)
    parser.add_argument('--sep', default='\t')
    parser.add_argument('--outfnfmt', help="Print to file rather than std out. E.g. {fnroot}-out.txt")
    parser.add_argument('--no-escape', dest='escape', action='store_false', help="Do not escape sep input argument.")
    parser.add_argument('--escape', dest='escape', action='store_true')
    return parser

def transform_file(fdin, outputfn=None, sep=',', nrows=2):
    """ Transform lines in fdin to a table. """
    fg = (line.strip() for line in fdin) # strip lines or just remove line terminator?
    if outputfn:
        with open(outputfn, 'w') as fout:
            #print("Writing to file:", outputfn)
            fout.write("\n".join(sep.join(tup) for tup in zip_longest(*[fg]*nrows, fillvalue="")))
    else:
        print("\n".join(sep.join(tup) for tup in zip_longest(*[fg]*nrows, fillvalue="")))



def main(argv=None):
    """ Main function. Invoked if run from command line. """
    parser = make_parser()
    argns = parser.parse_args(argv)
    if argns.sep and '\\' in argns.sep and argns.escape:
        # in case the user tried to set --sep "\t" (which is escaped into "\\t"):
        argns.sep = bytes(argns.sep, 'utf-8').decode('unicode_escape')
    if not argns.files and argns.stdin:
        transform_file(sys.stdin, sep=argns.sep, nrows=argns.nrows)
    for finpath in argns.files:
        with open(finpath) as fd:
            if argns.outfnfmt:
                basename = os.path.basename(finpath)
                fnroot, ext = os.path.splitext(basename)
                dirname = os.path.dirname(os.path.abspath(finpath))
                outputfn = argns.outfnfmt.format(fnroot=fnroot, ext=ext, basename=basename, dirname=dirname)
            else:
                outputfn = None
            transform_file(fd, outputfn=outputfn, sep=argns.sep, nrows=argns.nrows)


if __name__ == '__main__':
    main()
