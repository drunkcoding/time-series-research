
def partition(list_t, step_t, num_wins):
    len_t = len(list_t)
    a = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
    list_t.reverse()
    b = [list_t[i:i+step_t] for i in range(0,len_t,step_t)]
    if num_wins*step_t != len_t:
        a.pop()
        b.pop()
    return a+b
