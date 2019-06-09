'''
@author: xky
'''
import time
from collections import defaultdict
import os
import time
from prettytable import PrettyTable
from lexer.punc import SINGLE_PUNC_MAP, SINGLE_OPERATE_MAP
from config import *

# 终结符集合
VT = []
VN = []
SELECT = {}
# 存储规则左部和右部的集合
LANGUAGE = []
TABLE = {}
# first集
FIRST = []
# follow集
FOLLOW = []

# SLR(1)分析表
SLR1 = []
# 项目集族
ITEM_SETS = []
# 所有状态转换集合
STATE_ITEM = []


# 添加表格包
# try:
#     from prettytable import PrettyTable
# except Exception as e:
#     print(e)
#     try:
#         os.system('python -m pip install prettytable')
#         print("安装prettytable包成功")
#         from prettytable import PrettyTable
#     except Exception as e:
#         print(e)


# 申明全局变量用于修改。
def gen_lang():
    global LANGUAGE
    global VT
    global VN
    global START
    T_LANGUAGE = {}
    with open(lang_file, 'r', encoding='utf8')as f:
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
                    # else:
                    #     VT.add(v)
            more_value = value.split("|")
            for m in more_value:
                if key in T_LANGUAGE.keys():
                    # if key not in VN:
                    # VN.add(key)
                    T_LANGUAGE[key].append(m)
                else:
                    # if key not in VN:
                    #     VN.add(key)
                    T_LANGUAGE[key] = [m]
    # 去掉|号
    # VT.remove('|')
    # VT.add('#')
    # VT=list(VT)
    # VN=list(VN)
    # LANG变为list形式
    for key in T_LANGUAGE:
        for value in T_LANGUAGE[key]:
            value_arr = []
            for v in value:
                value_arr.append(v)
            LANGUAGE.append([key, value_arr])


def gen_vn_vt():
    global VN, VT
    for key in LANGUAGE:
        vn = key[0]
        value = key[1]
        if vn not in VN:
            VN.append(vn)
        for v in value:
            if v.isupper():
                if v not in VN:
                    VN.append(v)
            elif v != '$' and "'" not in v:
                if v not in VT:
                    VT.append(v)
            elif "'" in v:
                if v not in VN:
                    VN.append(v)
    VT.append('#')


def gen_first(current):
    global FIRST, LANGUAGE
    # 全序遍历防止first集加入不完整
    for key in LANGUAGE:
        vn = key[0]
        value = key[1]
        if current == vn:
            current_pos = VN.index(current)
            # 遍历产生式，把产生式的第一个加入first集合中
            if value[0] in VT or value[0] == '$':
                if value[0] not in FIRST[current_pos]:
                    FIRST[current_pos].append(value[0])
            else:
                t_vn_pos = VN.index(value[0])
                # 遍历产生式，如果第一个字符是非终结符X，把该字符的first集合加入A
                if not FIRST[t_vn_pos] and value[0] != vn:
                    gen_first(value[0])
                if '$' in FIRST[VN.index(value[0])]:
                    temp = FIRST[VN.index(value[0])][:]
                    FIRST[current_pos] = temp.remove('$')
                else:
                    for c_arr in FIRST[VN.index(value[0])]:
                        if c_arr not in FIRST[current_pos]:
                            FIRST[current_pos].extend(c_arr)


def gen_follow():
    global FOLLOW
    for current in VN:
        if '#' not in FOLLOW[0]:
            FOLLOW[0].append('#')
        for key in LANGUAGE:
            value = key[1]
            if current in value:
                ch_pos = value.index(current)
                # 若A→αB是一个产生式，则把FOLLOW(A)加至FOLLOW(B)中
                if ch_pos == len(value) - 1:
                    for c_arr in FOLLOW[VN.index(key[0])]:
                        if c_arr not in FOLLOW[VN.index(current)]:
                            FOLLOW[VN.index(current)].extend(c_arr)
                elif value[ch_pos + 1] in VT:
                    if value[ch_pos + 1] not in FOLLOW[VN.index(current)]:
                        FOLLOW[VN.index(current)].extend(value[ch_pos + 1])
                # A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中
                elif ch_pos + 1 == len(value) - 1 and '$' in FIRST[VN.index(value[ch_pos + 1])]:
                    for t in FOLLOW[VN.index(key[0])]:
                        if t not in FOLLOW[VN.index(current)]:
                            FOLLOW[VN.index(current)].extend(t)
                # 若A→αBβ是一个产生式，则把FIRST(β)\{$}加至FOLLOW(B)中；
                if ch_pos != len(value) - 1 and value[ch_pos + 1] in VN:
                    # 去掉空串
                    if '$' in FIRST[VN.index(value[ch_pos + 1])]:
                        temp = FIRST[VN.index(value[ch_pos + 1])][:]
                        temp.remove('$')
                        for char in temp:
                            if char not in FOLLOW[VN.index(current)]:
                                FOLLOW[VN.index(current)].append(char)
                    else:
                        for e in FIRST[VN.index(value[ch_pos + 1])]:
                            if e not in FOLLOW[VN.index(current)]:
                                FOLLOW[VN.index(current)].extend(e)


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


