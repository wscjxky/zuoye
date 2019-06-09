'''
@author: xky
'''
from lexer.scanner import *
from  slr1 import *

if __name__ == '__main__':
    gen_tokens()
    gen_input_str()
    sl1_main()
    # gen_lang()
    # gen_first()
    # gen_follow()
    # gen_goto()
    # gen_action()


