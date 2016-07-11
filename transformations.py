#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import math
from numpy import matrix


def kreuz(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print("wrong input: ", v1, v2)
        return 0
    
    return ["(" + v1[1] + ") * (" + v2[2] + ") + (" + v1[2] + ") * (" + v2[1] + ")" ,
            "(" + v1[0] + ") * (" + v2[2] + ") - (" + v1[2] + ") * (" + v2[0] + ")" ,
            "(" + v1[0] + ") * (" + v2[1] + ") + (" + v1[1] + ") * (" + v2[0] + ")"]
    
def mult(m1,m2):
    # only mult lists of lists, no np.matricces!
    ret= [['0' for j in range(len(m2[0]))] for i in range(len(m1))]

    if len(m1[0]) != len(m2):   # assumption: len(m[0]) == len(m[i])
        print("matricces cannot be multiplied, wrong matrix size: ", len(m1[0]), len(m2))
        return 0
    
    for i in range(len(m1)):
        for k in range(len(m1[i])):
            for j in range(len(m2[k])):
                if m1[i][k] != '0' and m2[k][j] != '0':
                    if ret[i][j] == '0':
                        ret[i][j] = ''
                    else:
                        ret[i][j] += ' + '
                    
                    s = ''
                    if m1[i][k] != '1':
                        s += m1[i][k]
                    if m2[k][j] != '1':
                        if s != '':
                            s += '*'
                        s += m2[k][j]
                    
                    if s == '':
                        s = '1'
                    ret[i][j] += s
                    
    return ret

def minus(v1, v2):
    if len(v1) != len(v2):
        print("Minus not possible, got vectors with different lengthhs: ", v1, v2)
        return 0
    
    return ["(" + v1[i] + ") - (" + v2[i] + ")" for i in range(len(v1))]

def split_brackets(term):
    terms = []
    o = 0
    s = 0
    e = 0
    function = []
    for c in term:
        e +=1
        if c == '(':
            o += 1
            if o == 1:
                if len(terms) > 0:
                    terms.append(term[s:e-1])
                    function.append(True)
                s = e
                
        if c == ')':
            o -= 1
            if o == 0:
                terms.append(term[s:e-1])
                function.append(False)
                s = e
                
    return terms, function

def calc(st, q, l):
    if "(" in st:
        terms, function = split_brackets(st)
        
        parts = []
        part = calc(terms[0],q,l)
        for i in range(1, len(terms)): # first multiplication
            if function[i] and "*" in terms[i]:
                part *= calc(terms[i+1],q,l)
            elif function[i]:
                parts.append(part)
                part = calc(terms[i+1],q,l)
                parts.append(terms[i])
        parts.append(part)
                
        val = parts[0]
        for i in range(1, len(parts)):
            if type(parts[i]) == str:
                if "+" in parts[i]:
                    val += parts[i+1]
                elif "-" in parts[i]:
                    val -= parts[i+1]
                else:
                    print("Unknown function: ", parts[i])
                    
        return val
    else:
        return calc_string(st, q, l)

def calc_string(st, q, l):
    if type(st) == list and len(st) == 1:
        st = st[0]
    elif type(st) == list:
        print(st, " is list")
    
    el = st.split("+")
    result = 0
    
    for i in range(len(el)):
        el[i] = el[i].split("*")
        tmp = 1
        for j in range(len(el[i])):
            if "l" in el[i][j]:
                tmp *= calc_length(el[i][j], l)
            else:
                tmp *= calc_angle(el[i][j], q)
        result += tmp
    
    #print(st , " = " , result)
    return result

def calc_length(st, l):
    el = st.split("/")
    
    ind = -1
    for i in range(len(l)):
        if str(i) in el[0]:
            ind = i
            break
    
    if ind == -1:
        print("[2]: ", st, len(l))
    
    result = l[ind]
    
    if len(el) > 1:
        print("debug: ", el[1], int(el[1]))
        result /= int(el[1])
    
    return result

def calc_angle(st, q):
    result = 1
    
    if "-" in st:
        result *= -1
    
    ind = -1
    for i in range(len(q)):
        if str(i) in st:
            ind = i
            break
    
    if ind == -1:
        print("[0]: ", st, len(q))
    
    if "c" in st:
        if q[ind] == abs(math.pi/2):
            result *= 0
        else:
            result *= math.cos(q[ind])
    elif "s" in st:
        result *= math.sin(q[ind])
    else:
        if "-1" in st:
            result *= -1
        elif "1" in st:
            pass
        elif "0" in st:
            result *= 0
        else:
            print("[1]: ", st)

    return result
     

class transformations():
    
    def __init__(self):
        self.t = []
        self.t0i = []
    
    def kuka_lbr_iiwa_14(self):
        self.t0i = []
        self.t = []
        self.t.append([['c0', '0', 's0', '0'], ['s0', '0', '-c0', '0'], ['0', '1', '0', 'l0'], ['0', '0', '0', '1']])
        self.t.append([['c1', '0', '-s1', '0'], ['s1', '0', 'c1', '0'], ['0', '-1', '0', '0'], ['0', '0', '0', '1']])
        self.t.append([['c2', '0', 's2', '0'], ['s2', '0', '-c2', '0'], ['0', '1', '0', 'l1'], ['0', '0', '0', '1']])
        self.t.append([['c3', '0', '-s3', '0'], ['s3', '0', 'c3', '0'], ['0', '-1', '0', '0'], ['0', '0', '0', '1']])
        self.t.append([['c4', '0', 's4', '0'], ['s4', '0', '-c4', '0'], ['0', '1', '0', 'l2'], ['0', '0', '0', '1']])
        self.t.append([['c5', '0', '-s5', '0'], ['s5', '0', 'c5', '0'], ['0', '-1', '0', '0'], ['0', '0', '0', '1']])
         
    def transform0i(self):
        if len(self.t0i) != 0:
            return self.t0i
        
        
        self.t0i.append(self.__transform(0, 0))
        self.t0i.append(self.__transform(self.t0i[-1], 1))
        self.t0i.append(self.__transform(self.t0i[-1], 2))
        self.t0i.append(self.__transform(self.t0i[-1], 3))
        self.t0i.append(self.__transform(self.t0i[-1], 4))
        self.t0i.append(self.__transform(self.t0i[-1], 5))
    
        return self.t0i
    
    def __transform(self, t0i, ind_next):
        if len(self.t) < ind_next:
            print("transformation matricces not defined for index: ", ind_next)
            return 0
        
        if ind_next == 0:
            return self.t[0]
        
        return mult(t0i, self.t[ind_next])
    
    def rotation(self,q):
        return [self.__extract_rotation(self.t0i[i],q) for i in range(0,6)]
    
    def __extract_rotation(self, m, q):
        cropped = [a[0:3] for a in m[0:3]]
        return matrix([[calc(element,q,0) for element in row] for row in cropped])

    def calculate_jacobians(self):
        return [jacobian(self.transform0i(), i) for i in range(6)]

    def coms(self, q,l):
        return [self.__coms(q,l,i) for i in range(len(self.t0i))]

    def __coms(self, q, l, ind):
        if ind == 5:
            return [[calc(st,q,l) for st in row] for row in mult(self.t0i[5], [[str(e)] for e in [0,0,0,1]])[0:3]]
    
        if ind % 2 == 0:
            # dreh -> next: kipp
            local_point = [0,-0.5,0, 1]
        else:
            # kipp -> next: dreh
            local_point = [0,0,-0.5, 1]
        
        if ind == 0:
            length_index = 0
        elif ind < 3:
            length_index = 1
        elif ind < 5:
            length_index = 2
        else:
            length_index = 3
        
        local_point = [p * l[length_index] for p in local_point]
        # local_point[3] = 1    #not important, will be refused anyway

        return [[calc(st,q,l) for st in row] for row in mult(self.t0i[ind+1], [[str(e)] for e in local_point])[0:3]]
        
class jacobian():
    
    def __init__(self, transformation_matricces, index):
        self.j = []

        p = [transformation_matricces[index][i][3] for i in range(3)]
        
        for t in transformation_matricces:
            self.j.append(self.__column([t[i][2] for i in range(3)],
                                        [t[i][3] for i in range(3)],
                                        p))
    
    def __column(self, z_i, p_i, p):
        jp = kreuz(z_i, minus(p, p_i))
        jo = z_i
        
        return [jp[0], jp[1], jp[2], jo[0], jo[1], jo[2]]

    def get(self, q, l, jac_type=0):
        # 0: all, 1: jp, 2: jo
        
        if jac_type == 0:
            r = [0,6]
        elif jac_type == 1:
            r = [0,3]
        else:
            r = [3,6]

        return matrix([ [calc(self.j[i][j], q,l) for j in range(len(self.j[i])) ] for i in range(r[0],r[1])])


if __name__ == '__main__':
    t = transformations()
    t.kuka_lbr_iiwa_14()
    
    j = jacobian(t.transform0i(), 5)

    print(j.get([0,math.pi/2,0,0,0,0],[1,1,1,1]))
    
    #print(t.rotation())
    
            