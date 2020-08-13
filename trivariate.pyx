import cython
import math
from scipy import integrate, LowLevelCallable
import matplotlib.pyplot as plt
import time
from libc.math cimport sqrt, log, pow, abs
import ctypes, os
import ast
import numpy as np


lib = ctypes.CDLL(os.path.abspath('./trivariate-integrands.so'))
lib.top_x_real.restype = ctypes.c_double
lib.top_x_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_y_real.restype = ctypes.c_double
lib.top_y_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_z_real.restype = ctypes.c_double
lib.top_z_real.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_x_est.restype = ctypes.c_double
lib.top_x_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_y_est.restype = ctypes.c_double
lib.top_y_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.top_z_est.restype = ctypes.c_double
lib.top_z_est.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
lib.bottom.restype = ctypes.c_double
lib.bottom.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)


cpdef run(double learning_rate, real_means, est_means, epsilon, step_limit, s_intervals=None):
    est_x = est_means[0]
    est_y = est_means[1]
    est_z = est_means[2]
    error = 1e15
    step = 0

    step_list = []
    error_list = []

    while step < step_limit:
        step += 1
        prev_error = error
        error = euclidean_distance(real_means, est_x, est_y, est_z)
        print(est_x, est_y, est_z, error)

        step_list.append(step)
        error_list.append(error)

        temp_est_x = est_x
        temp_est_y = est_y
        temp_est_z = est_z

        data = (temp_est_x, temp_est_y, temp_est_z, real_means[0], real_means[1], real_means[2])

        est_x = temp_est_x + learning_rate * (get_value('x_real', 'real', data) - get_value('x_est', 'est', data))
        est_y = temp_est_y + learning_rate * (get_value('y_real', 'real', data) - get_value('y_est', 'est', data))
        est_z = temp_est_z + learning_rate * (get_value('z_real', 'real', data) - get_value('z_est', 'est', data))

    return step_list, error_list


def get_value(top, bottom, data, intervals=None):
    # get bottom
    c = ctypes.c_double * 3
    if bottom == 'real':
        c = c(data[3], data[4], data[5])
    elif bottom == 'est':
        c = c(data[0], data[1], data[2])
    user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)
    integrand_bottom = LowLevelCallable(lib.bottom, user_data)

    # lib.tetra.restype = ctypes.c_double
    # lib.tetra.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    # tetra = LowLevelCallable(lib.tetra, user_data)
    # test = integrate.tplquad(tetra, 0, 1, lambda x: 0, lambda x: 2-2*x, lambda x,y: 0, lambda x,y: 3-3*x-1.5*y)
    # print(test, "tetra")

    # lib.para.restype = ctypes.c_double
    # lib.para.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p)
    # para = LowLevelCallable(lib.para, user_data)
    # test = integrate.tplquad(para, -math.sqrt(2), math.sqrt(2), lambda x: -math.sqrt(2-x**2), lambda x: math.sqrt(2-x**2), lambda x,y: x**2+y**2, lambda x,y: math.sqrt(6-x**2 - y**2))
    # print(test, "para")

    bottom = integrate.tplquad(integrand_bottom, 0, 3, lambda x: 0, lambda x: 2-(2*x/3), lambda x,y: 0, lambda x,y: 5-(5*x/3)-(5*y/2))[0]

    # get the rest
    c = ctypes.c_double * 7
    c = c(data[0], data[1], data[2], data[3], data[4], data[5], bottom)
    user_data = ctypes.cast(ctypes.pointer(c), ctypes.c_void_p)

    if top == 'x_real':
        integrand_top = LowLevelCallable(lib.top_x_real, user_data)
    elif top == 'x_est':
        integrand_top = LowLevelCallable(lib.top_x_est, user_data)
    elif top == 'y_real':
        integrand_top = LowLevelCallable(lib.top_y_real, user_data)
    elif top == 'y_est':
        integrand_top = LowLevelCallable(lib.top_y_est, user_data)
    elif top == 'z_real':
        integrand_top = LowLevelCallable(lib.top_z_real, user_data)
    elif top == 'z_est':
        integrand_top = LowLevelCallable(lib.top_z_est, user_data)
        
    top = integrate.tplquad(integrand_top, 0, 3, lambda x: 0, lambda x: 2-(2*x/3), lambda x,y: 0, lambda x,y: 5-(5*x/3)-(5*y/2))[0]

    return top


cdef euclidean_distance(real, double est_x, double est_y, double est_z):
    distance_list = []
    distance_list.append(sqrt(pow((real[0] + est_x), 2) + pow((real[1] - est_y), 2) + pow((real[2] - est_z), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x), 2) + pow((real[1] + est_y), 2) + pow((real[2] - est_z), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x), 2) + pow((real[1] - est_y), 2) + pow((real[2] - est_z), 2)))
    distance_list.append(sqrt(pow((real[0] + est_x), 2) + pow((real[1] + est_y), 2) + pow((real[2] - est_z), 2)))
    distance_list.append(sqrt(pow((real[0] + est_x), 2) + pow((real[1] - est_y), 2) + pow((real[2] + est_z), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x), 2) + pow((real[1] + est_y), 2) + pow((real[2] + est_z), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x), 2) + pow((real[1] - est_y), 2) + pow((real[2] + est_z), 2)))
    distance_list.append(sqrt(pow((real[0] + est_x), 2) + pow((real[1] + est_y), 2) + pow((real[2] + est_z), 2)))
    return min(distance_list)