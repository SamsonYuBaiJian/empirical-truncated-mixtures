import cython
import math
from scipy import integrate, LowLevelCallable
import matplotlib.pyplot as plt
import time
from libc.math cimport sqrt, log, pow, abs
import ctypes, os
import ast
import numpy as np

lib = ctypes.CDLL(os.path.abspath('./bivariate-integrands.so'))
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

cpdef run(double learning_rate, real_means, est_means, s_intervals, epsilon):
    plt.ylabel('Error')
    plt.xlabel('Iteration')
    plt.title('Error vs. Iteration')

    est_x1 = est_means[0]
    est_x2 = est_means[1]
    step_values = []
    error_values = []
    epsilon_step = None
    error = 1e15

    step = 0

    while True:
        step += 1
        prev_error = error
        error = euclidean_distance(real_means, est_x1, est_x2)

        if step % 1000 == 0:
            print('\n')
            print('Steps: ' + str(step))
            print('Learning rate: ' + str(learning_rate))
            print('Intervals (x1,x2): ' + str(s_intervals))
            print('Starting estimated means (x1,x2): ' + str(est_means))
            print('Current estimated means (x1,x2): (' + str(est_x1) +',' + str(est_x2) + ')')
            print('Real means (x1,x2): ' + str(real_means))
            print('Error: ' + str(error))

        if epsilon_step is None:
            if prev_error > epsilon and error < epsilon:
                epsilon_step = step
                print("Final step for reaching error: " + str(epsilon_step))
                break

        # step_values.append(i)
        # error_values.append(error)
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

        est_x1 = temp_est_x1 + learning_rate * (expectation(s_intervals, integrand_top_x1_real, integrand_bottom_real, c) - expectation(s_intervals, integrand_top_x1_est,integrand_bottom_est, c))
        est_x2 = temp_est_x2 + learning_rate * (expectation(s_intervals, integrand_top_x2_real, integrand_bottom_real, c) - expectation(s_intervals, integrand_top_x2_est,integrand_bottom_est, c))
    
    denominator = get_denominator(s_intervals, integrand_bottom_real, c)

    # plt.plot(step_values, error_values)
    # plt.show()

    return epsilon_step, denominator


def expectation(intervals, integrand_top, integrand_bottom, est_or_real_mean):
    top = integrate.dblquad(integrand_top, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1], args=(est_or_real_mean))[0]
    bottom = integrate.dblquad(integrand_bottom, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1], args=(est_or_real_mean))[0]
    try:
        return top / bottom
    except:
        print("Bottom is too small. Please try again.")


def get_denominator(intervals, integrand_bottom, est_or_real_mean):
    return integrate.dblquad(integrand_bottom, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1], args=(est_or_real_mean))[0]


cdef euclidean_distance(real, double est_x1, double est_x2):
    return sqrt(pow((real[0] - est_x1),2) + pow((real[1] - est_x2),2))


def plot_denom(path):
    assert os.path.exists(path)

    files = os.listdir(path)

    assert len(files) > 0

    error_checkpoint = str(path.split('/')[-1].split('-')[-1])

    plt.ylabel('Number of Iterations')
    plt.xlabel('Denominator')
    plt.title('Number of Iterations vs. Denominator (Error Checkpoint = ' + error_checkpoint + ')')

    epsilon_steps = []
    denominators = []

    graph_dict = {}

    for file in files:
        graph_dict[round(float(str(file.split('/')[-1].split('-')[-2])),3)] = int(str(file.split('/')[-1].split('-')[-1]))
    
    for key in sorted(graph_dict.keys()):
        denominators.append(key)
        epsilon_steps.append(graph_dict[key])

    # plt.xticks(np.arange(denominators[0], denominators[-1], 0.1))
    # plt.yticks(np.arange(epsilon_steps[0], epsilon_steps[-1], 10))
    plt.plot(denominators, epsilon_steps)
    plt.show()