import sys
from pyedit import main

filename = None
if len(sys.argv) > 1:
    filename = sys.argv[1]

main.run(filename)
