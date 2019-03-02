import numpy as np
import math
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def gradient_descent(steps, learning_rates, real_means, est_means, var, s_intervals):
    plt.ylabel('Distance')
    plt.xlabel('Number of steps')
    plt.title('Distance vs. number of steps')

    for est_initial in est_means:
        for real in real_means:
            for lr in learning_rates:
                for interval in s_intervals:
                    est = est_initial
                    step_values = []
                    dist_values = []

                    for step in range(steps):
                        step_values.append(step)
                        dist_values.append(distance(real, est))
                        est = est + (lr / var) * (expectation([interval], integrand_top(
                                est, var, real), integrand_bottom(
                                var, real)) - expectation([interval], integrand_top(
                                est, var, est), integrand_bottom(var, est)))

                        if step % 1000 == 0:
                            print('Number of steps: ' + str(step))
                            print('Learning rate: ' + str(lr))
                            print('Interval: ' + str(interval))
                            print('Starting estimated mean: ' + str(est_initial))
                            print('Current estimated mean ' + str(est))
                            print('Population mean: ' + str(real))
                            print('Distance: ' + str(distance(real, est)))
                            print('\n')

                    plt.plot(step_values, dist_values, label=str(interval))

    plt.legend(loc='upper right')
    plt.show()


def integrand_top(est_mean, var, est_or_real_mean):
    return lambda x: x * np.tanh(x * est_mean / var) * (0.5 * (1/math.sqrt(math.pi * 2 * var)) * math.exp(-(x - est_or_real_mean)**2/(2 * var)) + \
           0.5 * (1/math.sqrt(math.pi * 2 * var)) * math.exp(-(x + est_or_real_mean)**2/(2 * var)))


def integrand_bottom(var, est_or_real_mean):
    return lambda x: 0.5 * (1/math.sqrt(math.pi * 2 * var)) * math.exp(-(x - est_or_real_mean)**2/(2 * var)) + \
           0.5 * (1/math.sqrt(math.pi * 2 * var)) * math.exp(-(x + est_or_real_mean)**2/(2 * var))


def expectation(s_intervals, integrand_top, integrand_bottom):
    top = 0
    bottom = 0
    for interval in s_intervals:
        top += integrate.quad(integrand_top, interval[0], interval[1])[0]
        bottom += integrate.quad(integrand_bottom, interval[0], interval[1])[0]
    try:
        return top / bottom
    except ZeroDivisionError:
        return top / 1e-14


def distance(real, est):
    return abs(real - est)


## initialise parameters
population_means = [5]
learning_rates = [0.05]
starting_estimated_means = [30]
s_intervals = [[0,3],[2,5],[2,8],[3.5,6.5],[5,8],[8,11]]
steps = 3000
# variance is fixed
var = 1

gradient_descent(steps, learning_rates, population_means, starting_estimated_means, var, s_intervals)