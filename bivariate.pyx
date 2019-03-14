import cython
import math
from scipy import integrate, LowLevelCallable
import matplotlib.pyplot as plt
import time
from libc.math cimport exp, tanh, sqrt, log, pow
import ctypes, os

lib = ctypes.CDLL(os.path.abspath('./integrands.so'))
lib.top_x1_real.restype = ctypes.c_double
lib.top_x1_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_x2_real.restype = ctypes.c_double
lib.top_x2_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.bottom_real.restype = ctypes.c_double
lib.bottom_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)

lib.top_x1_est.restype = ctypes.c_double
lib.top_x1_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_x2_est.restype = ctypes.c_double
lib.top_x2_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.bottom_est.restype = ctypes.c_double
lib.bottom_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)

cpdef gradient_descent(int steps, double learning_rate, real_means, est_means, s_intervals):
    plt.ylabel('Log Distance')
    plt.xlabel('Steps')
    plt.title('Log Distance vs. Steps')

    for intervals in s_intervals:
        est_x1 = est_means[0]
        est_x2 = est_means[1]
        step_values = []
        dist_values = []
        dist_values_log = []

        for step in range(steps):
            if step > 1:
                distance = euclidean_distance(real_means, est_x1, est_x2)
                if step % 1000 == 0:
                    print('\n')
                    print('Steps: ' + str(step))
                    print('Learning Rate: ' + str(learning_rate))
                    print('Intervals (x1, x2): ' + str(intervals))
                    print('Starting Estimated Means (x1, x2): ' + str(est_means))
                    print('Current Estimated Means (x1, x2): (' + str(est_x1) +', ' + str(est_x2) + ')')
                    print('Population Means (x1, x2): ' + str(real_means))
                    print('Log Distance: ' + str(log(distance)))

                step_values.append(step)
                # dist_values.append(distance)
                dist_values_log.append(log(distance))
                temp_est_x1 = est_x1
                temp_est_x2 = est_x2

                c = ctypes.c_double * 4
                c = c(temp_est_x1,temp_est_x2,real_means[0],real_means[1])
                user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

                integrand_top_x1_real = LowLevelCallable(lib.top_x1_real, user_data)
                integrand_top_x2_real = LowLevelCallable(lib.top_x2_real, user_data)
                integrand_bottom_real = LowLevelCallable(lib.bottom_real, user_data)
                integrand_top_x1_est = LowLevelCallable(lib.top_x1_est, user_data)
                integrand_top_x2_est = LowLevelCallable(lib.top_x2_est, user_data)
                integrand_bottom_est = LowLevelCallable(lib.bottom_est, user_data)

                est_x1 = temp_est_x1 + learning_rate * (expectation(intervals, integrand_top_x1_real, integrand_bottom_real, c) - expectation(intervals, integrand_top_x1_est,integrand_bottom_est, c))
                est_x2 = temp_est_x2 + learning_rate * (expectation(intervals, integrand_top_x2_real, integrand_bottom_real, c) - expectation(intervals, integrand_top_x2_est,integrand_bottom_est, c))


    plt.plot(step_values, dist_values_log)
    # plt.legend(loc='upper right')
    plt.show()


def expectation(intervals, integrand_top, integrand_bottom, est_or_real_mean):
    top = integrate.dblquad(integrand_top, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1], args=(est_or_real_mean))[0]
    bottom = integrate.dblquad(integrand_bottom, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1], args=(est_or_real_mean))[0]
    try:
        return top / bottom
    except:
        print("Bottom is too small. Please try again.")


cdef euclidean_distance(real, double est_x1, double est_x2):
    return sqrt(pow((real[0] - est_x1),2) + pow((real[1] - est_x2),2))

def help():
    print("\nFormat: gradient_descent(steps, learning_rate, (x1_real_mean, x2_real_mean), (x1_start_mean, x2_start_mean), [[(x1_lower_bound,x1_upper_bound),(x2_lower_bound,x2_upper_bound)]])\n")
    print("\nExample: gradient_descent(10000, 0.01, (4,4), (10,10), [[(3,5),(5,8)]])\n")