#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame
import random
import math

from force import force_calculator

def t(p):
    return (int(p[0]*50 + 10), int(-p[1]*300 + 470))
    
    
class draw():
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.screen.fill((255,255,255))
    
        black = (0,0,0)
        pygame.draw.lines(self.screen, black, False, [t((0,0)),t((10,0))], 2)
        pygame.draw.lines(self.screen, black, False, [t((0,0)),t((0,1))], 2)
     
    def insert_point(self, m_u, v):
        try:
            black = (0,0,0)
            pygame.draw.circle(self.screen, black, t((m_u,v)), 1)
        except:
            print("probably sth to large")

    def update(self):
        pygame.display.update()

def rand_angle():
    return [random.random() * 2*math.pi - math.pi for i in range(6)]

def rand_mov():
    return [random.random() * 2 - 1 for i in range(3)]

if __name__ == '__main__':
    d = draw()
    
    fc = force_calculator(1, [1,1,1,1,1,1], [1,1,1,1])

    while True:
        v, m_u = fc.calc_max_speed(rand_angle(), rand_mov())
        d.insert_point(m_u[0,0], v)
        
        d.update()
