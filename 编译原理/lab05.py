'''
@author: xky
'''
import time

FIRST = {}
FOLLOW = {}
Table = {}
GOTO = {('0', ' i'): 's3', ('1', ' #'): 'acc', ('2', ' ='): ')', ('3', ' ='): ')', ('4', ' ('): 's8', ('4', ' i'): 's9',
        ('5', ' #'): 'r1', ('5', ' +'): 's10', ('5', ' -'): 's11', ('6', ' #'): 'r4', ('6', ' +'): 'r4',
        ('6', ' -'): 'r4', ('6', ' )'): 'r4', ('6', ' *'): 's12', ('6', ' /'): 's13', ('7', ' #'): 'r7',
        ('7', ' +'): 'r7', ('7', ' -'): 'r7', ('7', ' *'): 'r7', ('7', ' /'): 'r7', ('7', ' )'): 'r7',
        ('8', ' ('): 's8', ('8', ' i'): 's9', ('9', ' #'): 'r9', ('9', ' +'): 'r9', ('9', ' -'): 'r9',
        ('9', ' *'): 'r9', ('9', ' /'): 'r9', ('9', ' )'): 'r9', ('10', ' ('): 's8', ('10', ' i'): 's9',
        ('11', ' ('): 's8', ('11', ' i'): 's9', ('12', ' ('): 's8', ('12', ' i'): 's9', ('13', ' ('): 's8',
        ('13', ' i'): 's9', ('14', ' )'): 's19', ('14', ' +'): 's10', ('14', ' -'): 's11', ('15', ' #'): 'r2',
        ('15', ' +'): 'r2', ('15', ' -'): 'r2', ('15', ' )'): 'r2', ('15', ' *'): 's12', ('15', ' /'): 's13',
        ('16', ' #'): 'r3', ('16', ' +'): 'r3', ('16', ' -'): 'r3', ('16', ' )'): 'r3', ('16', ' *'): 's12',
        ('16', ' /'): 's13', ('17', ' #'): 'r5', ('17', ' +'): 'r5', ('17', ' -'): 'r5', ('17', ' *'): 'r5',
        ('17', ' /'): 'r5', ('17', ' )'): 'r5', ('18', ' #'): 'r6', ('18', ' +'): 'r6', ('18', ' -'): 'r6',
        ('18', ' *'): 'r6', ('18', ' /'): 'r6', ('18', ' )'): 'r6', ('19', ' #'): 'r8', ('19', ' +'): 'r8',
        ('19', ' -'): 'r8', ('19', ' *'): 'r8', ('19', ' /'): 'r8', ('19', ' )'): 'r8'}

ACTION = {('0', ' A'): '1', ('0', ' V'): '2', ('4', ' E'): '5', ('4', ' T'): '6', ('4', ' F'): '7', ('8', ' E'): '14',
          ('8', ' T'): '6', ('8', ' F'): '7', ('10', ' T'): '15', ('10', ' F'): '7', ('11', ' T'): '16',
          ('11', ' F'): '7', ('12', ' F'): '17', ('13', ' F'): '18'}

SLR_TABLE = [[None, None, None, None, None, None, None, 's3', None, 1, 2, None, None, None],
             [None, None, None, None, None, None, None, None, 'acc', None, None, None, None, None],
             ['s4', None, None, None, None, None, None, None, None, None, None, None, None, None],
             ['r10', None, None, None, None, None, None, None, None, None, None, None, None, None],
             [None, None, None, None, None, 's8', None, 's9', None, None, None, 5, 6, 7],
             [None, 's10', 's11', None, None, None, None, None, 'r1', None, None, None, None, None],
             [None, 'r4', 'r4', 's12', 's13', None, 'r4', None, 'r4', None, None, None, None, None],
             [None, 'r7', 'r7', 'r7', 'r7', None, 'r7', None, 'r7', None, None, None, None, None],
             [None, None, None, None, None, 's8', None, 's9', None, None, None, 14, 6, 7],
             [None, 'r9', 'r9', 'r9', 'r9', None, 'r9', None, 'r9', None, None, None, None, None],
             [None, None, None, None, None, 's8', None, 's9', None, None, None, None, 15, 7],
             [None, None, None, None, None, 's8', None, 's9', None, None, None, None, 16, 7],
             [None, None, None, None, None, 's8', None, 's9', None, None, None, None, None, 17],
             [None, None, None, None, None, 's8', None, 's9', None, None, None, None, None, 18],
             [None, 's10', 's11', None, None, None, 's19', None, None, None, None, None, None, None],
             [None, 'r2', 'r2', 's12', 's13', None, 'r2', None, 'r2', None, None, None, None, None],
             [None, 'r3', 'r3', 's12', 's13', None, 'r3', None, 'r3', None, None, None, None, None],
             [None, 'r5', 'r5', 'r5', 'r5', None, 'r5', None, 'r5', None, None, None, None, None],
             [None, 'r6', 'r6', 'r6', 'r6', None, 'r6', None, 'r6', None, None, None, None, None],
             [None, 'r8', 'r8', 'r8', 'r8', None, 'r8', None, 'r8', None, None, None, None, None]]

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
                    if key not in VN:
                        VN.add(key)
                    LANGUAGE[key].append(m)
                else:
                    if key not in VN:
                        VN.add(key)
                    LANGUAGE[key] = [m]
    # 去掉|号
    VT.remove('|')
    print("START: %s VN：%s VT：%s" % (START, VN, VT))
    # LANG变为list形式
    VN = ['S', 'A', 'V', 'E', 'T', 'F']
    VT = ['=', '+', '-', '*', '/', '(', ')', 'i', '#']
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


