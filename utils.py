## utility functions
##
def filter_list (F: list, A: list, check: bool = False) -> list:
    #assert len(F) <= len(A)
    R = [ ]
    for x in zip(F, A[:len(F)]):
        test, value = x[0], x[1]
        if test == 0 or test is False or test is None:
            pass
        else:
            R.append(value)
    if check:
        print (R)
    return R

##
def simplify (L: list, nested: bool = True) -> list:
    R = []
    for x in L:
        if nested:
            if isinstance(x, list):
                for y in simplify (x):
                    R.append(y)
            else:
                R.append(x)
        else:
            R.append(x)
    ##
    M = []
    return [ x for x in R if not x in M ]

##
def singlify_labels (data: object, labels: list, failure_mark: str = 'xxx', check: bool = False) -> list:
    R = []
    ## when data is Panda DataFrame
    try:
        for i, d in data.iterrows():
            if check:
                print("======")
                print(f"d:\n{d}")
            r = filter_list (list(d), labels)
            if check:
                print(f"r: {r}")
            try:
                v = r[0]
                R.append (v)
            except IndexError:
                R.append (failure_mark)
                print(f"failed on:\n{d}")
    ## other cases, typically NumPy ndarray
    except AttributeError:
        for d in list (data):
            r = filter_list (list(d), labels)
            try:
                v = r[0]
                R.append (v)
            except IndexError:
                R.append (failure_mark)
    ##
    return R

##

if __name__ == "__main__":

    a = [0,0,1]
    b = "abcde"
    filter_list(a, b)