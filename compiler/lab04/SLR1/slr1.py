'''
@author: xky
'''
import time
from collections import defaultdict

from lexer.punc import SINGLE_PUNC_MAP, SINGLE_OPERATE_MAP

FOLLOW = {}
Table = {}

# 终结符集合
VT = []
VN = []
SELECT = {}
LANGUAGE = []
TABLE = {}
# first集
First = []
for j in range(len(VN)):
    First.append([])
# follow集
Follow = []
# 存储规则左部和右部的集合
LANGUAGE = []
# SLR(1)分析表
SLR1 = []
# 项目集族
proj = []
# 所有状态转换集合
status_trans = []
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
    T_LANGUAGE = {}
    with open('source.txt', 'r', encoding='utf8')as f:
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
    print("LANGUAGE：%s" % LANGUAGE)


def identify_vt_and_vn():
    global VN, VT
    for i in range(len(LANGUAGE)):
        # 把规则左部加入到非终结符集合中
        if LANGUAGE[i][0] not in VN:
            VN.append(LANGUAGE[i][0])
        # 将规则右部的终结符和非终结符加入到相应的集合
        for j in range(len(LANGUAGE[i][1])):
            if LANGUAGE[i][1][j].isupper():
                if LANGUAGE[i][1][j] not in VN:
                    VN.append(LANGUAGE[i][1][j])
            elif LANGUAGE[i][1][j] != 'ε' and "'" not in LANGUAGE[i][1][j]:
                if LANGUAGE[i][1][j] not in VT:
                    VT.append(LANGUAGE[i][1][j])
            elif "'" in LANGUAGE[i][1][j]:
                if LANGUAGE[i][1][j] not in VN:
                    VN.append(LANGUAGE[i][1][j])
    VT.append('#')
    print("START: %s VN：%s VT：%s" % (START, VN, VT))


def create_first_set(ch):
    global First

    for i in range(len(LANGUAGE)):
        if ch == LANGUAGE[i][0]:
            # 如果规则右部的第一个字符为终结符或者空串，则将他们加入ch的first集
            if LANGUAGE[i][1][0] in VT or LANGUAGE[i][1][0] == 'ε':
                if LANGUAGE[i][1][0] not in First[VN.index(ch)]:
                    First[VN.index(ch)].append(LANGUAGE[i][1][0])
            else:
                temp_al = VN.index(LANGUAGE[i][1][0])
                # 如果右部第一个字符为非终结符，且该字符的First集还不存在，则递归的调用该函数求右部第一个字符的first集
                if not First[temp_al] and LANGUAGE[i][1][0] != LANGUAGE[i][0]:
                    create_first_set(LANGUAGE[i][1][0])
                # 将右部第一个字符的first集去掉空串加入到ch的first集中
                if 'ε' in First[VN.index(LANGUAGE[i][1][0])]:
                    temp = First[VN.index(LANGUAGE[i][1][0])][:]
                    First[VN.index(ch)] = temp.remove('ε')
                else:
                    for c in First[VN.index(LANGUAGE[i][1][0])]:
                        if c not in First[VN.index(ch)]:
                            First[VN.index(ch)].extend(c)


def gen_first():
    # for k in LANGUAGE:
    #     l = LANGUAGE[k]
    #     FIRST[k] = list()
    #     # 遍历产生式，把产生式的第一个加入first集合中
    #     for s in l:
    #         if not (s[0].isupper()):
    #             FIRST[k].append(s[0])
    # # 遍历4次，防止first集加入不完整
    # for i in range(4):
    #     for k in LANGUAGE:
    #         l = LANGUAGE[k]
    #         for s in l:
    #             # 遍历产生式，如果第一个字符是非终结符X，把该字符的first集合加入A
    #             if s[0] in VN:
    #                 FIRST[k].extend(FIRST[s[0]])
    #                 FIRST[k] = list(set(FIRST[k]))  # 去重
    pass


def gen_follow():
    for j in range(len(VN)):
        Follow.append([])
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


