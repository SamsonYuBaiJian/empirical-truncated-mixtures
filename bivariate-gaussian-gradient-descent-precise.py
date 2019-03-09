import numpy as np
import math
import matplotlib.pyplot as plt
import mpmath as mp

def gradient_descent(steps, learning_rates, real_means, est_means, s_intervals):
    plt.ylabel('Distance')
    plt.xlabel('Number of steps')
    plt.title('Distance vs. number of steps')

    for est_initial in est_means:
        for real in real_means:
            for lr in learning_rates:
                for intervals in s_intervals:
                    est_x1 = est_initial[0]
                    est_x2 = est_initial[1]
                    step_values = []
                    dist_values = []

                    for step in range(steps):
                        if step % 1000 == 0:
                            print('Number of steps: ' + str(step))
                            print('Learning rate: ' + str(lr))
                            print('Intervals (x1,x2): ' + str(intervals))
                            print('Starting estimated means (x1,x2): ' + str(est_initial))
                            print('Current estimated means (x1,x2): (' + str(est_x1) +', ' + str(est_x2) + ')')
                            print('Population means (x1,x2): ' + str(real))
                            print('Distance: ' + str(euclidean_distance(real, est_x1, est_x2)))
                            print('\n')

                        step_values.append(step)
                        dist_values.append(euclidean_distance(real, est_x1, est_x2))
                        temp_est_x1 = est_x1
                        temp_est_x2 = est_x2
                        temp_est = (temp_est_x1, temp_est_x2)

                        est_x1 = temp_est_x1 + lr * (expectation(intervals, integrand_top_x1(
                                temp_est, real), integrand_bottom(
                                real)) - expectation(intervals, integrand_top_x1(
                                temp_est, temp_est), integrand_bottom(temp_est)))

                        est_x2 = temp_est_x2 + lr * (expectation(intervals, integrand_top_x2(
                                temp_est, real), integrand_bottom(
                                real)) - expectation(intervals, integrand_top_x2(
                                temp_est, temp_est), integrand_bottom(temp_est)))


                    plt.plot(step_values, dist_values, label=str(intervals))

    plt.legend(loc='upper right')
    plt.show()


def integrand_top_x1(est_mean, est_or_real_mean):
    return lambda x1,x2: x1 * math.tanh(x1 * est_mean[0] + x2 * est_mean[1]) * (math.exp(-0.5 * ((x1 - est_or_real_mean[0])**2 + (x2 - est_or_real_mean[1])**2)) + \
           math.exp(-0.5 * ((x1 + est_or_real_mean[0])**2 + (x2 + est_or_real_mean[1])**2)))

def integrand_top_x2(est_mean, est_or_real_mean):
    return lambda x1,x2: x2 * math.tanh(x1 * est_mean[0] + x2 * est_mean[1]) * (math.exp(-0.5 * ((x1 - est_or_real_mean[0])**2 + (x2 - est_or_real_mean[1])**2)) + \
           math.exp(-0.5 * ((x1 + est_or_real_mean[0])**2 + (x2 + est_or_real_mean[1])**2)))


def integrand_bottom(est_or_real_mean):
    return lambda x1,x2: math.exp(-0.5 * ((x1 - est_or_real_mean[0])**2 + (x2 - est_or_real_mean[1])**2)) + \
           math.exp(-0.5 * ((x1 + est_or_real_mean[0])**2 + (x2 + est_or_real_mean[1])**2))


def expectation(intervals, integrand_top, integrand_bottom):
    top = mp.quad(integrand_top, [intervals[0][0], intervals[0][1]], [intervals[1][0], intervals[1][1]])
    bottom = mp.quad(integrand_bottom, [intervals[0][0], intervals[0][1]], [intervals[1][0], intervals[1][1]])
    try:
        return top / bottom
    except:
        print("Bottom is too small. Please try again.")


def euclidean_distance(real, est_x1, est_x2):
    return math.sqrt((real[0] - est_x1)**2 + (real[1] - est_x2)**2)


## initialise parameters
population_means_x1_x2 = [(5,5)]
learning_rates = [0.05]
starting_estimated_means_x1_x2 = [(30,30)]
s_intervals_x1_x2 = [[(12,20),(25,35)]]
steps = 7000
mp.dps = 5

gradient_descent(steps, learning_rates, population_means_x1_x2, starting_estimated_means_x1_x2, s_intervals_x1_x2)