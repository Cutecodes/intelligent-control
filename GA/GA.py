import numpy as np 
import matplotlib.pyplot as plt

pop_size = 400
Pc = 0.8 #交叉率
Pm =1.0/pop_size #变异率

x_min = -1.0
x_max = 2.0

epoch = 100

def init(x_min,x_max,pop_size):
    X = np.random.uniform(x_min,x_max,pop_size)#均匀生成样本点

    return X

def fitness(X):
    '''
    适应度函数
    
    '''
    fit = X.copy()
    for i in range(len(fit)):
        x = fit[i]
        x = x*np.sin(10*np.pi*x)+2.0
        fit[i] = x
    
    return fit

def selection(X,pop_size):
    Y = fitness(X)
    zipped = zip(X,Y)
    sort_zipped = sorted(zipped,key=lambda x:x[1],reverse = True)
    result = zip(*sort_zipped)
    X,Y=[list(x) for x in result]
    '''sumy = np.sum(Y)
    Y = np.around(Y/sumy*pop_size)# 计算个数四舍五入
    print(np.sum(Y))
    temp = np.zeros(pop_size)
    j=0
    for i in range(len(X)):
        while Y[i]>0 and j<pop_size:
            temp[j]=X[i]
            j+=1
            Y[i]=Y[i]-1
    '''
    temp = np.zeros(pop_size)
    for i in range(pop_size):
        temp[i]=X[i]
    np.random.shuffle(temp)#打乱顺序
    X = temp
    return X


def crossover(X):
    global Pc
    Y = np.zeros(2*len(X))
    for i in range(0,len(X),2):
        x = X[i]
        y = X[i+1]
        Y[len(X)+i] = Pc*x+(1-Pc)*y
        Y[len(X)+1+i] = Pc*y+(1-Pc)*x
        Y[i] = x
        Y[i+1] = y
    return Y

def mutation(X):
    global x_min,x_max,Pm
    for x in X:
        if np.random.random_sample()<Pm:
            direction = np.random.choice(10)
            p = np.random.random_sample()
            if direction%2==0:
                x = p*x+(1-p)*x_max
            else:
                x = p*x_min+(1-p)*x
    return X

def main():
    global pop_size,Pc,Pm
    global x_min,x_max,epoch
    X = init(x_min,x_max,pop_size)
    max_fitness = []
    avg_fitness = []
    for i in range(epoch):
        fit = fitness(X)
        max_fitness.append(np.max(fit))    	
        avg_fitness.append(np.mean(fit))
        X = crossover(X)
        X = mutation(X)
        X = selection(X,pop_size)
        
    print("最大函数值为：%.6f"% np.max(max_fitness))
    #收敛之后用平均值代表最优值
    print("最优解为：%.6f"% max(X,key = lambda x:x*np.sin(10*np.pi*x)+2.0))

    plt.plot(np.linspace(0,len(max_fitness),len(max_fitness)),max_fitness)
    plt.plot(np.linspace(0,len(max_fitness),len(max_fitness)),avg_fitness)
    plt.show()

if __name__ == '__main__':
    main()
