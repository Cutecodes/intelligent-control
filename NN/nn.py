import numpy as np 
import matplotlib.pyplot as plt

def target_fn(x):
    return 1+np.sin(np.pi*x/4)

#sample = [(i,target_fn(i))for i in np.linspace(-2,2,20)]
sample = [(-2,target_fn(-2)),(-1,target_fn(-1)),\
            (0,target_fn(0)),(1,target_fn(1)),(2,target_fn(2))]
def dataset():
    #随机返回一个样本
    '''sample = [(-2,target_fn(-2)),(-1,target_fn(-1)),\
            (0,target_fn(0)),(1,target_fn(1)),(2,target_fn(2))]'''
    global sample
    
    return sample[np.random.randint(0,len(sample))]

def logsig(x):
    return 1/(1+np.exp(-x))

def purelin(x):
    return x 

#初始条件
w1 = np.array([[-0.27],[-0.41]])
b1 = np.array([[-0.48],[-0.13]])
w2 = np.array([[0.09,-0.17]])
b2 = np.array([[0.48]])
alpha = 0.01



def train():
    global w1,b1,w2,b2,alpha
    (a0,t) = dataset()
    
    #前向传播   
    a1 = logsig(w1*a0+b1)
    a2 = purelin(np.dot(w2,a1)+b2)
        
    #反向传播  
    df2 = 1
    df1 = np.array([[(1-a1[0][0])*a1[0][0],0],
        [0,(1-a1[1][0])*a1[1][0]]])    
    s2 = -2 * df2 * (t-a2)
    s1 = np.dot(df1,w2.T)*s2
    
    #更新权值
    w2 = w2 - alpha*s2*a1.T    
    b2 = b2 - alpha*s2   
    w1 = w1 - alpha*s1*a0   
    b1 = b1 - alpha*s1
    return np.sum(t-a2)

def forward(a0):
    global w1,b1,w2,b2,alpha
    a1 = logsig(w1*a0+b1)
    a2 = purelin(np.dot(w2,a1)+b2)

    return np.sum(a2)

def main():
    global w1,b1,w2,b2,alpha,sample
    e = []
    for i in range(10000):
        e.append(train())
    print("w1:")
    print(w1)
    print("b1:")
    print(b1)
    print("w2:")
    print(w2)
    print("b2:")
    print(b2)
    #实际函数
    gx = []
    #神经网络拟合
    nnx = []
    x = np.linspace(-2,2,1000)
    for i in x:
        gx.append(target_fn(i))
        nnx.append(forward(i))
    plt.subplot(311)
    plt.title('gx')
    plt.plot(x,gx)
    plt.subplot(312)
    plt.title('nnx')
    plt.plot(x,nnx)
    plt.subplot(313)
    plt.title('e')
    plt.plot(np.linspace(0,len(e),len(e)),e)
    
    plt.show()

if __name__ == '__main__':
    main()


