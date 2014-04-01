import parse
import main
import random
import math
import re
import os
import file_handler
import string
import time
def num(s):
  try:
      return int(s)
  except ValueError:
      return float(s)
class Stack:
  s = []
  mem = {'true': True, 'false': False, 'pi': math.pi, 's': ' ', ':': 'literal', '@': 'file_call', '$': 'fetch', '=': 'store'}
  code = []
  pntr = 0
  def __init__(self, code):
    self.code = code
    self.pntr = 0
    while self.pntr < len(self.code):
      for i in self.inst:
        if i.__name__ == self.code[self.pntr]:
          i(self)
          self.info()
          break
      self.pntr += 1
  def push(self, x): self.s.append(x)
  def pop(self): return self.s.pop()
  #misc instructions
  def echo(self): print(self.pop())
  def get_input(self): self.push(input(''))
  def get_time(self): self.push(time.time())
  def info(self): print(str(self.pntr) + ': ' + str(self.s))
  def size(self): self.push(len(self.s))
  def file_call(self): self.pntr += 1; st = Stack(fh.get_file(str(self.code[self.pntr])))
  def dup(self): x = pop(); self.push(x); self.push(x)
  def swap(self): x = self.pop(); y = self.pop(); self.push(x); self.push(y)
  def drop(self): self.pop()
  def literal(self): self.pntr += 1; self.push(self.code[self.pntr])
  def fetch(self): self.pntr += 1; self.push(self.mem[self.code[self.pntr]])
  def store(self): self.pntr += 1; self.mem[self.code[self.pntr]] = self.pop() 
  #io instructions
  def write(self):
    path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'scripts', str(self.pop() + '.txt'))
    with open(path, 'a+') as out_file:
      out_file.write(str(self.pop()))
  def read(self):
    path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'scripts', str(self.pop() + '.txt'))
    with open(path, 'r') as out_file:
      self.push(out_file.readlines())
  #math instructions
  def increment(self): self.push(int(self.pop()) + 1)
  def decrement(self): self.push(int(self.pop()) - 1)
  def plus(self): self.push(num(self.pop()) + num(self.pop()))
  def minus(self): n = self.pop(); self.push(num(self.pop()) - num(n))
  def star(self): self.push(num(self.pop()) * num(self.pop()))
  def slash(self): n = self.pop(); self.push(num(self.pop()) // num(n))
  def modulus(self): n = self.pop(); self.push(num(self.pop()) % num(n))
  def power(self): n = self.pop(); self.push(num(self.pop()) ** num(n))
  def orOp(self): self.push(self.pop() | self.pop())
  def negate(self): self.push(-num(self.pop()))
  def square_root(self): self.push(math.sqrt(num(self.pop())))
  def cos(self): self.push(math.cos(num(self.pop())))
  def sin(self): self.push(math.sin(num(self.pop())))
  def tan(self): self.push(math.tan(num(self.pop())))
  def dist(self): y2 = int(self.pop()); x2 = int(self.pop()); y1 = int(self.pop()); x1 = int(self.pop()); self.push(math.hypot(x2 - x1, y2 - y1))
  def rnd(self): end = self.pop(); self.push(random.randint(int(self.pop()), int(end)))
  #string instructions
  def concat(self): n = self.pop(); self.push(str(self.pop()) + str(n))
  def join(self): n = self.pop(); self.push(str(self.pop()) + ' ' + str(n))
  def join_new_line(self): n = self.pop(); self.push(str(self.pop()) + '\n' + str(n))
  def sub(self): n = self.pop(); m = self.pop(); self.push(re.sub(str(self.pop()), str(m), str(n)))
  def rnd_str(self): self.push(u''.join(random.choice(string.ascii_lowercase) for x in range(int(self.pop()))))
  def starts(self): n = self.pop(); self.push(str(self.pop()).startswith(str(n)))
  def ends(self): n = self.pop(); self.push(str(self.pop()).endswith(str(n)))
  #equality instructions
  def equals(self): self.push(self.pop() == self.pop())
  def notequals(self): self.push(self.pop() != self.pop())
  def less_than(self): self.push(self.pop()) > num(self.pop())
  def greater_than(self): self.push(self.pop()) < num(self.pop())
  def less_or_equal(self): self.push(self.pop()) >= num(self.pop())
  def greater_or_equal(self): self.push(self.pop()) <= num(self.pop())
  #loop instructions
  def repeat(self):
    func = self.pop()
    times = self.pop()
    for i in self.inst:
      if i.__name__ == parse.substitute(str(func)):
        for t in range(int(times)):
          i(self)
          self.info()
        return
  def for_op(self):
    address = self.pop()
    end = self.pop()
    start = self.pop() 
    loop_index = self.pop()
    self.mem[loop_index] = start
    while int(self.mem[loop_index]) < int(end):
      st = Stack(fh.get_file(str(address)))
      self.mem[loop_index] = int(self.mem[loop_index]) + 1
  def while_op(self):
    address = self.pop()
    cond_address = self.pop()
    self.mem[cond_address] = True
    while self.mem[cond_address]:
      st = Stack(fh.get_file(str(address)))
  #branch instructions
  def if_branch(self):
    true_cond = self.pop()
    cond = self.pop()
    if cond: st = Stack(fh.get_file(str(true_cond)))
  ###########################################################################################################################################
  inst = [literal, file_call, while_op, for_op, if_branch, get_input, info, echo, dup, swap, drop, plus, minus, star, slash, orOp, negate,
          equals, notequals, rnd, fetch, store, less_than, greater_than, less_or_equal, greater_or_equal, modulus, power, concat, sub,
          square_root, cos, sin, tan, dist, repeat, join, size, increment, decrement, write, join_new_line, rnd_str, starts, ends, get_time,
          read]
