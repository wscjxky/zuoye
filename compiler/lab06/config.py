import os
# cwd=os.pardir
cwd=os.getcwd()
mid_dir=cwd+os.sep+'mid_result'+os.sep
print(mid_dir)
input_c_file=mid_dir+'input.c'
token_file=mid_dir+'token.txt'
input_str_file=mid_dir+'input_str.txt'
input_source_file=mid_dir+'input_source.txt'
lang_file=mid_dir+'lang.txt'
slr1_file=mid_dir+'slr1.txt'
first_file=mid_dir+'first.txt'
follow_file=mid_dir+'follow.txt'
assembly_file=mid_dir+'assembly.txt'
quadruples_file=mid_dir+'quadruples.txt'

