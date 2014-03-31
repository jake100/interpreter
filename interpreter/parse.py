import re
import os
import stack
class FileHandler:
  files = []
  def __init__(self):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    path = os.path.join(__location__, 'file_path' + '.txt')
    fo = open(path, "r")
    line = fo.readline()
    fo.close()
    file_names = re.split(' ', line)
    for name in file_names:
      self.files.append(File(name))
  def get_file(self, s):
    for file in self.files:
      if file.name == s:
        return file.tokens
class File:
  tokens = []
  name = ''
  def __init__(self, name):
    self.name = name
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    path = os.path.join(__location__, name + '.txt')
    fo = open(path, "r")
    lines = fo.readlines()
    fo.close()
    self.tokens = tokenize(lines)
def substitute(token):
  token = re.sub('\n', '', token)
  if token == 'sqrt': token = 'square_root'
  if token == '..': token = 'concat'
  if token == '**': token = 'power'
  if token == '%': token = 'modulus'
  if token == '+': token = 'plus'
  if token == 'if': token = 'if_branch'
  if token == 'for': token = 'for_op'
  if token == 'while': token = 'while_op'
  if token == 'in': token = 'get_input'
  if token == '-': token = 'minus'
  if token == '*': token = 'star'
  if token == '/': token = 'slash'
  if token == '|': token = 'orOp'
  if token == '!': token = 'negate'
  if token == '==': token = 'equals'
  if token == '!=': token = 'notequals'
  if token == '<': token = 'less_than'
  if token == '>': token = 'greater_than'
  if token == '<=': token = 'less_or_equal'
  if token == '>=': token = 'greater_or_equal'
  return token
def handle_store(tokens):
  new_tokens = []
  for token in tokens:
    if token.startswith('='):
      new_tokens.append('store')
      new_tokens.append(token[1:])
    else:
      new_tokens.append(token)
  return new_tokens
def handle_fetch(tokens):
  new_tokens = []
  for token in tokens:
    if token.startswith('$'):
      new_tokens.append('fetch')
      new_tokens.append(token[1:])
    else:
      new_tokens.append(token)
  return new_tokens
def handle_literals(tokens):
  new_tokens = []
  for token in tokens:
    if token.startswith(':'):
      new_tokens.append('literal')
      new_tokens.append(token[1:])
    else:
      new_tokens.append(token)
  return new_tokens
def handle_file_call(tokens):
  new_tokens = []
  for token in tokens:
    if token.startswith('@'):
      new_tokens.append('file_call')
      new_tokens.append(token[1:])
    else:
      new_tokens.append(token)
  return new_tokens
def tokenize(lines):
  tokens = []
  for line in lines:
    line = re.sub(r'#.*$', "", line)
    line = re.split(' ', str(line))
    for i, token in enumerate(line):
      line[i] = substitute(token)
    line = handle_literals(line)
    line = handle_file_call(line)
    line = handle_store(line)
    line = handle_fetch(line)
    for i, token in enumerate(line):
      line[i] = substitute(token)
    tokens += line
  return tokens
