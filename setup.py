import pathlib
from setuptools import setup, find_packages
from src.__main__ import main
from typing import List

def _get_reqs() -> List[str]:
    return pathlib.Path('requirements.txt').read_text().splitlines()

setup(
    name='PAD Auto Solver',
    version='1.0.0',
    url='https://github.com/senkevinli/PAD-Auto-Solver',
    author='Kevin Li',
    description='Command Line Interface tool for solving Puzzles and Dragons',
    packages=find_packages(),
    install_requires=_get_reqs(),
    entry_points='''
        [console_scripts]
        pad_solver=src.__main__:main
    '''
)