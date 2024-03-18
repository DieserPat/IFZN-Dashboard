# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 12:54:10 2023

@author: gross
"""

from pandas import read_csv
import subprocess
import os

cwd = os.getcwd()

files = read_csv("{}\\files.txt".format(cwd), index_col=0, header=0)

p = subprocess.Popen('cmd', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# send a command to the prompt
p.stdin.write('cd {}\n'.format(files.loc["path"][0]).encode())
p.stdin.write('{}\n'.format(files.loc["activate_path"][0]).encode())
p.stdin.write('{}\n'.format(files.loc["activate"][0]).encode())
p.stdin.write('cd {}\n'.format(files.loc["path"][0]).encode())
p.stdin.write('explorer {}\n'.format(files.loc["openDash"][0]).encode())
p.stdin.write('{}\n'.format(files.loc["start"][0]).encode())

p.stdin.close()

output, errors = p.communicate()