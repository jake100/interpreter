import cProfile
import random
import stack
import parse
import file_handler
def main():
  s = stack.Stack(file_handler.fh.get_file('main'))
if __name__ == '__main__':
  main()
  #cProfile.run('main()')
