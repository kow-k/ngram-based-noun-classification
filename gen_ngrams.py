#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a generator of skippy n-grams from a string or a list of segments.
developed by Kow Kuroda (kow.kuroda@gmail.com)
Creation: 2024/06/21
Modified:
2024/06/22: changed argument order to ensure compatibility with ngrams_skippy.py and ngrams.py
2024/06/28: renamed variable 'splitter' to 'sep' for compatibility; implemented max_distance
2024/11/24 fixed a serious bug that mishandles short input
2025/01/03 added skppy_ngram_size, gen_extended_skippy_ngrams
"""

## imports
import itertools

## functions
def segment (text: str, sep: str, check: bool):
    """
    converts a string to a list of segmenets with the specified separator.
    """
    try:
        L = text.split(sep)
    except ValueError:
        L = list(text)
    ## remove null strings generated by inefficient splitter
    L = [ x for x in L if len(x) > 0 ]
    if check:
        print(f"#L: {L}")
    #
    return L

##
def make_substrings (P, as_list: bool = False, check: bool = False):
    ## generate substrings
    Q = [ ]
    for p in P:
        if check:
            print(f"#p: {p}")
        q = [ ]
        ## irrelevant cases
        if len(p) < 1:
            pass
        ## cases where len(p) > 1
        elif len(p) >= 2:
            for i in range(len(p)):
                try:
                    sec = p[i:i+2]
                    if check:
                        print(f"#sec: {sec}")
                    pos, next_pos = sec[0], sec[1]
                except IndexError:
                    pos, next_pos = p[i], p[i]
                gap = (next_pos - pos)
                if check:
                    print(f"#pos: {pos}; next_pos: {next_pos}")
                    print(f"#gap: {gap}")
                seg = S[pos]
                if gap > 1:
                    if pos == 0:
                        q.append (seg)
                        q.append (missing_mark)
                    elif pos == end_pos:
                        q.append (seg)
                    else:
                        q.append (missing_mark)
                        q.append (seg)
                        q.append (missing_mark)
                elif gap == 1:
                    if pos == 0:
                        q.append (seg)
                    elif pos == end_pos:
                        q.append (seg)
                    else:
                        q.append (missing_mark)
                        q.append (seg)
                else:
                    if pos == 0:
                        q.append (seg)
                    elif pos == end_pos:
                        q.append (seg)
                    else:
                        q.append (seg)
                        q.append (missing_mark)
        ## cases where len(p) ==  1
        else:
            for pos in p:
                if check:
                    print(f"#pos: {pos}")
                seg = S[pos]
                if   ( pos == 0 ):
                    q.append(seg)
                    q.append(missing_mark)
                elif ( pos == (S_len - 1)):
                    q.append(missing_mark)
                    q.append(seg)
                else:
                    q.append(missing_mark)
                    q.append(seg)
                    q.append(missing_mark)
        ## singlify repeated missing_marks
        q2 = []
        last = ""
        for x in q:
            if x != last:
                q2.append(x)
            last = x
        q = q2
        ## update
        Q.append(q)
    ## return result
    if as_list: ## result is a list of unstrung lists
        return Q
    else: ## result is a list of strings
        return [ sep.join(q) for q in Q ]

##
def gen_ngrams (S: list, n: int, sep = " ", as_list = False, check = False):
    """
    takes a list S of segments and returns a list R of n-grams out of them.
    """
    if check:
        print(f"#S: {S}")
    ##
    assert n > 0
    if len(S) <= n:
        if as_list:
            return S
        else:
            return [ sep.join(S) ]
    #
    R = [ ]
    for i, x in enumerate(S):
        try:
            y = S[ i:i + n] # get an n-gram
            if len(y) == n: # check its length
                R.append(y)
        except IndexError:
            pass
    ##
    if as_list:
        return R
    return [ sep.join(r) for r in R ]

##
def gen_ngrams_from_str (text: str, n: int, sep = " ", as_list = False, check = False):
    """
    takes a string and returns a list of n-grams out of segments generated using the separator
    """
    S = segment (text, sep, check)
    if check:
        print(f"#S: {S}")
    ##
    assert n > 0
    if len (S) <= n:
        if as_list:
            return S
        else:
            return text
    ##
    R = [ ]
    for i, x in enumerate(S):
        try:
            y = S[ i:i + n] # get an n-gram
            if len(y) == n: # check its length
                R.append(y)
        except IndexError:
            pass
    ##
    if as_list:
        return R
    return [ sep.join(r) for r in R ]

##
def gen_skippy_ngrams (S: list, n: int, max_distance = None, sep: str = " ", missing_mark: str = "…", as_list: bool = False, check: bool = False):
    """
    takes a list of segments and returns a list of skippy n-grams out of them
    """
    ##
    assert n > 0
    if check:
        print(f"#S: {S}")
    #
    if len(S) <= n:
        if as_list:
            return S
        else:
            return [ sep.join(S) ]
    ## generate target index list
    S_len = len(S)
    R = range(S_len)
    ##P = itertools.combinations(I, r = n) # turned out to be offensive
    ## [ x for x in ...] is necessary as in the following
    ## implementation of restriction by max gap distance
    if max_distance is None: ## max_distance-free
        P = [ x for x in itertools.combinations(R, r = n) if max(x) <= S_len ]
    else: ## max_distance implementation
        Rx = [[ x for x in itertools.combinations(range(i, i + max_distance + 1), n) if max(x) < len(S) ] for i in R ]
        ## flatten U
        P = [ ]
        for rx in Rx:
            P.extend(rx)
    ##
    if check:
        print(f"#P: {P}")
    ## generate substrings
    Q = [ ]
    for p in P:
        q = [ ]
        for j in range(len(p)):
            i = p[j]
            seg = S[i]
            if i == 0:
                q.append(seg)
                last_i = 0
            else:
                if last_i + 1 == i:
                    q.append(seg)
                else:
                    q.append(missing_mark)
                    q.append(seg)
                last_i = i
        #
        Q.append(q)
    ## return result
    if as_list: ## result is a list of unstrung lists
        return Q
    else: ## result is a list of strings
        R = [ ]
        for q in Q:
            ## remove the intial missing_mark wrongly generated
            if q[0] == missing_mark:
                R.append(q[1:])
            else:
                R.append(q)
        #
        return ([ sep.join(r) for r in R ])

##
def gen_extended_skippy_ngrams (S: list, n: int, max_distance = None, sep: str = " ", missing_mark: str = "…", as_list: bool = False, check: bool = False):
    """
    takes a list of segments and returns a list of skippy n-grams out of them
    """
    ##
    assert n > 0
    if check:
        print(f"#S: {S}")
    #
    if len(S) <= n:
        if as_list:
            return S
        else:
            return [ sep.join(S) ]
    ## generate target index list
    S_len = len(S)
    end_pos = (S_len - 1)
    if check:
        print(f"S_len: {S_len}")
    ##
    R = range(S_len)
    ##P = itertools.combinations(I, r = n) # turned out to be offensive
    ## [ x for x in ...] is necessary as in the following
    ## implementation of restriction by max gap distance
    if max_distance is None: ## max_distance-free
        P = [ x for x in itertools.combinations(R, r = n) if max(x) <= S_len ]
    else: ## max_distance implementation
        Rx = [[ x for x in itertools.combinations(range(i, i + max_distance + 1), n) if max(x) < len(S) ] for i in R ]
        ## flatten U
        P = [ ]
        for rx in Rx:
            P.extend(rx)
    ##
    if check:
        print(f"#P: {P}")
    ## generate substrings
    Q = [ ]
    for p in P:
        if check:
            print(f"#p: {p}")
        q = [ ]
        ## irrelevant cases
        if len(p) < 1:
            pass
        ## cases where len(p) > 1
        elif len(p) >= 2:
            for i in range(len(p)):
                try:
                    sec = p[i:i+2]
                    if check:
                        print(f"#sec: {sec}")
                    pos, next_pos = sec[0], sec[1]
                except IndexError:
                    pos, next_pos = p[i], p[i]
                gap = (next_pos - pos)
                if check:
                    print(f"#pos: {pos}; next_pos: {next_pos}")
                    print(f"#gap: {gap}")
                seg = S[pos]
                if gap > 1:
                    if pos == 0:
                        q.append (seg)
                        q.append (missing_mark)
                    elif pos == end_pos:
                        q.append (seg)
                    else:
                        q.append (missing_mark)
                        q.append (seg)
                        q.append (missing_mark)
                elif gap == 1:
                    if pos == 0:
                        q.append (seg)
                    elif pos == end_pos:
                        q.append (seg)
                    else:
                        q.append (missing_mark)
                        q.append (seg)
                else:
                    if pos == 0:
                        q.append (seg)
                    elif pos == end_pos:
                        q.append (seg)
                    else:
                        q.append (seg)
                        q.append (missing_mark)
        ## cases where len(p) ==  1
        else:
            for pos in p:
                if check:
                    print(f"#pos: {pos}")
                seg = S[pos]
                if   ( pos == 0 ):
                    q.append(seg)
                    q.append(missing_mark)
                elif ( pos == (S_len - 1)):
                    q.append(missing_mark)
                    q.append(seg)
                else:
                    q.append(missing_mark)
                    q.append(seg)
                    q.append(missing_mark)
        ## singlify repeated missing_marks
        q2 = []
        last = ""
        for x in q:
            if x != last:
                q2.append(x)
            last = x
        q = q2
        ## update
        Q.append(q)
    ## return result
    if as_list: ## result is a list of unstrung lists
        return Q
    else: ## result is a list of strings
        return [ sep.join(q) for q in Q ]

## alias
gen_ext_skippy_ngrams = gen_extended_skippy_ngrams

##
def skippy_ngram_size (s: str, gap_mark: str = "…") -> int:
    "a given skippy n-gram, returns the number of substances in it"
    return len([ x for x in s if str(x) != gap_mark ])

## alias
sk_ngram_size = skippy_ngram_size

##
def gen_skippy_ngrams_from_str (text: str, n: int, sep: str = " ", missing_mark: str = "…", max_distance = None, as_list: bool = False, check: bool = False):
    """
    takes a string and returns a list of skippy n-grams out of segments generated the using separator
    """
    assert n > 0
    ## split into segments
    S = segment(text, sep, check)
    if check:
        print(f"#S: {S}")
    if len(S) <= n:
        if as_list:
            return S
        else:
            return text
    ## generate target index list
    I = range(len(S))
    ##
    if max_distance is None:
        ##P = itertools.combinations(I, r = n) # turned out to be offensive
        ## [ x for x in ...] is necessary as in the following
        #P = [ x for x in itertools.combinations(I, r = n) ]
        P = list(itertools.combinations(I, r = n))  # suggested by Pylint
    else:
        Rx = [[ x for x in itertools.combinations(range(i, i + max_distance), n) if max(x) < len(S) ] for i in I ]
        ## flatten U
        P = [ ]
        for rx in Rx:
            P.extend(rx)
    if check:
        print(f"#P: {P}")
    ## generate substrings
    return make_substrings (P)

##
def main():
    # test 1
    text1 = "abcdefghij"
    print(f"input: '{text1}'")
    print(gen_skippy_ngrams_from_str (text1, 3, sep = " ", check = False))
    # test 2
    text2 = "abc   def  gh ijk lmn   op"
    print(f"input: '{text2}'")
    print(gen_skippy_ngrams_from_str (text2, 3, sep = " ", as_list = False, check = False))
    # test 3
    text3 = "abde"
    print(f"input: '{text3}'")
    print(gen_skippy_ngrams_from_str (text3, 4, sep = " ", check = False))
    # test 4
    print(f"input: '{text3}'")
    print(gen_skippy_ngrams_from_str (text3, 5, sep = " ", check = False))

    ## test 5
    print(f"input: '{text1}'")
    print(gen_ngrams (text1, 5, sep = "", check = False))
    ## test 6
    print(f"input: '{text2}'")
    print(gen_ngrams (text2, 3, sep ="", check = False))

## tests
if __name__ == "__main__":
    main()


### end of script