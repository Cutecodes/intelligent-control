import numpy as np 
import matplotlib.pyplot as plt
from PID import PID

class InvertPendulum(object):
    def __init__(self,y=0.0,dy=0.0,au=0.0,sum_e=0.0,controller=None,r=None,u=None):
        '''
        初始化状态参数
        y:倒立摆偏移角度
        dy:倒立摆偏移角度的导数
        au:控制器/干扰力的影响
        e:偏差
        sum_e：偏差积分
        controller(de,e,sum_e):控制器输出
        r(t):参考
        u(t):干扰
        '''
        self.status = np.array([y,dy,au,r(0)-y,sum_e])
        self.t = 0
        self.controller = controller
        self.r = r 
        self.u = u

    def derivative(self,x,r,u,t,h):
        '''
        x:状态列表 y,dy,au,e,sum_e
        r:参考量（函数）
        u:干扰外力（函数）
        返回值
        y:状态的导数
        '''
        y = x.copy()
        y[0] = x[1]
        y[1] = (
                (9.8*np.sin(x[0])+
                np.cos(x[0])*((-x[2]-0.25*x[1]*x[1]*np.sin(x[0]))/1.5)
                )/
                0.5*(4.0/3.0-1.0/3.0*np.cos(x[0])**2)
                )
        y[2] = -100*x[2]+100*(self.controller((r(t+h)-r(t))/h-x[1],x[3],x[4])+u(t))
        y[3] = (r(t+h)-r(t))/h-x[1]
        y[4] = x[3]
        return y

    def Euler(self,h):
        self.status = self.status + h * self.derivative(self.status,self.r,self.u,self.t,h)

    def Runge_Kutta(self,h):
        #the fourth-order Runge-Kutta method 四阶龙格库塔法
        k1 = h * self.derivative(self.status,self.r,self.u,self.t,h)
        k2 = h * self.derivative(self.status+k1/2,self.r,self.u,self.t+h/2,h)
        k3 = h * self.derivative(self.status+k2/2,self.r,self.u,self.t+h/2,h)
        k4 = h * self.derivative(self.status+k3,self.r,self.u,self.t+h,h)
        self.status = self.status + (k1+2*k2+2*k3+k4)/6
    def step(self,tick=0.0001):
        #self.Euler(tick)
        self.Runge_Kutta(tick)
        self.t = self.t +tick
        
        if self.status[0]>2*np.pi:
            self.status[0]=self.status[0]-2*np.pi
        elif self.status[0]<-2*np.pi:
            self.status[0]=self.status[0]+2*np.pi
        return self.status
def r(t):
    return 0.0
def u(t):
    #if t>=1.99 and t<=2.01:
        #return 600
    #else:
        #return 0.0
    return 0.0
    
def controller(x,y,z):
    return 0.0
def main():
    h = 0.0001
    pid_controller = PID(-150,-100.0,-30.0)
    ip = InvertPendulum(y=0.1,controller=controller,r=r,u=u)
    result = []
    for i in range(100000):
        result.append(ip.step(h)[0])
        
    x=np.linspace(0,10,100000)
    plt.plot(x,result)
    plt.show()

if __name__ == '__main__':
    main()
