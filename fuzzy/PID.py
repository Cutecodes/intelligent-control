import numpy as np 
import matplotlib.pyplot as plt


class PID(object):
    def __init__(self, kp,ki,kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
    def __call__(self,de,e,sum_e):
    	return self.kp*e+self.ki*sum_e+self.kd*de
		

