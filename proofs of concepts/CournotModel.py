# p = 14 - Q 
# Q = q_1 + q_2
# C = c*q_i

q_1 = int(input('input how much to produce: '))
q_2 = 5

Q = q_1 + q_2
p = max(14 - Q, 0)
c = 2

profit_1 = q_1*p-q_1*c
profit_2 = q_2*p-q_2*c

print(profit_1,profit_2)