def init_ass():
    ass_file = open(assembly_file, 'w')
    ass_file.write("DATAS  SEGMENT\n")
    ass_file.write("  ;\n")
    ass_file.write("DATAS  ENDS\n")
    ass_file.write("CODES  SEGMENT\n")
    ass_file.write("ASSUME   CS:CODES,DS:DATAS\n")
    ass_file.write("START:\n")
    return ass_file


# 四元组转汇编语句
def arr2assembly(ass_file, no, arr):
    if arr[0] == '=':
        ass_file.write('  MOV,%s,%s\n' % (arr[-1], arr[-3]))
    if arr[0] == '+':
        ass_file.write('  MOV,%s,%s\n' % (arr[-1], 0))
        ass_file.write('  ADD,%s,%s\n' % (arr[-1], arr[-2]))
        ass_file.write('  ADD,%s,%s\n' % (arr[-1], arr[-3]))
    if arr[0] == '-':
        ass_file.write('  MOV,%s,%s\n' % (arr[-1], 0))
        ass_file.write('  SUB,%s,%s\n' % (arr[-1], arr[-2]))
        ass_file.write('  SUB,%s,%s\n' % (arr[-1], arr[-3]))
    if arr[0] == '*':
        ass_file.write('  MOV,%s,%s\n' % (arr[-1], 0))
        ass_file.write('  MUL,%s,%s\n' % (arr[-1], arr[-2]))
        ass_file.write('  MUL,%s,%s\n' % (arr[-1], arr[-3]))
    if arr[0] == "/":
        ass_file.write('  MOV,%s,%s\n' % (arr[-1], 0))
        ass_file.write('  DIV,%s,%s\n' % (arr[-1], arr[-2]))
        ass_file.write('  DIV,%s,%s\n' % (arr[-1], arr[-3]))
    # 大于转移
    if arr[0] == "jmp>":
        ass_file.write('  CMP,%s,%s\n' % (arr[-3], arr[-2]))
        ass_file.write('  JA,%s\n' % (arr[-1]))
    if arr[0] == "jmp<":
        ass_file.write('  CMP,%s,%s\n' % (arr[-3], arr[-2]))
        ass_file.write('  JB,%s\n' % (arr[-1]))
    if arr[0] == "jmp":
        ass_file.write('  JMP,%s\n' % (arr[-1]))


def closure(c_arr):
    index_i = 0
    flag = len(c_arr)
    while index_i != flag:
        pos = c_arr[index_i][2]
        vts = c_arr[index_i][1]
        vn = c_arr[index_i][0]
        if pos != len(vts) and vts[pos] in VN:
            if index_i > 0:
                if vts[pos] == c_arr[index_i - 1][1][c_arr[index_i - 1][2]]:
                    index_i += 1
                    continue
            for key in LANGUAGE:
                if key[0] == vts[pos]:
                    temp_c = [index_i for index_i in range(3)]
                    temp_c[0] = key[0]
                    temp_c[1] = key[1]
                    temp_c[2] = 0
                    c_arr.append(temp_c)
        flag = len(c_arr)
        index_i += 1


def go(n, x):
    init_col = []
    for key in ITEM_SETS[n]:
        temp_pos = key[2]
        if temp_pos != len(key[1]) and key[1][temp_pos] == x:
            temp_item = [i for i in range(3)]
            temp_item[0] = key[0]
            temp_item[1] = key[1]
            temp_item[2] = key[2] + 1
            init_col.append(temp_item)
    closure(init_col)
    try:
        # 如果在项目集中
        status_pos = ITEM_SETS.index(init_col)

        temp_state = [0 for i in range(3)]
        temp_state[0] = n
        temp_state[1] = status_pos
        temp_state[2] = x
        STATE_ITEM.append(temp_state)

    except:
        # 如果没在项目集中
        ITEM_SETS.append(init_col)
        temp_state = [0 for i in range(3)]
        temp_state[0] = n
        temp_state[1] = len(ITEM_SETS) - 1
        temp_state[2] = x
        STATE_ITEM.append(temp_state)


