import parser
import main
import random
import math
import re
import os
import loader
import string
import time
def is_num(s):
  try:
    int(s)
    return True
  except ValueError:
    return False
def num(s):
  try:
    return int(s)
  except ValueError:
    try:
      return float(s)
    except ValueError:
      return 0
class Stack:
  s = []
  #mem holds global variables
  mem = {'true': True, 'false': False, 'pi': math.pi}
  
  code = []
  pntr = 0
  def __init__(self, code, strings, functions):
    self.code = code
    self.pntr = 0
    self.strings = strings
    self.functions = dict(functions)
    while self.pntr < len(self.code):
      for i in self.inst:
        if i.__name__ == self.code[self.pntr]:
          i(self)
          self.info()
          break
      self.pntr += 1
  def push(self, x): self.s.append(x)
  def pop(self):
    if len(self.s) == 0: self.pntr = len(self.code); return 0
    item = self.s.pop()
    if item is None: return 0
    return item
  #misc instructions
  def echo(self): print(self.pop())
  def get_input(self): self.push(input(''))
  def get_time(self): self.push(time.time())
  def info(self): print(str(self.pntr) + ': ' + str(self.s))
  def size(self): self.push(len(self.s))
  def file_call(self): self.pntr += 1; f = loader.fh.files[str(self.code[self.pntr])]; st = Stack(f[0], f[1], f[2])
  def func_call(self): self.pntr += 1; st = Stack(self.functions[str(self.code[self.pntr])], self.strings, self.functions)
  def dup(self): x = self.pop(); self.push(x); self.push(x)
  def swap(self): x = self.pop(); y = self.pop(); self.push(x); self.push(y)
  def drop(self): self.pop()
  def get_func(self): self.pntr += 1; self.push(self.functions[self.code[self.pntr]])
  def number(self):
    try:
      self.pntr += 1
      self.push(self.code[self.pntr])
    except:
      self.push(0)
  def string(self):
    try:
      self.pntr += 1
      self.push(self.strings[int(self.code[self.pntr])])
    except:
      self.push(0)
      print('error')
  def fetch(self): self.pntr += 1; self.push(self.mem[self.code[self.pntr]])
  def store(self): self.pntr += 1; self.mem[self.code[self.pntr]] = self.pop()
  def run(self): p = parser.tokenize(lines); lines = [self.pop()]; st = Stack(p[0], p[1], p[2])
  def src(self): self.push(" ".join(str(self.code)))
  #io instructions
  def write(self):
    path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'scripts', str(self.pop()) + '.txt')
    with open(path, 'w') as out_file:
      out_file.write(str(self.pop()))
  def read(self):
    path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'scripts', str(self.pop()) + '.txt')
    with open(path, 'r') as out_file:
      self.push(out_file.readlines())
  #math instructions
  def increment(self): self.push(num(self.pop()) + 1)
  def decrement(self): self.push(num(self.pop()) - 1)
  def plus(self): self.push(num(self.pop()) + num(self.pop()))
  def minus(self): n = self.pop(); self.push(num(self.pop()) - num(n))
  def star(self): self.push(num(self.pop()) * num(self.pop()))
  def slash(self):
    try:
      n = self.pop()
      self.push(num(self.pop()) // num(n))
    except:
      self.push(0)
  def modulus(self):
    n = self.pop()
    try:
      n = num(self.pop()) % num(n)
    except:
      self.push(0)
  def power(self):
    try:
      n = self.pop()
      self.push(num(self.pop()) ** num(n))
    except:
      self.push(0)

  def orOp(self):
    try:
      self.push(self.pop() | self.pop())
    except:
      self.push(0)
  def negate(self): self.push(-num(self.pop()))
  def square_root(self):
    try:
      self.push(math.sqrt(num(self.pop())))
    except:
      self.push(0)
  def cos(self): self.push(math.cos(num(self.pop())))
  def sin(self): self.push(math.sin(num(self.pop())))
  def tan(self): self.push(math.tan(num(self.pop())))
  #string instructions
  def concat(self): n = self.pop(); self.push(str(self.pop()) + str(n))
  def join(self): n = self.pop(); self.push(str(self.pop()) + ' ' + str(n))
  def join_new_line(self): n = self.pop(); self.push(str(self.pop()) + '\n' + str(n))
  def sub(self): n = self.pop(); m = self.pop(); self.push(re.sub(str(self.pop()), str(m), str(n)))
  def rnd_str(self): self.push(u''.join(random.choice(string.ascii_lowercase) for x in range(num(self.pop()))))
  def starts(self): n = self.pop(); self.push(str(self.pop()).startswith(str(n)))
  def ends(self): n = self.pop(); self.push(str(self.pop()).endswith(str(n)))
  #equality instructions
  def equals(self): self.push(self.pop() == self.pop())
  def notequals(self): self.push(self.pop() != self.pop())
  def less_than(self): self.push(self.pop()) > num(self.pop())
  def greater_than(self): self.push(self.pop()) < num(self.pop())
  def less_or_equal(self): self.push(self.pop()) >= num(self.pop())
  def greater_or_equal(self): self.push(self.pop()) <= num(self.pop())
  def eval_py(self): self.push(eval(self.pop()))
  def and_op(self): self.push(self.pop() and self.pop())
  #loop instructions
  def for_op(self):
    cond = self.pop()
    end = self.pop()
    start = self.pop() 
    loop_index = self.pop()
    self.mem[loop_index] = start
    while int(self.mem[loop_index]) < num(end):
      st = Stack(loader.substitute_tokens(cond), self.strings, self.functions)
      self.mem[loop_index] = num(self.mem[loop_index]) + 1
  def while_op(self):
    cond = self.pop()
    cond_address = self.pop()
    self.mem[cond_address] = True
    while self.mem[cond_address]:
      st = Stack(loader.substitute_tokens(cond), self.strings, self.functions)
  #branch instructions
  def if_else_branch(self):
    false_cond = self.pop()
    true_cond = self.pop()
    cond = self.pop()
    if cond: st = Stack(loader.substitute_tokens(true_cond), self.strings, self.functions)
    else: st = Stack(loader.substitute_tokens(false_cond), self.strings, self.functions)
  def if_branch(self):
    true_cond = self.pop()
    cond = self.pop()
    if cond: st = Stack(loader.substitute_tokens(true_cond), self.strings, self.functions)
  ###############################################################################################################################################
  inst = [file_call, while_op, for_op, if_branch, get_input, info, echo, dup, swap, drop, plus, minus, star, slash, orOp, negate,
          equals, notequals, fetch, store, less_than, greater_than, less_or_equal, greater_or_equal, modulus, power, concat, sub,
          square_root, cos, sin, tan, join, size, increment, decrement, write, join_new_line, rnd_str, starts, ends, get_time,
          read, if_else_branch, run, src, number, string, func_call, eval_py, get_func, and_op]
  ###############################################################################################################################################
