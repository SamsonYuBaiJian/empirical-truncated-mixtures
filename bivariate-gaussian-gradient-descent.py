import math
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import time

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
                    dist_values_log = []

                    for step in range(steps):
                        if step > 1:
                            if step % 1000 == 0:
                                print('Number of steps: ' + str(step))
                                print('Learning rate: ' + str(lr))
                                print('Intervals (x1,x2): ' + str(intervals))
                                print('Starting estimated means (x1,x2): ' + str(est_initial))
                                print('Current estimated means (x1,x2): (' + str(est_x1) +', ' + str(est_x2) + ')')
                                print('Population means (x1,x2): ' + str(real))
                                distance = euclidean_distance(real, est_x1, est_x2)
                                print('Distance: ' + str(distance))
                                print('Distance log: ' + str(math.log(distance)))
                                print('\n')

                            step_values.append(step)
                            distance = euclidean_distance(real, est_x1, est_x2)
                            dist_values.append(distance)
                            dist_values_log.append(math.log(distance))
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

                    #plt.plot(step_values_log, dist_values, label="Step Log")
                    plt.plot(step_values, dist_values_log, label="Distance log vs step")
                    # plt.plot(step_values, dist_values, label="Distance")

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
    top = integrate.dblquad(integrand_top, intervals[0][0], intervals[0][1], lambda x2: intervals[1][0], lambda x2: intervals[1][1])[0]
    bottom = integrate.dblquad(integrand_bottom, intervals[0][0], intervals[0][1], lambda x2: intervals[1][0], lambda x2: intervals[1][1])[0]
    try:
        return top / bottom
    except:
        print("Bottom is too small. Please try again.")


def euclidean_distance(real, est_x1, est_x2):
    return math.sqrt((real[0] - est_x1)**2 + (real[1] - est_x2)**2)


## initialise parameters
population_means_x1_x2 = [(5,5)]
learning_rates = [0.01]
starting_estimated_means_x1_x2 = [(40,40)]
s_intervals_x1_x2 = [[(9,12),(10,15)]]
steps = 10000

start_time = time.clock()
gradient_descent(steps, learning_rates, population_means_x1_x2, starting_estimated_means_x1_x2, s_intervals_x1_x2)
print(time.clock() - start_time, "seconds")