# def gen_table():
#     # 生成分析表
#     for x in VN:
#         for y in VT:
#             for key in SELECT:
#                 # 最后会生成["E",","]="ETC"格式的分析表
#                 if x == key[0] and y in SELECT[key]:
#                     TABLE[x + ',' + y] = key[3:]
#                     break
#     print('分析表：%s' % TABLE)
#
#
# def print_slr1():
#     print('\t\tGOTO表')
#     for i, g in enumerate(GOTO):
#         if i % 5 == 0 and i != 0:
#             print()
#         print("%s + %s -> %s" % (g[0], g[1], GOTO[g]), end='\t')
#     print()
#     print('\t\tACTION表')
#     for i, g in enumerate(ACTION):
#         if i % 5 == 0 and i != 0:
#             print()
#         print("%s + %s -> %s" % (g[0], g[1], ACTION[g]), end='\t')
#     print()
#     print('\t\tSLR分析表')
#     head=[' ']
#     head.extend(VT)
#     VN.remove('S')
#     head.extend(VN)
#     tb = PrettyTable(head)
#     for state,value in enumerate(SLR_TABLE):
#         row=[state]
#         row.extend(value)
#         tb.add_row(row)
#     print(tb)
#     VN.insert(0,'S')
# def find_vt(f_vt):
#     for index, v in enumerate(VT):
#         if v == f_vt:
#             return index
#
#
#
# def find_vn(f_vn):
#     for index, v in enumerate(VN):
#         if v == f_vn:
#             return index
#
#
def analy_slr1():
    global VN
    global LANGUAGE
    LANGUAGE.append(['S'])
    # 初始化状态
    now = 0
    stage_arr = []
    stage_arr.append(0)
    # 创建符号栈
    signal_arr = []
    signal_arr.append('#')
    # in_str = 'i=i+i*ii#'
    # in_str = 'i=i*(i+i)#'
    fanyi_count = 0
    in_str = 'i=i+i#'
    print('\t\t\t\tSLR(1)分析过程如下')
    tb = PrettyTable(["状态栈", '符号栈', '输入符号串', 'ACTION', 'GOTO'])
    ori_input = ''
    output = ""
    while True:
        row = []
        # 加入状态栈行和符号栈行
        row.append(str(stage_arr))
        row.append(str(signal_arr))
        # 读入下一个状态
        now_stage = stage_arr[-1]
        now_slr_act = SLR_TABLE[now_stage][VT.index(in_str[now])]
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
            current_rule = LANGUAGE[rulepos]
            count = 0
            temp_arr = []
            while count != len(current_rule[1]):
                # 与A同时压栈的状态为当前的状态
                # 字符和状态一起弹出
                punc = signal_arr.pop()
                stage_arr.pop()
                count += 1
                # temp_arr.append(punc)
            # 遍历使用的规则产生式，如果有两个以上的非终结符那就可以输出语法制导的结果
            # sym_count = 0
            # for sym in current_rule[1]:
            #     if sym in VN:
            #         sym_count += 1
            # if sym_count > 1:
            #     # 找到非终结符后面的操作数
            #     opt = current_rule[1][1]
            #     output += "(" + opt + ","
            #     print(opt)
            #     if opt == '=':
            #         output += signal_arr[-1] + ", _,"
            #         signal_arr.pop()
            #         output += signal_arr[-1] + ")"
            #     else:
            #         for i in range(sym_count):
            #             output +=  signal_arr[-1] + "," + " " + "_,"
            #             signal_arr.pop()
            #         output += "T%s" % fanyi_count
            #         # value.push("T" + std::to_string(temp));
            #         fanyi_count += 1
            signal_arr.append(current_rule[0])
            now_siagnl = signal_arr[-1]
            inputs = ['void', 'main', '(', ')', '{', 'a', '=', '1', 'return', '}']
            sta_len = (len(stage_arr))
            sig_len = (len(signal_arr))

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
            if len(row) != 5:
                row.append('')
            tb.add_row(row)
        # 如果状态是acc则结束分析，接受字符串
        elif now_slr_act == 'acc':
            print(tb)
            print('接受字符串:%s ！' % in_str)
            print(output)
            break
        else:
            print(tb)
            print('%s为不合法字符串' % in_str)
            print('接受字符串失败，错误字符串:%s ,错误字符：%s！' % (in_str, in_str[now]))
            break


