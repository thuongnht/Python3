# compute cost function
# gradien descent
# feature normalize
# normal equation
import pandas as pd
import numpy as np
import scipy.linalg as linalg


class Linear_Regression_Helper(object):

    def __init__(self):
        self.result = {}
        pass

    def compute_cost(self, data, target, theta):
        # Initialize some useful values
        J = 0
        temp = np.multiply(float(1) / float(2*self.m), np.square((np.dot(data, theta) - target)))
        # You need to return the following variables correctly
        J += temp.sum().iloc[0]
        return J

    def gradient_descent(self, theta, alpha, iters):
        J_history = np.zeros((iters,1))
        temp = theta

        data = pd.concat([self.data], axis=1)
        target = pd.concat([self.target], axis=1)

        for i in range(0, iters):
            J0 = self.compute_cost(data, target, temp)

            temp -= np.multiply(float(alpha/self.m), np.dot(data.transpose(), (np.dot(data, temp) - target)))

            if self.compute_cost(data, target, temp) > J0:
                # alpha *= 1/3
                # return self.gradient_descent(temp, alpha, iters)
                break
            else:
                # Save the cost J in every iteration
                J_history[i, 0] = self.compute_cost(data, target, temp)

        return temp[:, 0], J_history[:, 0]

    def feature_normalize(self, data):
        # You need to set these values correctly
        X_norm = pd.concat([data], axis=1)
        std = X_norm.std().iloc[:]
        mean = X_norm.mean().iloc[:]
        for j in range(0, self.n-1):
            X_norm.iloc[:, j] = (data.iloc[:, j] - mean.iloc[j]) / std.iloc[j];

        return X_norm, mean, std

    def normal_equation(self):
        data = pd.concat([self.data], axis=1)
        target = pd.concat([self.target], axis=1)
        # pinv(transpose(X)*X)*transpose(X)*y;
        return np.dot(np.dot(linalg.pinv(np.dot(data.transpose(), data)), data.transpose()), target);

    def Fit(self, data, target, choice):
        self.m = len(data.axes[0])
        self.n = len(data.axes[1]) + 1
        self.target = target

        x0 = pd.DataFrame(1.0, index=np.arange(self.m), columns=['x0'])
        self.data = pd.concat([x0, data], axis=1)

        if choice == 'gd':
            print('Running Gradient Descent ...')

            normalized_data, mean, std = self.feature_normalize(data)
            self.data = pd.concat([x0, normalized_data], axis=1)

            iters = 400  # init the iteration values
            alphas = [0.03, 0.01, 0.003]  # init learning rate
            #alphas = [0.01]
            end_theta = np.zeros((len(alphas), self.n))
            J_history = np.zeros((len(alphas), iters))

            for i in range(len(alphas)):
                theta = np.zeros((self.n, 1))
                # self.compute_cost(theta)

                end_theta[i, :], J_history[i, :] = self.gradient_descent(theta, alphas[i], iters)
                # print(np.dot(self.data, end_theta[i,:].transpose()))
                self.result[str(alphas[i])] = {
                    'data': {
                        'x': data.iloc[:, 0],
                        'y': np.dot(self.data, end_theta[i, :].transpose())
                    },
                    'J_history': J_history[i, :].transpose(),
                    'alphas': alphas,
                    'theta': end_theta[i, :].transpose(),
                    'mean': mean,
                    'std': std,
                    'feature': self.n-1
                }
                # print(end_theta)

            return self.result

        elif choice == 'ne':
            print('Solving with Normal Equation ...')

            end_theta = self.normal_equation()
            # print(np.dot(self.data, end_theta))
            self.result['0'] = {
                    'data': {
                        'x': data.iloc[:, 0],
                        'y': np.dot(self.data, end_theta)
                    },
                    'theta': end_theta,
                    'feature': self.n-1
            }

            return self.result


if __name__ == '__main__':
    lrh = Linear_Regression_Helper()
    print(lrh)
