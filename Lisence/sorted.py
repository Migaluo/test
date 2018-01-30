
def by_name(t):
    return t[0]
def by_score(t):
    return t[1]
L=[('Adam', 92), ('Bart', 66), ('Lisa', 88)]
print(sorted(L,key=by_name))
print(sorted(L,key=by_score,reverse=True))   #按字符串大小以及分数排列