def create_follow_set(ch):
    global Follow
    if '#' not in Follow[0]:
        Follow[0].append('#')
    for i in range(len(LANGUAGE)):
        if ch in LANGUAGE[i][1]:
            ch_pos = LANGUAGE[i][1].index(ch)
            # 如果ch为最后一个字符，则将产生式左部字符的Follow集加入ch的Follow集
            if ch_pos == len(LANGUAGE[i][1]) - 1:
                for c in Follow[VN.index(LANGUAGE[i][0])]:
                    if c not in Follow[VN.index(ch)]:
                        Follow[VN.index(ch)].extend(c)
            # 如果ch后的一个字符为终结符，则将该终结符加入ch的Follow集
            elif LANGUAGE[i][1][ch_pos + 1] in VT:
                if LANGUAGE[i][1][ch_pos + 1] not in Follow[VN.index(ch)]:
                    Follow[VN.index(ch)].extend(LANGUAGE[i][1][ch_pos + 1])
            # 如果ch后的一个字符的first集有空串，且该字符为最后一个元素，则将左部的Follow集加入ch的follow集
            elif ch_pos + 1 == len(LANGUAGE[i][1]) - 1 and 'ε' in First[VN.index(LANGUAGE[i][1][ch_pos + 1])]:
                for t in Follow[VN.index(LANGUAGE[i][0])]:
                    if t not in Follow[VN.index(ch)]:
                        Follow[VN.index(ch)].extend(t)
            # 如果ch后的一个字符为非终结符，则将该非终结符的first集去掉空串加入ch的Follow集
            if ch_pos != len(LANGUAGE[i][1]) - 1 and LANGUAGE[i][1][ch_pos + 1] in VN:
                if 'ε' in First[VN.index(LANGUAGE[i][1][ch_pos + 1])]:
                    temp = First[VN.index(LANGUAGE[i][1][ch_pos + 1])][:]
                    temp.remove('ε')
                    for char in temp:
                        if char not in Follow[VN.index(ch)]:
                            Follow[VN.index(ch)].append(char)
                else:
                    for e in First[VN.index(LANGUAGE[i][1][ch_pos + 1])]:
                        if e not in Follow[VN.index(ch)]:
                            Follow[VN.index(ch)].extend(e)


def is_contained(c):
    """
    判断某个项目集是否已经存在与总的项目集中
    :param c: 待判断的项目集列表
    :return: 如果项目集已经存在，返回项目集的位置，如果不存在，返回-1
    """

    for i in range(len(proj)):
        count = 0
        for j in range(len(proj[i])):
            for k in range(len(c)):
                if c[k][0] == proj[i][j][0] and c[k][1] == proj[i][j][1] and c[k][2] == proj[i][j][2]:
                    count += 1
                    break
        if count == len(proj[i]):
            return i
    return False


# 项目集族的闭包操作
def enclosure(c):
    i = 0
    l = len(c)
    while i != l:
        pos = c[i][2]
        if pos != len(c[i][1]) and c[i][1][pos] in VN:
            if i > 0:
                if c[i][1][pos] == c[i - 1][1][c[i - 1][2]]:
                    i += 1
                    continue
            for j in range(len(LANGUAGE)):
                if LANGUAGE[j][0] == c[i][1][pos]:
                    temp = [i for i in range(3)]
                    temp[0] = LANGUAGE[j][0]
                    temp[1] = LANGUAGE[j][1]
                    temp[2] = 0
                    c.append(temp)
        l = len(c)
        i += 1


# 存储状态转换情况的类
class StatusTrans(object):
    def __init__(self, status_init, status_trans, x):
        """
        :param status_init: 初始状态
        :param status_trans: 接收x后转换到的状态
        :param x: 初始状态接收非终结符x
        """
        self.status_init = status_init
        self.status_trans = status_trans
        self.x = x


def go(n, x):
    """
    项目集族的读操作
    :param n: 第n个状态
    :param x: 第n个状态接收非终结符x
    :return: 状态n接收x后转换到的新状态
    """
    c = []
    for i in range(len(proj[n])):
        # 存储一个项目集的全部项目
        p = proj[n][i][2]
        if p != len(proj[n][i][1]) and proj[n][i][1][p] == x:
            new_proj = [i for i in range(3)]
            new_proj[0] = proj[n][i][0]
            new_proj[1] = proj[n][i][1]
            new_proj[2] = proj[n][i][2] + 1
            c.append(new_proj)
    enclosure(c)
    if not is_contained(c):
        proj.append(c)
        new_status = StatusTrans(n, len(proj) - 1, x)
        status_trans.append(new_status)
    else:
        status_pos = is_contained(c)
        new_status = StatusTrans(n, status_pos, x)
        status_trans.append(new_status)


# 生成项目集族
def gen_proj():
    # 生成c0
    c_0 = [i for i in range(3)]
    c_0[0] = LANGUAGE[0][0]
    c_0[1] = LANGUAGE[0][1]
    c_0[2] = 0
    proj.append([c_0, ])
    enclosure(proj[0])
    l = len(proj)
    i = 0
    # 读操作
    while i != l:
        for j in range(len(proj[i])):
            p = proj[i][j][2]
            if p != len(proj[i][j][1]):
                if j > 0 and proj[i][j - 1][2] != len(proj[i][j - 1][1]):
                    if proj[i][j][1][p] == proj[i][j - 1][1][proj[i][j - 1][2]]:
                        continue
                go(i, proj[i][j][1][p])
                l = len(proj)
        i = i + 1


