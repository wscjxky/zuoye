'''
@author: xky
'''
import time
from collections import defaultdict

FIRST = {}
FOLLOW = {}
Table = {}
DFA={0: ['S->·A', 'A->·V=E', 'V->·i'], 1: ['S->A·'], 2: ['A->V·=E'], 3: ['V->i·'], 4: ['A->V=·E', 'E->·E+T', 'E->·E-T', 'E->·T', 'T->·T*F', 'T->·T/F', 'T->·F', 'F->·(E)', 'F->·i'], 5: ['A->V=E·', 'E->E·+T', 'E->E·-T'], 6: ['E->T·', 'T->T·*F', 'T->T·/F'], 7: ['T->F·'], 8: ['F->(·E)', 'E->·E+T', 'E->·E-T', 'E->·T', 'T->·T*F', 'T->·T/F', 'T->·F', 'F->·(E)', 'F->·i'], 9: ['F->i·'], 10: ['E->E+·T', 'T->·T*F', 'T->·T/F', 'T->·F', 'F->·(E)', 'F->·i'], 11: ['E->E-·T', 'T->·T*F', 'T->·T/F', 'T->·F', 'F->·(E)', 'F->·i'], 12: ['T->T*·F', 'F->·(E)', 'F->·i'], 13: ['T->T/·F', 'F->·(E)', 'F->·i'], 14: ['F->(E·)', 'E->E·+T', 'E->E·-T'], 15: ['E->E+T·', 'T->T·*F', 'T->T·/F'], 16: ['E->E-T·', 'T->T·*F', 'T->T·/F'], 17: ['T->T*F·'], 18: ['T->T/F·'], 19: ['F->(E)·']}
ACTION = {('0', 'i'): 's3', ('1', '#'): 'r0', ('2', '='): 's4', ('3', '='): 'r10', ('4', '('): 's8', ('4', 'i'): 's9',
        ('5', '#'): 'r1', ('5', '+'): 's10', ('5', '-'): 's11', ('6', '#'): 'r4', ('6', '+'): 'r4',
        ('6', '-'): 'r4', ('6', ')'): 'r4', ('6', '*'): 's12', ('6', '/'): 's13', ('7', '#'): 'r7',
        ('7', '+'): 'r7', ('7', '-'): 'r7', ('7', '*'): 'r7', ('7', '/'): 'r7', ('7', ')'): 'r7',
        ('8', '('): 's8', ('8', 'i'): 's9', ('9', '#'): 'r9', ('9', '+'): 'r9', ('9', '-'): 'r9',
        ('9', '*'): 'r9', ('9', '/'): 'r9', ('9', ')'): 'r9', ('10', '('): 's8', ('10', 'i'): 's9',
        ('11', '('): 's8', ('11', 'i'): 's9', ('12', '('): 's8', ('12', 'i'): 's9', ('13', '('): 's8',
        ('13', 'i'): 's9', ('14', ')'): 's19', ('14', '+'): 's10', ('14', '-'): 's11', ('15', '#'): 'r2',
        ('15', '+'): 'r2', ('15', '-'): 'r2', ('15', ')'): 'r2', ('15', '*'): 's12', ('15', '/'): 's13',
        ('16', '#'): 'r3', ('16', '+'): 'r3', ('16', '-'): 'r3', ('16', ')'): 'r3', ('16', '*'): 's12',
        ('16', '/'): 's13', ('17', '#'): 'r5', ('17', '+'): 'r5', ('17', '-'): 'r5', ('17', '*'): 'r5',
        ('17', '/'): 'r5', ('17', ')'): 'r5', ('18', '#'): 'r6', ('18', '+'): 'r6', ('18', '-'): 'r6',
        ('18', '*'): 'r6', ('18', '/'): 'r6', ('18', ')'): 'r6', ('19', '#'): 'r8', ('19', '+'): 'r8',
        ('19', '-'): 'r8', ('19', '*'): 'r8', ('19', '/'): 'r8', ('19', ')'): 'r8'}

GOTO = {('0', 'A'): '1', ('0', 'V'): '2', ('4', 'E'): '5', ('4', 'T'): '6', ('4', 'F'): '7', ('8', 'E'): '14',
          ('8', 'T'): '6', ('8', 'F'): '7', ('10', 'T'): '15', ('10', 'F'): '7', ('11', 'T'): '16',
          ('11', 'F'): '7', ('12', 'F'): '17', ('13', 'F'): '18'}

# 终结符集合
VT = set()
VN = set()
SELECT = {}
LANGUAGE = {}
TABLE = {}
import os
import time

# 添加表格包
try:
    from prettytable import PrettyTable
except Exception as e:
    print(e)
    try:
        os.system('python -m pip install prettytable')
        print("安装prettytable包成功")
        from prettytable import PrettyTable
    except Exception as e:
        print(e)


# 申明全局变量用于修改。
def gen_lang():
    global LANGUAGE
    global VT
    global VN
    global START
    with open('Lang.txt', 'r', encoding='utf8')as f:
        ls = f.readlines()
        START = ls[0][2]
        for l in ls[1:]:
            l = l.strip('\n')
            l = l.replace('E`', 'Z')
            l = l.replace('T`', 'X')
            key, value = l.split("->")
            if key == 'T`':
                key = 'Z'
            if key == 'E`':
                key = 'X'
            for v in value:
                if "A" <= v <= "Z":
                    pass
                else:
                    VT.add(v)
            more_value = value.split("|")
            for m in more_value:
                if key in LANGUAGE.keys():
                    VN.add(key)
                    LANGUAGE[key].append(m)
                else:
                    VN.add(key)
                    LANGUAGE[key] = [m]
    # 去掉|号
    VT.remove('|')
    print("START: %s VN：%s VT：%s" % (START, VN, VT))
    print("LANGUAGE：%s" % LANGUAGE)


