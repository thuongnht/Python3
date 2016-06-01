# compute cost function
# gradien descent
# feature normalize
# normal equation
import pandas as pd
import numpy as np
import scipy.optimize as op


class Logistic_Regression_Helper(object):

    def __init__(self):
        self.result = {}
        pass

    def Sigmoid(self, theta, x):
        return 1/(1 + np.exp(-np.dot(x, theta)))

    def Gradient(self, theta, x, target, lbda=None):
        thetaReg = theta[1:]
        thetaReg = thetaReg.reshape((self.n-1, 1))
        theta = theta.reshape((self.n, 1))
        grad = np.dot(x.transpose(), self.Sigmoid(theta, x)-target) / self.m
        if lbda:
            grad0 = np.dot(x.iloc[:, 0:1].transpose(), self.Sigmoid(theta, x)-target) / self.m
            grad1 = (np.dot(x.iloc[:, 1:].transpose(), self.Sigmoid(theta, x)-target) / self.m) + (lbda/self.m)*thetaReg
            grad = np.concatenate((grad0, grad1))
            return grad.flatten()
        else:
            return grad.flatten()

    def CostFunc(self, theta, x, target, lbda=None):
        thetaReg = theta[1:]
        thetaReg = thetaReg.reshape((self.n-1, 1))
        theta = theta.reshape((self.n, 1))
        target = target.transpose()
        term1 = np.log(self.Sigmoid(theta, x))
        term2 = np.log(1 - self.Sigmoid(theta, x))
        cost = np.sum(-(np.dot(target, term1) + np.dot((1.0-target), term2))) / self.m
        if lbda:
            cost += (lbda/(2.0*self.m))*np.sum(thetaReg**2)
            return cost
        else:
            return cost

    def Predict(self, theta, x, y):
        p = np.zeros((self.m, 1))
        g = self.Sigmoid(theta, x)
        for i in range(len(g)):
            if g[i] >= 0.5:
                p[i, 0] = 1
            else:
                p[i, 0] = 0
        return np.mean((p[:, 0] == y.iloc[:, 0])*100)

    def frange(self, start, stop, step):
        i = start
        while i <= stop:
            yield i
            i += step

    def Feature_Mapping(self, data, cols, degree):
        if type(data) is np.ndarray:
            data = pd.DataFrame(data)
        else:
            pass
        X0 = data.iloc[:, 0]
        X1 = pd.concat([data.iloc[:, cols[0]]])
        X2 = pd.concat([data.iloc[:, cols[1]]])
        newdata = pd.concat([X0])
        i = 1
        while i <= degree:
            j = 0
            while j <= i:
                newdata = pd.concat([newdata, (np.power(X1, i-j)*np.power(X2, j)).transpose()], axis=1)
                j += 1
            i += 1
        return newdata

    def estimate(self, data, theta, deg=None):
        if self.choice == 'mc':
            return self.Sigmoid(theta.reshape(self.n, 1), data)
        elif self.choice == 'mcr':
            newX = self.Feature_Mapping(data, [1, 2], deg)
            return self.Sigmoid(theta, newX)
        else:
            pass

    def Fit(self, data, target, choice, lbda=None, deg=None):
        self.m = len(data.axes[0])
        self.n = len(data.axes[1]) + 1
        self.choice = choice
        y = target

        x0 = pd.DataFrame(1.0, index=np.arange(self.m), columns=['x0'], dtype=np.float32)
        X = pd.concat([x0, data], axis=1)

        if self.choice == 'mc':
            print('Running Minimize Cost Function ...')

            initial_theta = np.zeros(self.n)
            Result = op.minimize(fun=self.CostFunc,
                                 x0=initial_theta,
                                 args=(X, y),
                                 method='TNC',
                                 jac=self.Gradient,
                                 options={'disp': True,
                                          'maxiter': 400})

            self.result['0'] = {
                'theta': Result.x,
                'cost': self.CostFunc(Result.x, X, y),
                'accuracy': self.Predict(Result.x, X, y),
                'instance': self
            }

            return self.result

        elif self.choice == 'mcr':
            print('Running Regular Minimize Cost Function ...')

            newX = self.Feature_Mapping(X, [1, 2], deg)
            self.n = len(newX.axes[1])
            initial_theta = np.zeros(self.n)
            Result = op.minimize(fun=self.CostFunc,
                                 x0=initial_theta,
                                 args=(newX, y, lbda),
                                 method='TNC',
                                 jac=self.Gradient,
                                 options={'disp': True,
                                          'maxiter': 400})

            self.result['0'] = {
                'theta': Result.x,
                'cost': self.CostFunc(Result.x, newX, y, lbda),
                'accuracy': self.Predict(Result.x, newX, y),
                'instance': self
            }

            return self.result


if __name__ == '__main__':
    lrh = Logistic_Regression_Helper()
    print(lrh)
