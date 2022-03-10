from Inverted_pendulum import InvertPendulum
from PID import PID
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np 

def FIS(g0,g1,h):
    #设定变量取值范围
    x_de_range = np.arange(-np.pi/2,np.pi/2,0.01,np.float32)
    x_e_range = np.arange(-np.pi,np.pi,0.01,np.float32)
    y_u_range = np.arange(-30,30,0.1,np.float32)

    #创建模糊控制变量
    x_de = ctrl.Antecedent(x_de_range,'change-in-error')
    x_e = ctrl.Antecedent(x_e_range,'error')
    y_u = ctrl.Consequent(y_u_range,'force')
    #定义模糊集和隶属函数
    x_de['neglarge'] = fuzz.trapmf(x_de_range,[-np.pi,-np.pi/2,-np.pi/4,-np.pi/8])
    x_de['negsmall'] = fuzz.trimf(x_de_range,[-np.pi/4,-np.pi/8,0.0])
    x_de['zero'] = fuzz.trimf(x_de_range,[-np.pi/8,0.0,np.pi/8])
    x_de['possmall'] = fuzz.trimf(x_de_range,[0.0,np.pi/8,np.pi/4])
    x_de['poslarge'] = fuzz.trapmf(x_de_range,[np.pi/8,np.pi/4,np.pi/2,np.pi])

    x_e['neglarge'] = fuzz.trapmf(x_e_range,[-np.pi*2,-np.pi,-np.pi/2,-np.pi/4])
    x_e['negsmall'] = fuzz.trimf(x_e_range,[-np.pi/2,-np.pi/4,0.0])
    x_e['zero'] = fuzz.trimf(x_e_range,[-np.pi/4,0.0,np.pi/4])
    x_e['possmall'] = fuzz.trimf(x_e_range,[0.0,np.pi/4,np.pi/2])
    x_e['poslarge'] = fuzz.trapmf(x_e_range,[np.pi/4,np.pi/2,np.pi,np.pi*2])

    y_u['neglarge'] = fuzz.trimf(y_u_range,[-30.0,-20.0,-10.0])
    y_u['negsmall'] = fuzz.trimf(y_u_range,[-20.0,-10.0,0.0])
    y_u['zero'] = fuzz.trimf(y_u_range,[-10.0,0.0,10.0])
    y_u['possmall'] = fuzz.trimf(y_u_range,[0.0,10.0,20.0])
    y_u['poslarge'] = fuzz.trimf(y_u_range,[10.0,20.0,30.0])  

    # 设定输出powder的解模糊方法——质心解模糊方式
    y_u.defuzzify_method='centroid'
    #可视化隶属函数
    #x_de.view()
    #x_e.view()
    #y_u.view()
    
    # 建立模糊控制规则
    rule0 = ctrl.Rule(antecedent=((x_de['neglarge'] & x_e['neglarge']) |
                               (x_de['neglarge'] & x_e['negsmall']) |
                               (x_de['neglarge'] & x_e['zero']) |
                               (x_de['negsmall'] & x_e['neglarge'])|
                               (x_de['negsmall'] & x_e['negsmall']) |
                               (x_de['zero'] & x_e['neglarge'])
                               ),
                              consequent=y_u['poslarge'], label='rule poslarge')

    rule1 = ctrl.Rule(antecedent=((x_de['possmall'] & x_e['neglarge']) |
                               (x_de['zero'] & x_e['negsmall']) |
                               (x_de['negsmall'] & x_e['zero']) |
                               (x_de['neglarge'] & x_e['possmall'])
                               
                               ),
                               consequent=y_u['possmall'], label='rule possmall')

    rule2 = ctrl.Rule(antecedent=((x_de['poslarge'] & x_e['neglarge']) |
                               (x_de['possmall'] & x_e['negsmall']) |
                               (x_de['zero'] & x_e['zero']) |
                               (x_de['negsmall'] & x_e['possmall'])|
                               (x_de['neglarge'] & x_e['poslarge'])
                               ),
                               consequent=y_u['zero'], label='rule zero')

    rule3 = ctrl.Rule(antecedent=((x_de['possmall'] & x_e['zero']) |
                                (x_de['zero'] & x_e['possmall']) |
                               (x_de['negsmall'] & x_e['poslarge']) |
                               (x_de['poslarge'] & x_e['negsmall'])
                               
                               ),
                               consequent=y_u['negsmall'], label='rule negsmall')

    rule4 = ctrl.Rule(antecedent=((x_de['poslarge'] & x_e['poslarge']) |
                               (x_de['poslarge'] & x_e['possmall']) |
                               (x_de['poslarge'] & x_e['zero']) |
                               (x_de['possmall'] & x_e['poslarge'])|
                               (x_de['possmall'] & x_e['possmall']) |
                               (x_de['zero'] & x_e['poslarge'])
                               ),
                               consequent=y_u['neglarge'], label='rule neglarge')
    # 系统和运行环境初始化
    
    #rule0.view()
    system = ctrl.ControlSystem(rules=[rule0, rule1, rule2,rule3,rule4])

    fuzzy_controller = ctrl.ControlSystemSimulation(system)
    def controller(de,e,sum_e):
        fuzzy_controller.input['change-in-error']=g0*de
        fuzzy_controller.input['error']=g1*e
        fuzzy_controller.compute()
        return h*fuzzy_controller.output['force']
    return controller

def r(t):
    #参考量
    return 0.0

def U(t):
    #扰动量    
    return 0.0

def main():
    #时间间隔
    h = 0.001
    #创建PID控制器 FIS（g0,g1,h)
    #g0*de g1*e h*u
    fis_controller = FIS(0.1,2.0,5.0)
    ip = InvertPendulum(y=0.1,controller=fis_controller,r=r,u=U)
    y = []
    u = []
    for i in range(3000):
        # 模拟4s
        status = ip.step(h)
        y.append(status[0])
        u.append(fis_controller((r(i*h+h)-r(i*h))/h-status[1],status[3],status[4]))

    t = np.linspace(0,3,3000)
    plt.subplot(211)
    plt.title('fis_y')
    plt.plot(t,y)
    plt.subplot(212)
    plt.title('fis_u')
    plt.plot(t,u)
    plt.show()

if __name__ == '__main__':
    main()