def gen_first():
    for k in LANGUAGE:
        l = LANGUAGE[k]
        FIRST[k] = list()
        # 遍历产生式，把产生式的第一个加入first集合中
        for s in l:
            if not (s[0].isupper()):
                FIRST[k].append(s[0])
    # 遍历4次，防止first集加入不完整
    for i in range(4):
        for k in LANGUAGE:
            l = LANGUAGE[k]
            for s in l:
                # 遍历产生式，如果第一个字符是非终结符X，把该字符的first集合加入A
                if s[0] in VN:
                    FIRST[k].extend(FIRST[s[0]])
                    FIRST[k] = list(set(FIRST[k]))  # 去重
    print("FIRST集为：%s" % FIRST)


def gen_follow():
    for k in LANGUAGE:
        FOLLOW[k] = list()
        if k == list(LANGUAGE.keys())[0]:
            FOLLOW[k].append('#')
    for i in range(2):
        for k in LANGUAGE:
            l = LANGUAGE[k]
            for s in l:
                # 若A→αB是一个产生式，则把FOLLOW(A)加至FOLLOW(B)中
                if s[len(s) - 1] in VN:
                    FOLLOW[s[len(s) - 1]].extend(FOLLOW[k])
                    # 去掉空串
                    try:
                        FOLLOW[s[len(s) - 1]].remove("$")
                    except:
                        pass
                for index in range(len(s) - 1):
                    if s[index] in VN:
                        if s[index + 1] in VN:  # 若A→αBβ是一个产生式，则把FIRST(β)\{ε}加至FOLLOW(B)中；
                            FOLLOW[s[index]].extend(FIRST[s[index + 1]])
                            try:
                                FOLLOW[s[index]].remove("$")
                            except:
                                pass
                        if not (s[index + 1] in VN) and (s[index + 1] != '$'):
                            FOLLOW[s[index]].append(s[index + 1])
                        emptyflag = 1
                        for i in range(index + 1, len(s)):
                            if not (s[i] in VN) or (s[i] in VN and ('$' not in FIRST[s[i]])):
                                emptyflag = 0
                                break
                        if emptyflag == 1:
                            FOLLOW[s[index]].extend(FOLLOW[k])  # A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中
                            try:
                                FOLLOW[s[index]].remove("$")
                            except:
                                pass
    # 去重
    for k in FOLLOW:
        FOLLOW[k] = list(set(FOLLOW[k]))
    print('FOLLOW集为：%s' % FOLLOW)


def gen_select():
    for key in VN:
        for s in LANGUAGE[key]:
            # 先把first集加入select集合
            if s[0] in VT:
                SELECT[key + '->' + s] = [s[0]]
            elif s[0] == '$':
                SELECT[key + '->' + s] = set(FOLLOW[key])
            else:
                SELECT[key + '->' + s] = FIRST[key]
                if '$' in SELECT[key + '->' + s]:
                    # 如果能退出空串，Select（A->X）= (first(A) - e)∪(follow)
                    SELECT[key + '->' + s].remove('$')
                    SELECT[key + '->' + s] = set(SELECT[key + '->' + s]) | set(FOLLOW[key])
    print('SELECT集为：%s' % SELECT)


def gen_table():
    # 生成分析表
    for x in VN:
        for y in VT:
            for key in SELECT:
                # 最后会生成["E",","]="ETC"格式的分析表
                if x == key[0] and y in SELECT[key]:
                    TABLE[x + ',' + y] = key[3:]
                    break
    print('分析表：%s' % TABLE)


def main():
    stack = ['#', 'S']
    instr = "i=i+i*i#"
    in_len = len(instr)
    print('分析过程:')
    VT.add('$')
    flag = 1
    while stack:
        if stack[-1] in VT:
            # 如果栈顶刚好是终结符，接受并且pop栈
            if stack[-1] == instr[0]:
                t = instr[0]
                stack.pop()
                instr = instr[1:]
                print("%s        %s     %s" % (stack, t, instr))
        # 如果栈顶是非终结符
        elif stack[-1] in VN:
            while True:
                # 查分析表，如果能够接受，接受并pop
                match = stack.pop() + ',' + instr[0]
                if (instr) == '#':
                    stack.pop()
                    print("%s        %s     %s" % (stack, instr[0], ''))
                    print('分析完成，字符串被成功接收！')
                    exit()
                # 查分析表，推导下一个生成式
                if (match in TABLE.keys()):
                    for i in reversed(TABLE[match]):
                        if i == '$':
                            break
                        stack.append(i)
                    print("%s        %s     %s" % (stack, instr[0], instr))
                if not stack:
                    print('分析完成，字符串被拒绝接收,错误字符为%s，位置在%s' % (instr[0], (in_len - len(instr))))
                    exit()
                if stack[-1] in VT:
                    break
                if stack[-1] == 'X' and flag:
                    flag = 0
                    stack.pop()

def show_items():
    items=[]
    statuses=[]
    print(GOTO)
    print(ACTION)
    tb = PrettyTable(["项目集编号","项目集"])
    for key in DFA.keys():
        tb.add_row([key,DFA[key]])
    print(tb)
if __name__ == '__main__':
    time.time()
    gen_lang()
    gen_first()
    gen_follow()
    show_items()
