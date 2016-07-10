#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import transformations
import math
from numpy import matrix

def as_matrix(vec):    
    if type(vec[0]) == list:
        return matrix([[element for element in row] for row in vec])
    else:
        return matrix([[element] for element in vec])

def dist(np_vec):
    tmp = 0
    for e in np_vec:
        if len(e) > 1:
            print("Something unexpected with this vector: ", e, np_vec)
        tmp += e[0]**2
    
    return math.sqrt(tmp)
    
def norm(vec):
    l = math.sqrt(sum([v**2 for v in vec]))
    
    return [v/l for v in vec]
        
class force_calculator():
    
    def __init__(self, max_force, masses):
        self.t = transformations.transformations()
        self.t.kuka_lbr_iiwa_14()
        self.j = self.t.calculate_jacobians()
        
        self.masses = masses
        self.max_force = max_force
        self.coms = self.__def_coms()
    
    def __def_coms(self):
        return [as_matrix([0,0,0]) for i in range(0,6)]
    
    def calc_max_speed(self, q,l, direction):
        
        u = as_matrix(norm(direction))        
        
        mass_matrix = self.__calc_mass_matrix(self.masses,
                                              self.__calc_inertia(self.masses, self.coms),
                                              [self.j[i].get(q,l,1) for i in range(0,6)],
                                              [self.j[i].get(q,l,2) for i in range(0,6)],
                                              self.t.rotation(q))
        
        forceful_mass = u.I * self.__lambda_v(mass_matrix, self.j[5].get(q,l)) * u.I.T
        
        return math.sqrt(2*self.max_force / forceful_mass)
    
    def __lambda_v(self, mass_matrix, J ):
        great_lambda = J.I.T * mass_matrix * J.I

        return great_lambda[0:3,0:3]
    
    def __calc_inertia(self, masses, coms):
        inertia = [0.5 * masses[0] * dist(coms[0])**2]
        for i in range(1,len(masses)):
            inertia.append(0.5 * masses[i] * dist(coms[i])**2 + inertia[i-1])
        
        return inertia

    
    def __calc_mass_matrix(self, m, I, JP, JO, R):
        return sum([m[i]*JP[i].T*JP[i] + JO[i].T*R[i]*I[i]*R[i].T*JO[i] for i in range(len(m))])
    
    
if __name__ == '__main__':
    fc = force_calculator(1, [1,1,1,1,1,1])
    print(fc.calc_max_speed([0,0,0,0,0,0], [1,1,1,1], [-1,-1,-1]))
    