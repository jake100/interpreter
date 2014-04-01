import parse
import os
class FileHandler:
  files = []
  def __init__(self):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'scripts'))
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
      for file in files:
        if file.endswith('.txt'):
          name = os.path.splitext(file)[0]
          self.files.append(File(name))
  def get_file(self, s):
    for file in self.files:
      if file.name == s:
        return file.tokens
class File:
  tokens = []
  def __init__(self, name):
    self.name = name
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'scripts'))
    path = os.path.join(__location__, name + '.txt')
    fo = open(path, "r")
    lines = fo.readlines()
    fo.close()
    self.tokens = parse.tokenize(lines)
fh = FileHandler()
