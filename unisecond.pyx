import cython
import math
from scipy import integrate, LowLevelCallable
import matplotlib.pyplot as plt
import time
from libc.math cimport exp, tanh, sqrt, log, pow, abs
import ctypes, os
import ast

lib = ctypes.CDLL(os.path.abspath('./second-derivatives.so'))
lib.top_1.restype = ctypes.c_double
lib.top_1.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_2.restype = ctypes.c_double
lib.top_2.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_3.restype = ctypes.c_double
lib.top_3.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.bottom_real.restype = ctypes.c_double
lib.bottom_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.bottom_est.restype = ctypes.c_double
lib.bottom_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)

cpdef univariate_second_derivative(double start, real_mean, s_intervals):
    plt.ylabel('Second Derivatives')
    plt.xlabel('Estimated Means')
    plt.title('Second Derivatives vs. Estimated Means')

    for interval in s_intervals:
        second_derivatives = []
        estimated_means = []

        current = start
        end = -start
        difference = abs(start) * 2

        if start < end:
            change = 0.01
        else:
            change = -0.01

        steps = abs(difference/change)

        initial_diff = int(abs(current - start))
        initial_count = 0
        cur_diff = initial_diff

        for i in range(int(steps)):
            estimated_means.append(current)

            c = ctypes.c_double * 2
            c = c(current, real_mean)
            user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

            integrand_top_1 = LowLevelCallable(lib.top_1, user_data)
            integrand_top_2 = LowLevelCallable(lib.top_2, user_data)
            integrand_top_3 = LowLevelCallable(lib.top_3, user_data)
            integrand_bottom_real = LowLevelCallable(lib.bottom_real, user_data)
            integrand_bottom_est = LowLevelCallable(lib.bottom_est, user_data)

            derivative = expectation(interval, integrand_top_1, integrand_bottom_real, c) - expectation(interval, integrand_top_2, integrand_bottom_est, c) + pow(expectation(interval, integrand_top_3, integrand_bottom_est, c),2);
            second_derivatives.append(derivative)

            check_cur_diff = int(abs(current - start))

            if check_cur_diff == initial_diff and initial_count == 0:
                print('\n')
                print('Starting Estimated Mean: ' + str(start))
                print('Estimated Mean: ' + str(current))
                print('Second Derivative: ' + str(derivative))
                print('Interval: ' + str(interval))
                print('Population Mean: ' + str(real_mean))
                initial_count += 1

            if check_cur_diff != cur_diff:
                print('\n')
                print('Starting Estimated Mean: ' + str(start))
                print('Estimated Mean: ' + str(current))
                print('Second Derivative: ' + str(derivative))
                print('Interval: ' + str(interval))
                print('Population Mean: ' + str(real_mean))
                cur_diff = check_cur_diff

            current += change

    plt.plot(estimated_means,second_derivatives)
    plt.show()

    save = input('\nDo you want to save this? (y/n)\n')

    if save == 'y':
        comments = input('\nEnter your comments.\n')
        f = open('./saved-parameters/second-derivatives/' + str(start) + '-' + str(real_mean) + '-' + str(s_intervals), 'w')
        save_dict = {}
        save_dict['second_derivatives_dict'] = second_derivatives
        save_dict['estimated_means_dict'] = estimated_means
        save_dict['start'] = str(start)
        save_dict['real_mean'] = str(real_mean)
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['comments'] = comments
        f.write(str(save_dict))
        f.close()


def expectation(interval, integrand_top, integrand_bottom, est_or_real_mean):
    arg_tuple=(est_or_real_mean[0], est_or_real_mean[1])
    top = integrate.quad(integrand_top, interval[0], interval[1], args=arg_tuple)[0]
    bottom = integrate.quad(integrand_bottom, interval[0], interval[1], args=arg_tuple)[0]
    try:
        return top / bottom
    except:
        print("Bottom is too small. Please try again.")

def help():
    print("\nFormat: univariate_second_derivative(start, real_mean, [(x1_lower_bound,x1_upper_bound)])\n")
    print("\nExample: univariate_second_derivative(4, 2.5, [(3, 5)])\n")

def load(txt):
    f = open('./saved-parameters/second-derivatives/' + str(txt), 'r').readlines()
    f = ast.literal_eval(f[0])
    print('\n')
    print('Start: ' + f['start'])
    print('Intervals: ' + f['s_intervals'])
    print('Population Mean: ' + f['real_means'])
    print('\nComments: ' + str(f['comments']))

    plt.plot(f['estimated_means_dict'],f['second_derivatives_dict'])
    plt.show()

    change = input("\nDo you want to change your comments? (y/n)\n")
    if change == 'y':
        new = input("\nEnter your new comments.\n")
        f['comments'] = new
        n = open('./saved-parameters/second-derivatives/' + str(txt), 'w')
        n.write(str(f))
        n.close()