def gen_proj():
    # 生成项目集族
    # 生成初始c
    temp_c = [i for i in range(3)]
    temp_c[0] = LANGUAGE[0][0]
    temp_c[1] = LANGUAGE[0][1]
    temp_c[2] = 0
    ITEM_SETS.append([temp_c, ])
    closure(ITEM_SETS[0])
    flag = len(ITEM_SETS)
    index_i = 0
    while index_i != flag:
        # 读操作
        key = ITEM_SETS[index_i]
        for index_j, value in enumerate(key):
            temp_pos = value[2]
            last_value = ITEM_SETS[index_i][index_j - 1]
            # 判断前一个项目及状态
            if temp_pos != len(value[1]):
                if last_value[2] != len(last_value[1]) and index_j > 0:
                    if value[1][temp_pos] == last_value[1][last_value[2]]:
                        continue
                go(index_i, value[1][temp_pos])
                flag = len(ITEM_SETS)
        index_i += + 1


def gen_slr1():
    # 生成slr表
    global SLR_TABLE
    SLR_TABLE = [[None for i in range(len(VT) + len(VN) - 1)] for j in ITEM_SETS]
    for state_i in STATE_ITEM:
        if state_i[2] in VT:
            SLR_TABLE[state_i[0]][VT.index(state_i[2])] = 's' + str(state_i[1])
        else:
            SLR_TABLE[state_i[0]][VN.index(state_i[2]) + len(VT) - 1] = state_i[1]
    for index, key in enumerate(ITEM_SETS):
        for value in key:
            # 非终结符是否在项目集的项目中
            vn_pos = VN.index(value[0])
            vn = value[0]
            vts = value[1]
            state = value[2]
            if state == len(vts) and vn == VN[0]:
                SLR_TABLE[index][VT.index('#')] = 'acc'
            elif state == len(vts):
                rule_pos = LANGUAGE.index(value[:2])
                for q in range(len(FOLLOW[vn_pos])):
                    # 如果是递归动作，加入slr表中
                    if FOLLOW[vn_pos][q] in VT:
                        SLR_TABLE[index][VT.index(FOLLOW[vn_pos][q])] = 'r' + str(rule_pos)


def gen_slr1_table():
    # print('\t\t\t\t\t\t\SLR(1)分析表')
    row = [' ']
    for vt in VT:
        row.append(vt)
    for vn in VN[1:]:
        row.append(vn)
    tb = PrettyTable(row)
    for i, key in enumerate(SLR_TABLE):
        row = [i]
        for v in key:
            row.append(v)
        tb.add_row(row)
    return tb


