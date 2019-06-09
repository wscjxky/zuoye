action = {i:[ 0 for j in range(0, len(analyze_table))] for i in VT}
goto =  {i:[-1 for j in range(0, len(analyze_table))] for i in VN}
for i in range(0, len(analyze_table)) :
    map = analyze_table[i][0]
    for j in analyze_table[i][1:]:
        #可归约项目
        if j[0] == generators[j[1]][-1] :
            #对任何终结符或'#'用产生式进行归约
            if j[1] == 0 and j[0] == generators[0][-1] :
                action['#'][i] = 'acc'
            else :
                for key in action:
                    if key in follow[generators[j[1]][0]]:
                        action[key][i] = -1 * j[1];
        elif generators[j[1]][j[0]] in VT:
            #移进项目
            action[generators[j[1]][j[0]]][i] = map[0]
            map = map[1:]
        else :
            goto[generators[j[1]][j[0]]][i] = map[0]
            map = map[1:]

print('  ',end='')
[print('%5s' % i, end=' ') for i in VT]
print()
for i in range(len(analyze_table)) :
    print('%2s' % i, end='')
    for j in VT:
        print('%5s' % action[j][i], end = ' ')
    print()