def print_slr1():
    print('\t\tGOTO表')
    for i, g in enumerate(GOTO):
        if i % 5 == 0 and i != 0:
            print()
        print("%s + %s -> %s" % (g[0], g[1], GOTO[g]), end='\t')
    print()
    print('\t\tACTION表')
    for i, g in enumerate(ACTION):
        if i % 5 == 0 and i != 0:
            print()
        print("%s + %s -> %s" % (g[0], g[1], ACTION[g]), end='\t')
    print()
    print('\t\tSLR分析表')
    print(VT)
    head=[' ']
    head.extend(VT)
    VN.remove('S')
    head.extend(VN)
    tb = PrettyTable(head)
    for state,value in enumerate(SLR_TABLE):
        row=[state]
        row.extend(value)
        tb.add_row(row)
    print(tb)
    VN.insert(0,'S')
def find_vt(f_vt):
    for index, v in enumerate(VT):
        if v == f_vt:
            return index


def find_vn(f_vn):
    for index, v in enumerate(VN):
        if v == f_vn:
            return index


def analy_slr1():
    global VN
    global LANGUAGE
    N_LANGUAGE = []
    N_LANGUAGE.append(['S', 'A'])
    for key in LANGUAGE:
        for value in LANGUAGE[key]:
            value_arr = []
            for v in value:
                value_arr.append(v)
            N_LANGUAGE.append([key, value_arr])
    LANGUAGE = N_LANGUAGE
    # 初始化状态
    now = 0
    stage_arr = []
    stage_arr.append(0)
    # 创建符号栈
    signal_arr = []
    signal_arr.append('#')
    in_str = 'i=i+i*ii#'
    in_str = 'i=i*(i+i)#'
    print('\t\t\t\tSLR(1)分析过程如下')
    tb = PrettyTable(["状态栈", '符号栈', '输入符号串', 'ACTION', 'GOTO'])
    while True:
        row = []
        # 加入状态栈行和符号栈行
        row.append(str(stage_arr))
        row.append(str(signal_arr))
        # 读入下一个状态
        now_stage = stage_arr[-1]
        now_slr_act = SLR_TABLE[now_stage][find_vt(in_str[now])]
        if now_slr_act and 's' in now_slr_act:
            # 如果当前状态与字符指针所指字符在SLR表中是ACTION,状态转换，则把当前now_stage字符压栈，
            # 因为每次压栈时要同时压入字符和状态，此时压入的对应的状态就是ACTION里标明的状态，然后读取下一个字符
            next_status = int(now_slr_act[1:])
            stage_arr.append(next_status)
            signal_arr.append(in_str[now])
            row.append(in_str[now:])
            row.append(now_slr_act)
            now += 1
            if len(row) != 5:
                row.append('')
            tb.add_row(row)
        elif now_slr_act and 'r' in now_slr_act:
            # 如果当前状态与字符指针所指字符在SLR表中是REDUCE，首先查看Ri对应的产生式，
            # 比如说A->V=E，此时则需要弹出栈中的V=E，把A压栈
            row.append(in_str[now:])
            row.append(now_slr_act)
            rulepos = int(now_slr_act[1:])
            count = 0
            while count != len(LANGUAGE[rulepos][1]):
                # 与A同时压栈的状态为当前的状态
                # 字符和状态一起弹出
                signal_arr.pop()
                stage_arr.pop()
                count += 1
            signal_arr.append(LANGUAGE[rulepos][0])
            now_siagnl = signal_arr[-1]
            while True:
                # 查找A在SLR表中对应的GOTO，如果当前状态为1，那么与A一起压栈的状态就是(1，A)对应的GOTO状态。
                now_stage = stage_arr[-1]
                now_slr_go = SLR_TABLE[now_stage][find_vn(now_siagnl) + len(VT) - 1]
                if now_slr_go:
                    stage_arr.append(now_slr_go)
                    row.append(now_slr_go)
                    break
                else:
                    stage_arr.pop()
            if len(row) != 5:
                row.append('')
            tb.add_row(row)
        # 如果状态是acc则结束分析，接受字符串
        elif now_slr_act == 'acc':
            print(tb)
            print('接受字符串:%s ，规约成功！' % in_str)
            break
        else:
            print(tb)
            print('%s为不合法字符串' % in_str)
            print('接受字符串失败，错误字符串:%s ,错误字符：%s！' % (in_str, in_str[0]))
            break


if __name__ == '__main__':
    start = time.time()
    gen_lang()
    gen_first()
    gen_follow()
    print_slr1()
    analy_slr1()
    end = time.time()
    print("花费时间：%s" % (end - start))
