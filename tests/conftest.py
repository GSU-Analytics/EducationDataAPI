# conftest.py
import sys
from os.path import abspath, dirname, join

# This assumes that the conftest.py file is located in the 'tests' directory
current_dir = dirname(abspath(__file__))
project_root = join(current_dir, '..') 
sys.path.insert(0, project_root)
