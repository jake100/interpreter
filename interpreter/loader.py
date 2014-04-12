import os
import re
def substitute_tokens(orig_tokens):
  tokens = []
  for i, token in enumerate(orig_tokens):
    if i == 0 or orig_tokens[i-1] != 'string':
        try:
          int(token)
          tokens.append('number')
        except ValueError:
          try:
            float(token)
            tokens.append('number')
          except ValueError: pass
    if token.startswith('='):
      tokens.append('store')
      token = token[1:]
    if token.startswith('$'):
      tokens.append('fetch')
      token = token[1:]
    if token.startswith('->'):
      tokens.append('func_call')
      token = token[2:]
    if token.startswith('@'):
      tokens.append('file_call')
      token = token[1:]
    if token.startswith('&'):
      tokens.append('get_func')
      token = token[1:]
    if token == 'and': token = 'and_op'
    if token == 'time': token = 'get_time'
    if token == '++': token = 'increment'
    if token == '--': token = 'decrement'
    if token == '...': token = 'join_new_line'
    if token == '..': token = 'join'
    if token == '.': token = 'concat'
    if token == 'sqrt': token = 'square_root'
    if token == '**': token = 'power'
    if token == '%': token = 'modulus'
    if token == '+': token = 'plus'
    if token == 'if_else': token = 'if_else_branch'
    if token == 'if': token = 'if_branch'
    if token == 'for': token = 'for_op'
    if token == 'while': token = 'while_op'
    if token == 'input': token = 'get_input'
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
    tokens.append(token)
  return tokens
def tokenize(lines):
  tokens = []
  strings = []
  functions = {}
  new_lines = ''
  for i, line in enumerate(lines):
    line = re.sub(r'#.*$', "", line)
    line = re.sub('\n', ' ', line)
    line = re.sub('\t', '', line)
    line = re.split('\'', line)
    for j, c in enumerate(line):
      if j % 2 == 0:
        new_lines += c
      else:
        strings.append(c)
        new_lines += 'string ' + str(len(strings) - 1)
  new_lines = re.split(';', new_lines)
  for i, token in enumerate(new_lines):
    if token != '' and token != ' ' and token != '\t':
      token = token.strip()
      token = re.split(' ', token)
      if i % 2 != 0:
        functions[token[0]] = token[1:]
      else:
        tokens += token
  tokens = substitute_tokens(tokens)
  return [tokens, strings, functions]
class FileHandler:
  def __init__(self):
    self.files = {}
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'scripts'))
    for root, dirs, all_files in os.walk(os.path.dirname(__file__)):
      for file in all_files:
        if file.endswith('.txt'):
          self.files[os.path.splitext(file)[0]] = File(os.path.splitext(file)[0])
class File:
  tokens = []
  strings = []
  def __init__(self, name):
    self.name = name
    self.tokens = []
    self.strings = []
    self.functions = []
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'scripts'))
    path = os.path.join(__location__, name + '.txt')
    fo = open(path, "r")
    lines = fo.readlines()
    fo.close()
    p = tokenize(lines)
    self.tokens = p[0]
    self.strings = p[1]
    self.functions = p[2]
fh = FileHandler()
