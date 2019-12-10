import cython
import math
from scipy import integrate, LowLevelCallable
import matplotlib.pyplot as plt
import time
from libc.math cimport sqrt, log, pow, abs
import ctypes, os
import ast

lib = ctypes.CDLL(os.path.abspath('./univariate-integrands.so'))
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

cpdef run(int steps, double learning_rate, double est_mean, real_mean, s_interval, fixed_error):
    plt.ylabel('Error')
    plt.xlabel('Iteration')
    plt.title('Error vs. Iteration')

    error_values = []
    estimated_mean = []

    current = est_mean
    end = -est_mean
    difference = abs(est_mean) * 2

    if est_mean < end:
        change = 0.01
    else:
        change = -0.01

    # steps = abs(difference/change)

    initial_diff = int(abs(current - est_mean))
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

        derivative = expectation(s_interval, integrand_top_1, integrand_bottom_real, c) - expectation(s_interval, integrand_top_2, integrand_bottom_est, c) + pow(expectation(s_interval, integrand_top_3, integrand_bottom_est, c),2);
        error_values.append(derivative)

        check_cur_diff = int(abs(current - est_mean))

        if check_cur_diff == initial_diff and initial_count == 0:
            print('\n')
            print('Starting Estimated Mean: ' + str(est_mean))
            print('Estimated Mean: ' + str(current))
            print('Second Derivative: ' + str(derivative))
            print('Interval: ' + str(s_interval))
            print('Population Mean: ' + str(real_mean))
            initial_count += 1

        if check_cur_diff != cur_diff:
            print('\n')
            print('Starting Estimated Mean: ' + str(est_mean))
            print('Estimated Mean: ' + str(current))
            print('Second Derivative: ' + str(derivative))
            print('Interval: ' + str(s_interval))
            print('Population Mean: ' + str(real_mean))
            cur_diff = check_cur_diff

        current += change

    plt.plot(estimated_means,second_derivatives)
    plt.show()

    if fixed_error_step is not None:
        # save values for iteration vs. denominator graph
        if not os.path.exists('./experiments/' + str(learning_rate) + '-' + str(real_mean) + '-' + str(fixed_error)):
            os.makedirs('./experiments/' + str(learning_rate) + '-' + str(real_mean) + '-' + str(fixed_error))
        f = open('./experiments/' + str(learning_rate) + '-' + str(real_mean) + '-' + str(fixed_error) + '/' + str(est_mean) + '-' + str(s_intervals) +  '-' + str(denominator) + '-' + str(fixed_error_step), 'w')
        save_dict = {}
        save_dict['second_derivatives_dict'] = second_derivatives
        save_dict['estimated_means_dict'] = estimated_means
        save_dict['steps'] = str(steps)
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['real_mean'] = str(real_mean)
        save_dict['est_mean'] = str(est_mean)
        save_dict['s_interval'] = str(s_interval)
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
    print("\nFormat: univariate.run(steps, learning_rate, real_mean, est_mean, (x_lower_bound,x_upper_bound), fixed_error_checkpoint)\n")
    print("\nExample: univariate.run(10000, 0.01, 4, 10, (3, 5), 0.1)\n")

def view(data_file_path):
    f = open(str(data_file_path), 'r').readlines()
    f = ast.literal_eval(f[0])
    print('\n')
    print('Steps: ' + f['steps'])
    print('Learning Rate: ' + f['learning_rate'])
    print('Real mean: ' + f['real_mean'])
    print('Interval: ' + f['s_interval'])
    print('Starting estimated mean: ' + f['est_mean'])
    print('Interval: ' + f['s_interval'])

    plt.ylabel('Error')
    plt.xlabel('Iteration')
    plt.title('Error vs. Iteration')
    plt.plot(f['estimated_means_dict'],f['second_derivatives_dict'])
    plt.show()