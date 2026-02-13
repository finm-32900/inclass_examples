"""
Name shadowing: a local file can shadow an installed package.

If you create a file called numpy.py in your working directory,
`import numpy` will import YOUR file instead of the real numpy.
This is a common source of confusing errors.

Run this script and look at sys.path to understand why.
"""

import sys

print("sys.path (where Python looks for modules, in order):")
for p in sys.path:
    print(f"  {p}")

print()

# This imports the LOCAL numpy.py, not the real numpy!
import numpy

numpy.hello()
