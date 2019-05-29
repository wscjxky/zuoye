'''
@author: xky
'''
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

FIRST_VT = {}
LAST_VT = {}
# 终结符集合
VT = set()
VN = set()
LANGUAGE = {}
TABLE = {}
START = ''
# eq 等于
# lt 大于
# st 小于
EQ = ' = '
LT = ' > '
ST = ' < '


# 申明全局变量用于修改。
def gen_lang():
    global LANGUAGE
    global VT
    global VN
    global START
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
                if v >= "A" and v <= "Z":
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


def init_set():
    m_set = {}
    for vn in VN:
        for vt in VT:
            m_set[vn + ',' + vt] = False
    return m_set


def insert_set(m_set, m_stack, vn, vt):
    if not m_set[vn + ',' + vt]:
        m_set[vn + ',' + vt] = True
        # 加入栈中便于更新
        m_stack.append(vn + ',' + vt)
    return m_set, m_stack


def print_set(m_set):
    head = [i for i in VT]
    head.insert(0, '  ')
    table = PrettyTable(head)
    for key in VN:
        line = []
        line.append(key)
        for v in VT:
            line.append(m_set[key + ',' + v])
        table.add_row(line)
    print(table)


def gen_firstvt():
    global FIRST_VT
    stack = []
    FIRST_VT = init_set()

    # 遍历所有产生式
    for key in LANGUAGE:
        for value in LANGUAGE[key]:
            # 如果有P->a..那么就把FIRST_VT[p,a]变为true
            if value[0] in VT:
                FIRST_VT, stack = insert_set(FIRST_VT, stack, key, value[0])
            # 如果有P->Qa..那么就把FIRST_VT[p,a]变为true
            if len(value) > 1:
                if value[0] in VN and value[1] in VT:
                    FIRST_VT, stack = insert_set(FIRST_VT, stack, key, value[1])

    # 遍历stack,因为当a属于firstvt(Q)中且P->Q，那么a也属于firstvt(P)中
    while stack:
        stack_p = stack.pop()
        vn = stack_p[0]
        vt = stack_p[2]
        for key in LANGUAGE:
            for value in LANGUAGE[key]:
                if value[0] == vn:
                    FIRST_VT, stack = insert_set(FIRST_VT, stack, key, vt)
    print("                FIRST_VT:")
    print_set(FIRST_VT)


def gen_lastvt():
    global LAST_VT
    stack = []
    # 初始化集合
    LAST_VT = init_set()
    # 遍历所有产生式
    for key in LANGUAGE:
        for value in LANGUAGE[key]:
            # 如果有P->...a那么就把FIRST_VT[p,a]变为true
            if value[-1] in VT:
                LAST_VT, stack = insert_set(LAST_VT, stack, key, value[-1])
            # 如果有P->aQ..那么就把FIRST_VT[p,a]变为true
            if len(value) > 1:
                if value[-1] in VN and value[-2] in VT:
                    LAST_VT, stack = insert_set(LAST_VT, stack, key, value[-2])

    # 遍历stack,因为当a属于lastvt(Q)中且P->...Q，那么a也属于lastvt(P)中
    while stack:
        stack_p = stack.pop()
        vn = stack_p[0]
        vt = stack_p[2]
        for key in LANGUAGE:
            for value in LANGUAGE[key]:
                if value[-1] == vn:
                    LAST_VT, stack = insert_set(LAST_VT, stack, key, vt)
    print("                LAST_VT:")
    print_set(LAST_VT)


# 把firstvt和lastvt转换成fisrt(P)的数组形式： first[P]=[+,-]
def tran_set(m_set):
    m_arr = {}
    for k in VN:
        m_arr[k] = []
    for key in m_set:
        vn = key[0]
        vt = key[2]
        if m_set[key]:
            m_arr[vn].append(vt)
    return m_arr


