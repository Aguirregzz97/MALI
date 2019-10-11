import glob, os, io, sys
from parser import *

def parse(file):
  text_trap = io.StringIO()
  sys.stdout = text_trap
  parser.parse(file.read())
  sys.stdout = sys.__stdout__ 

if __name__ == '__main__':
  os.chdir('testfiles')
  
  for file_name in glob.glob('correct/*_test.m'):
    file = open(file_name, 'r', newline='\n')
    try:
      parseString(file.read())
      print(f'Successfull {file_name}.')
    except SyntaxError:
      print(f'Fail        {file_name}.')

  for file_name in glob.glob('incorrect/*_test.m'):
    file = open(file_name, 'r', newline='\n')
    try:
      parseString(file.read())
      print(f'Fail        {file_name}.')
    except SyntaxError:
      print(f'Successfull {file_name}.')
