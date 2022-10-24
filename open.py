import numpy as np
test=[]
lst = [13, 4, 20, 15, 6, 20, 20]

lst = np.array(lst)

result = np.where(lst == 20)
for i in result[0]:
    test.append(i)
print(type(test))