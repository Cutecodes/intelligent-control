import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
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
    x_de.view()
    x_e.view()
    y_u.view()
    
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

    fig = plt.figure()  #定义新的三维坐标轴
    ax3 = plt.axes(projection='3d')

   #定义三维数据
    z=[]
    xx = np.arange(-np.pi/2,np.pi/2,0.1)
    yy = np.arange(-np.pi,np.pi,0.2)
    for x in xx:
      t = []
      for y in yy:
        fuzzy_controller.input['change-in-error']=x
        fuzzy_controller.input['error']=y
        fuzzy_controller.compute()
        t.append(fuzzy_controller.output['force'])
      z.append(t)
    Z = np.array(z)
    ##print(Z.shape)

    X, Y = np.meshgrid(xx, yy)

    
#作图

    ax3.view_init(30, 80)
    ax3.plot_surface(X,Y,Z,cmap='rainbow')
#ax3.contour(X,Y,Z, zdim='z',offset=-2，cmap='rainbow)   #等高线图，要设置offset，为Z的最小值
    plt.show()

def main():
    FIS(2.0,0.1,5)
if __name__ == '__main__':
    main()
