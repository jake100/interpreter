import cProfile
import random
import stack
import parser
import loader
def main():
  print('starting...')
  main = loader.fh.files['main']
  print('loading...')
  print(main.tokens, main.strings, main.functions)
  st = stack.Stack(main.tokens, main.strings, main.functions)
  print('done...')
if __name__ == '__main__':
  main()  #cProfile.run('main()')