def print_table():
    head = [i for i in VT]
    head.insert(0, '  ')
    table = PrettyTable(head)
    for vt in VT:
        line = [vt]
        for t_vt in VT:
            try:
                line.append(TABLE[vt + ',' + t_vt])
            # 没有这个就空着
            except:
                line.append(' ')
                pass
        table.add_row(line)
    print(table)
    # for index, key in enumerate(TABLE):
    #     left = key[0]
    #     right = key[2]
    #     compare = TABLE[key]
    #     line += left + " " + compare + " " + right + ' | '
    #     if index % 4 == 0 and index != 0:
    #         print(line)
    #         line = ''


def gen_table():
    global TABLE
    # 遍历所有产生式
    # 添加文法# -> #E#
    VT.add('#')
    LANGUAGE['#'] = ['#' + START + '#']
    for key in LANGUAGE:
        for value in LANGUAGE[key]:
            for index, v in enumerate(value[:-1]):
                # i+1个元素
                next_value = value[index + 1]
                count = len(value)
                if count > 1:
                    # 如果前后都为终结符，则优先等级相等。 P->ab
                    if v in VT and next_value in VT:
                        TABLE[v + ',' + next_value] = EQ
                # 如果前后都为终结符，则优先等级相等。 P->aQb
                if index < count - 2:
                    nn_value = value[index + 2]
                    if v in VT and nn_value in VT and next_value in VN:
                        TABLE[v + ',' + nn_value] = EQ
                # 如果 P->aQ 遍历firstvt集合为b，a<b
                if v in VT and next_value in VN:
                    for f_vt in FIRST_VT[next_value]:
                        TABLE[v + ',' + f_vt] = ST
                # 如果 P->Qa 遍历firstvt集合为b，a<b
                if v in VN and next_value in VT:
                    for l_vt in LAST_VT[v]:
                        TABLE[l_vt + ',' + next_value] = LT
    print("                算符优先表")
    print_table()


def analyse():
    print("%32s" % '分析表情况')
    head = ["当前步骤", "符号栈", "关系", "当前符号", "输入串"]
    table = PrettyTable(head)
    in_str = 'i+i*i#'
    in_str = 'i+i*ii#'
    ori_str = in_str
    stack = ['#']
    k = 1 - 1
    n = 0
    while True:
        # 读入下一个字符
        # 如果栈中第一个是终结符a，就取第一个a，不然取第二个Qa
        if stack[-1] in VT:
            j = k
        else:
            j = k - 1
        # 当前字符和栈顶比较大小
        value = in_str[0]
        # 如果优先顺序表中为空，则跳过
        try:
            compare = TABLE[stack[j] + "," + value]
        except:
            compare = ''
        # 如果栈顶>当前输入字符，就把指针j往下走
        if compare == LT:
            while True:
                temp_q = stack[j]
                if stack[j - 1] in VT:
                    j -= 1
                else:
                    j -= 2
                if TABLE[stack[j] + "," + temp_q] == ST:
                    break
            # 如果找到了<i>就进行规约i
            k = j + 1
            stack[k] = 'N'
            line = [n, stack[:j + 1], compare, value, in_str]
            table.add_row(line)
            n += 1
            continue
        # 如果栈顶<当前输入字符
        elif compare == ST:
            k += 1
            try:
                stack[k] = value
            except:
                stack.append(value)
                stack[k] = value
            line = [n, stack[:j + 1], compare, value, in_str]
            temp_line = line
            table.add_row(temp_line)
            in_str = in_str[1:]
            n += 1
            continue
        elif compare == EQ:
            if stack[j] == '#':
                print(table)
                print('接受字符串:%s ，规约成功！' % ori_str)
                break
            else:
                k += 1
                stack[k] = in_str[0]
                line = [n, stack, compare, value, in_str]
                table.add_row(line)
                n += 1
                in_str = in_str[1:]
                continue
        else:
            print(table)
            print('接受字符串失败，错误字符串:%s ,错误字符：%s，错误位置：%s！' % (ori_str, in_str[0], len(ori_str)-len(in_str)))
            # continue
            exit()


gen_lang()
gen_firstvt()
gen_lastvt()
FIRST_VT = tran_set(FIRST_VT)
LAST_VT = tran_set(LAST_VT)
gen_table()
analyse()
