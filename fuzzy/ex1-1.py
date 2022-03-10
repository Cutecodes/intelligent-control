from Inverted_pendulum import InvertPendulum
from PID import PID
import matplotlib.pyplot as plt

import numpy as np 

def r(t):
    #参考量
    return 0.0

def U(t):
    #扰动量    
    return 0.0

def main():
    #时间间隔
    h = 0.0001
    #创建PID控制器 PID（Kp,Ki,Kd）
    pid_controller = PID(-150,0.0,-30.0)
    ip = InvertPendulum(y=0.1,controller=pid_controller,r=r,u=U)
    y = []
    u = []
    for i in range(100000):
        # 模拟10s
        status = ip.step(h)
        y.append(status[0])
        u.append(pid_controller((r(i*h+h)-r(i*h))/h-status[1],status[3],status[4]))

    t = np.linspace(0,10,100000)
    plt.subplot(211)
    plt.title('pid_y')
    plt.plot(t,y)
    plt.subplot(212)
    plt.title('pid_u')
    plt.plot(t,u)
    plt.show()

if __name__ == '__main__':
    main()
    