def print_proj():
    """
    打印项目集族与识别活前缀的DFA
    :return: None
    """
    with open('proj.txt', 'w', encoding='utf-8') as proj_file:
        proj_file.write('项目集族如下\n')
        for i in range(len(proj)):
            proj_file.write('I%d\n' % i)
            for j in range(len(proj[i])):
                p = proj[i][j][2]
                s = proj[i][j][1][:]
                s.insert(p, '.')
                proj_file.write('%s -> %s\n' % (proj[i][j][0], "".join(s)))
        proj_file.write('\n')
        proj_file.write('识别活前缀的DFA如下\n')
        proj_file.write('初始状态\t接收终结符\t到达的状态\t\n')
        for k in range(len(status_trans)):
            proj_file.write('I%d\t\t%s\t\tI%d\t\t\n' % (
                status_trans[k].status_init, status_trans[k].x, status_trans[k].status_trans))
            proj_file.write('\n')


def get_rule_pos(temp):
    """
    得到某条产生式在规则集LANGUAGE中的位置
    :param temp: 待查询的规则
    :return: 该规则在LANGUAGE中的位置
    """
    for i in range(len(LANGUAGE)):
        if LANGUAGE[i][0] == temp[0] and LANGUAGE[i][1] == temp[1]:
            return i


def create_slr1():
    global SLR_TABLE
    for i in range(len(status_trans)):
        if status_trans[i].x in VT:
            SLR_TABLE[status_trans[i].status_init][VT.index(status_trans[i].x)] = 's' + str(
                status_trans[i].status_trans)
        else:
            SLR_TABLE[status_trans[i].status_init][VN.index(status_trans[i].x) + len(VT) - 1] = status_trans[
                i].status_trans
    for j in range(len(proj)):
        for k in range(len(proj[j])):
            p = proj[j][k][2]
            if p == len(proj[j][k][1]) and proj[j][k][0] == VN[0]:
                SLR_TABLE[j][VT.index('#')] = 'acc'
            elif p == len(proj[j][k][1]):
                rule_pos = get_rule_pos(proj[j][k])
                for q in range(len(Follow[VN.index(proj[j][k][0])])):
                    if Follow[VN.index(proj[j][k][0])][q] in VT:
                        SLR_TABLE[j][VT.index(Follow[VN.index(proj[j][k][0])][q])] = 'r' + str(rule_pos)


def print_slr1():
    print('\t\t\t\t\t\t\SLR(1)分析表')
    print('\t\t状态\t\tACTION\t\tGOTO')
    row=[' ']
    print(VN)
    for vt in VT:
        row.append(vt)
    #     去掉初始符号
    for vn in VN[1:]:
        row.append(vn)
    tb = PrettyTable(row)
    for i,key in enumerate(SLR_TABLE):
        row = [i]
        for v in key:
            row.append(v)
        tb.add_row(row)

    with open('slr1.txt', 'w', encoding='utf-8') as slr1_file:
        slr1_file.write('SLR(1)分析表如下\n')
        slr1_file.write('状态\t\tACTION\t\t\t\t\tGOTO\t\t\n')
        slr1_file.write('\t')
        for i in range(len(VT)):
            slr1_file.write('%s\t' % VT[i])
        for j in range(1, len(VN)):
            slr1_file.write('%s\t' % VN[j])
        slr1_file.write('\n')
        for m in range(len(SLR_TABLE)):
            slr1_file.write('%d\t' % m)
            for n in range(len(SLR_TABLE[m])):
                slr1_file.write('%s\t' % SLR_TABLE[m][n])
            slr1_file.write('\n')


if __name__ == '__main__':
    start = time.time()
    gen_lang()
    identify_vt_and_vn()
    for j in range(len(VN)):
        First.append([])
        Follow.append([])
    for k in range(len(VN)):
        create_first_set(VN[k])
    for p in range(0, len(VN)):
        create_follow_set(VN[p])
    # gen_follow()
    print("FIRST集为：%s" % First)
    print("Follow集为：%s" % Follow)
    gen_proj()
    print_proj()
    SLR_TABLE = [[None for col in range(len(VT) + len(VN) - 1)] for row in range(len(proj))]
    create_slr1()
    print_slr1()
    # print_slr1()
    analy_slr1()
    end = time.time()
    print("花费时间：%s" % (end - start))
