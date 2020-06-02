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


cpdef run(exp_type, double learning_rate, real_means, est_means, s_intervals, epsilon):
    est_x1 = est_means[0]
    est_x2 = est_means[1]
    error = 1e15
    step = 0
    step_limit = 10000


    if exp_type == 'random_points_error_vs_step':
        step_list = []
        error_list = []

        while step < step_limit:
            step += 1
            prev_error = error
            error = euclidean_distance(real_means, est_x1, est_x2)

            step_list.append(step)
            error_list.append(error)

            temp_est_x1 = est_x1
            temp_est_x2 = est_x2

            c = ctypes.c_double * 4
            c = c(temp_est_x1, temp_est_x2, real_means[0], real_means[1])
            user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

            integrand_top_x1_real = LowLevelCallable(lib.top_x1_real, user_data)
            integrand_top_x2_real = LowLevelCallable(lib.top_x2_real, user_data)
            integrand_bottom_real = LowLevelCallable(lib.bottom_real, user_data)
            integrand_top_x1_est = LowLevelCallable(lib.top_x1_est, user_data)
            integrand_top_x2_est = LowLevelCallable(lib.top_x2_est, user_data)
            integrand_bottom_est = LowLevelCallable(lib.bottom_est, user_data)

            est_x1 = temp_est_x1 + learning_rate * (expectation(s_intervals, integrand_top_x1_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x1_est, integrand_bottom_est))
            est_x2 = temp_est_x2 + learning_rate * (expectation(s_intervals, integrand_top_x2_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x2_est, integrand_bottom_est))

        return step_list, error_list


    elif exp_type == 'trajectory':
        all_est_means = []
        while True:
            step += 1
            all_est_means.append((est_x1, est_x2))
            prev_error = error
            error = euclidean_distance(real_means, est_x1, est_x2)

            if step == 1:
                print('Learning rate: ' + str(learning_rate))
                print('Starting estimated means: ' + str(est_means))
                print('True means: ' + str(real_means))
                print('Intervals: ' + str(s_intervals))
                print('Epsilon: ' + str(epsilon))

            if prev_error > epsilon and error < epsilon:
                epsilon_step = step
                print("Final step for reaching error: " + str(epsilon_step) + "\n")
                break

            temp_est_x1 = est_x1
            temp_est_x2 = est_x2

            c = ctypes.c_double * 4
            c = c(temp_est_x1, temp_est_x2, real_means[0], real_means[1])
            user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

            integrand_top_x1_real = LowLevelCallable(lib.top_x1_real, user_data)
            integrand_top_x2_real = LowLevelCallable(lib.top_x2_real, user_data)
            integrand_bottom_real = LowLevelCallable(lib.bottom_real, user_data)
            integrand_top_x1_est = LowLevelCallable(lib.top_x1_est, user_data)
            integrand_top_x2_est = LowLevelCallable(lib.top_x2_est, user_data)
            integrand_bottom_est = LowLevelCallable(lib.bottom_est, user_data)

            est_x1 = temp_est_x1 + learning_rate * (expectation(s_intervals, integrand_top_x1_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x1_est, integrand_bottom_est))
            est_x2 = temp_est_x2 + learning_rate * (expectation(s_intervals, integrand_top_x2_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x2_est, integrand_bottom_est))
        
        return all_est_means


    elif exp_type == 'random_points_epsilon_and_step':
        while True:
            step += 1
            prev_error = error
            error = euclidean_distance(real_means, est_x1, est_x2)

            if prev_error > epsilon and error < epsilon:
                epsilon_step = step
                break

            temp_est_x1 = est_x1
            temp_est_x2 = est_x2

            c = ctypes.c_double * 4
            c = c(temp_est_x1, temp_est_x2, real_means[0], real_means[1])
            user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

            integrand_top_x1_real = LowLevelCallable(lib.top_x1_real, user_data)
            integrand_top_x2_real = LowLevelCallable(lib.top_x2_real, user_data)
            integrand_bottom_real = LowLevelCallable(lib.bottom_real, user_data)
            integrand_top_x1_est = LowLevelCallable(lib.top_x1_est, user_data)
            integrand_top_x2_est = LowLevelCallable(lib.top_x2_est, user_data)
            integrand_bottom_est = LowLevelCallable(lib.bottom_est, user_data)

            est_x1 = temp_est_x1 + learning_rate * (expectation(s_intervals, integrand_top_x1_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x1_est, integrand_bottom_est))
            est_x2 = temp_est_x2 + learning_rate * (expectation(s_intervals, integrand_top_x2_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x2_est, integrand_bottom_est))
        
        return epsilon_step


    elif exp_type == 'single_point_vary_s':
        while True:
            step += 1
            prev_error = error
            error = euclidean_distance(real_means, est_x1, est_x2)

            if step == 1:
                print('Learning rate: ' + str(learning_rate))
                print('Starting estimated means: ' + str(est_means))
                print('True means: ' + str(real_means))
                print('Intervals: ' + str(s_intervals))
                print('Epsilon: ' + str(epsilon))

            if prev_error > epsilon and error < epsilon:
                epsilon_step = step
                print("Final step for reaching error: " + str(epsilon_step) + "\n")
                break

            temp_est_x1 = est_x1
            temp_est_x2 = est_x2

            c = ctypes.c_double * 4
            c = c(temp_est_x1, temp_est_x2, real_means[0], real_means[1])
            user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

            integrand_top_x1_real = LowLevelCallable(lib.top_x1_real, user_data)
            integrand_top_x2_real = LowLevelCallable(lib.top_x2_real, user_data)
            integrand_bottom_real = LowLevelCallable(lib.bottom_real, user_data)
            integrand_top_x1_est = LowLevelCallable(lib.top_x1_est, user_data)
            integrand_top_x2_est = LowLevelCallable(lib.top_x2_est, user_data)
            integrand_bottom_est = LowLevelCallable(lib.bottom_est, user_data)

            est_x1 = temp_est_x1 + learning_rate * (expectation(s_intervals, integrand_top_x1_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x1_est, integrand_bottom_est))
            est_x2 = temp_est_x2 + learning_rate * (expectation(s_intervals, integrand_top_x2_real, integrand_bottom_real) - expectation(s_intervals, integrand_top_x2_est, integrand_bottom_est))

        denominator = get_denominator(s_intervals, integrand_bottom_real)
        
        return epsilon_step, denominator


def expectation(intervals, integrand_top, integrand_bottom):
    top = integrate.dblquad(integrand_top, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1])[0]
    bottom = integrate.dblquad(integrand_bottom, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1])[0]
    try:
        return top / bottom
    except:
        print("Bottom is too small. Please try again.")


def get_denominator(intervals, integrand_bottom_real):
    normalising_constant = 0.5 / (2 * math.pi)
    return normalising_constant * integrate.dblquad(integrand_bottom_real, intervals[0][0], intervals[0][1], intervals[1][0], intervals[1][1])[0]


cdef euclidean_distance(real, double est_x1, double est_x2):
    distance_list = []
    distance_list.append(sqrt(pow((real[0] - (-est_x1)), 2) + pow((real[1] - est_x2), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x1), 2) + pow((real[1] - (-est_x2)), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x1), 2) + pow((real[1] - est_x2), 2)))
    distance_list.append(sqrt(pow((real[0] - (-est_x1)), 2) + pow((real[1] - (-est_x2)), 2)))
    return min(distance_list)