"""
Compile module in python library pid.

Created on 17.11.2018

@author: Ruslan Dolovanyuk

example running:
    python compile.py build_ext --inplace

"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
               Extension("board", ["board.py"]),
               Extension("cell", ["cell.py"]),
               Extension("constants", ["constants.py"]),
               Extension("game", ["game.py"]),
               Extension("player", ["player.py"]),
               Extension("speech", ["speech.py"])
              ]

setup(
      name='main',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
)
