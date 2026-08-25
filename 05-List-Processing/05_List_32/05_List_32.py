#
# 05_List_32: 05_QueueTicket 
#

q = list()
t = int(input())

number,time = [],[]
n_ticket,n_call = 0,0
sum_time = 0
n = 0

for k in range(t):
    c = input().split()
    if c[0] == 'reset':
        n_ticket = int(c[1])
        n_call = int(c[1])
        n_order = int(c[1])
    elif c[0] == 'new':
        print('ticket',n_ticket)
        number.append(n_ticket)
        time.append(int(c[1]))
        n_ticket += 1
    elif c[0] == 'next':
        print("call",n_call)
        n_call += 1
    elif c[0] == 'order':
        print('qtime',n_call-1,int(c[1]) - time[number.index(n_call-1)])
        sum_time += int(c[1]) - time[number.index(n_call-1)]
        n += 1
    elif c[0] == 'avg_qtime':
        print('avg_qtime',round(sum_time/n,4))
