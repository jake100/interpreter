import re
import os
import stack
def substitute(token):
  token = re.sub('\n', '', token)
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
    tokens += line
  return tokens
