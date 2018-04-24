'''
*******************************************************************************
Module DOCSTRING: Defines basic stuff used in general programming
'''
import importlib
import pip
import pip._internal

# Import Reload shortcut
rl = importlib.reload
# Pip Install shortcut
pipin = lambda pkg: pip._internal.main(['install', pkg, '--upgrade'])