def analy_slr1():
    global VN
    global LANGUAGE
    LANGUAGE.append(['S', 'A'])
    # 初始化状态
    now = 0
    stage_arr = []
    stage_arr.append(0)
    # 创建符号栈
    signal_arr = []
    signal_arr.append('#')
    # in_str = 'i=i+i*ii#'
    # in_str = 'i=i*(i+i)#'
    # 维护一个翻译栈
    fanyi_arr = []
    fanyi_count = 0
    with open(input_str_file, 'r')as f:
        in_str = f.read().strip('\n')
    with open(input_source_file, 'r')as f:
        ori_input = f.read().strip('\n').split(' ')
    # print('\t\t\t\tSLR(1)分析过程如下')
    tb = PrettyTable(["状态栈", '符号栈', '输入符号串', 'ACTION', 'GOTO', "翻译栈"])
    fanyi_result = []
    while True:
        # v变量variable，d，digital
        if signal_arr[-1] == 'v' or signal_arr[-1] == 'd' or signal_arr[-1] == '>' or signal_arr[-1] == '<':
            # 把非终结符与原始输入串的对应关系连接起来存储进入数组。
            t_arr = [signal_arr[-1], ori_input[now - 1]]
            fanyi_arr.append(t_arr)
        row = []
        # 加入状态栈行和符号栈行
        # 读入下一个状态
        now_stage = stage_arr[-1]
        now_slr_act = SLR_TABLE[now_stage][VT.index(in_str[now])]

        if now_slr_act and 's' in now_slr_act:
            # 如果当前状态与字符指针所指字符在SLR表中是ACTION,状态转换，则把当前now_stage字符压栈，
            # 因为每次压栈时要同时压入字符和状态，此时压入的对应的状态就是ACTION里标明的状态，然后读取下一个字符
            next_status = int(now_slr_act[1:])
            stage_arr.append(next_status)
            signal_arr.append(in_str[now])
            row.append(str(stage_arr))
            row.append(in_str[now:])
            row.append(now_slr_act)
            now += 1
            row.insert(1, str(signal_arr))
            if len(row) != 5:
                row.append('')
            row.append(str(fanyi_arr))
            tb.add_row(row)

        elif now_slr_act and 'r' in now_slr_act:
            # 如果当前状态与字符指针所指字符在SLR表中是REDUCE，首先查看Ri对应的产生式，
            # 比如说A->V=E，此时则需要弹出栈中的V=E，把A压栈
            row.append(in_str[now:])
            row.append(now_slr_act)
            rulepos = int(now_slr_act[1:])
            current_rule = LANGUAGE[rulepos]
            sym_count = 0
            if current_rule[0] == 'C':
                four_arr = [i for i in range(4)]
                # 如果碰到if中的cmp语句，就输入跳转四元组
                four_arr[2] = fanyi_arr.pop()[-1]
                four_arr[0] = 'jmp' + fanyi_arr.pop()[-1]
                four_arr[1] = fanyi_arr.pop()[-1]
                # 如果进入if语句，那就进入
                four_arr[3] = str(fanyi_count + 2)
                fanyi_result.extend(four_arr)
                fanyi_result.extend(['jmp', '_', '_', str(fanyi_count + 3)])
            for sym in current_rule[1]:
                if sym in VN:
                    sym_count += 1
            if sym_count > 1:
                # 找到非终结符后面的操作数
                opt = current_rule[1][1]
                # 如果找到IF语句,把赋值符号给替换
                if opt == '(' or opt == 'A':
                    opt = '='
                fanyi_result.append(opt)
                if opt == '=':
                    fanyi_result.append(fanyi_arr[-1][1])
                    fanyi_result.append('_')
                    fanyi_arr.pop()
                    fanyi_result.append(fanyi_arr[-1][1])

                else:
                    for i in range(sym_count):
                        fanyi_result.append(fanyi_arr[-1][1])
                        fanyi_arr.pop()
                    fanyi_result.append("S%s" % fanyi_count)
                    fanyi_arr.append(["S%s" % fanyi_count, "S%s" % fanyi_count])
                    fanyi_count += 1

            count = 0
            temp_arr = []
            while count != len(current_rule[1]):
                # 与A同时压栈的状态为当前的状态
                # 字符和状态一起弹出
                signal_arr.pop()
                stage_arr.pop()
                count += 1
                # temp_arr.append(punc)
            # 吧替換后的加入
            signal_arr.append(current_rule[0])
            now_siagnl = signal_arr[-1]

            # 遍历使用的规则产生式，如果有两个以上的非终结符那就可以输出语法制导的结果
            while True:
                # 查找A在SLR表中对应的GOTO，如果当前状态为1，那么与A一起压栈的状态就是(1，A)对应的GOTO状态。
                now_stage = stage_arr[-1]
                now_slr_go = SLR_TABLE[now_stage][VN.index(now_siagnl) + len(VT) - 1]
                if now_slr_go:
                    stage_arr.append(now_slr_go)
                    row.append(now_slr_go)
                    break
                else:
                    stage_arr.pop()
            # 最后加入更新后的栈
            row.insert(0, str(stage_arr))
            row.insert(1, str(signal_arr))
            if len(row) != 5:
                row.append('')
            row.append(fanyi_arr)
            tb.add_row(row)

        # 如果状态是acc则结束分析，接受字符串

        elif now_slr_act == 'acc':
            count = len(signal_arr) - 1
            while count:
                # acc清空站
                signal_arr.pop()
                stage_arr.pop()
                count -= 1
            row.append(str(stage_arr))
            row.append(signal_arr)
            row.append(in_str[now:])
            row.append(now_slr_act)
            row.append('')
            row.append(fanyi_arr)
            tb.add_row(row)
            # print(tb)
            print('接受字符串:%s ！' % in_str)
            break
        else:
            print(tb)
            print('%s为不合法字符串' % in_str)
            print('接受字符串失败，错误字符串:%s ,错误字符：%s！' % (in_str, in_str[now]))
            break
    quad_file = open(quadruples_file, 'w')
    ass_file = init_ass()
    quad_str = ''
    for f in range(len(fanyi_result) // 4):
        line = str(f) + ' (' + ','.join(fanyi_result[f * 4:(f + 1) * 4]) + ')'
        quad_file.write(line + '\n')
        quad_str += line + '\n'
        assembly = arr2assembly(ass_file, f, fanyi_result[f * 4:(f + 1) * 4])
    ass_file.write('  INT 21H\n')
    ass_file.write('CODE ENDS\n')
    ass_file.write('  END START\n')
    return tb, quad_str


def slr1_analyse():
    global SLR_TABLE, FIRST, FOLLOW
    gen_lang()
    gen_vn_vt()
    for i in VN:
        FIRST.append([])
        FOLLOW.append([])
    for vn in VN:
        gen_first(vn)
    gen_follow()
    gen_proj()
    gen_slr1()
    slr_table = gen_slr1_table()
    slr_process, slr_quad = analy_slr1()
    print(VN, VT, FIRST, FOLLOW, "\t状态\t\t\t\tACTION\t\t\t\t\t\t\t\tGOTO\n%s" % slr_table, slr_process, slr_quad)
    return VN, VT, FIRST, FOLLOW, "\t状态\t\t\t\tACTION\t\t\t\t\t\t\t\tGOTO\n%s" % slr_table, slr_process, slr_quad

# slr1_analyse()
