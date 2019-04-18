import numpy as np
import sys
import matplotlib.pyplot as plt
import math

def sample_function_truncation(a,b,s):
    while True:
        x = np.random.normal(loc=a)
        if s > 0:
            if x <= s and x >= -s:
                break
        elif s < 0:
            if x >= s and x <= -s:
                break
        else:
            print("Please make sure interval endpoint is not zero.")
            sys.exit()

    return x * (math.exp(b*x)-math.exp(-b*x))/(math.exp(b*x)+math.exp(-b*x))

def get_real_mean(steps, sample_mean, est_mean, s):
    plt.ylabel('Estimated real mean')
    plt.xlabel('Number of steps')
    plt.title('Estimated real mean vs. number of steps')

    starting_est_real_mean = est_mean

    mean_values = []
    step_values = []

    for step in range(steps):
        step_values.append(step + 1)
        mean_values.append(est_mean)

        est_mean = est_mean + (1/math.sqrt(step + 1)) * (sample_function_truncation(sample_mean,est_mean,s)-sample_function_truncation(est_mean,est_mean,s))

        if (step + 1) % 1000 == 0:
            print('Number of steps: ' + str(step + 1))
            print('Starting sample mean: ' + str(sample_mean))
            print('Starting estimated real mean: ' + str(starting_est_real_mean))
            if s > 0:
                print('Interval: (' + str(-s) + ', ' + str(s) + ')')
            elif s < 0:
                print('Interval: (' + str(s) + ', ' + str(-s) + ')')
            print('Current estimated real mean: ' + str(est_mean))
            print('\n')

    plt.plot(step_values, mean_values)
    plt.show()

while True:
    steps = input('Enter the number of steps: ')
    sample_mean = input('Enter your sample mean: ')
    est_mean = input('Enter your starting estimate for the real mean: ')
    s = input('Enter the endpoint of your interval: ')
    get_real_mean(int(steps), float(sample_mean), float(est_mean), float(s))
    cont = input('Do you want to continue [y/n]: ')
    if cont != 'y':
        break