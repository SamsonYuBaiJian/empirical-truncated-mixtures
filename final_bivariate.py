import numpy as np
import sys
import matplotlib.pyplot as plt
import math

# a and b are tuples
def sample_function_truncation(a,b,sx,sy):
    while True:
        x = np.random.normal(loc=a[0])
        y = np.random.normal(loc=a[1])
        if sx > 0:
            if sy > 0:
                if x <= sx and x >= -sx and y <= sy and y >= -sy:
                    break
            elif sy < 0:
                if x <= sx and x >= -sx and y <= -sy and y >= sy:
                    break
        elif sx < 0:
            if sy > 0:
                if x >= sx and x <= -sx and y <= sy and y >= -sy:
                    break
            elif sy < 0:
                if x >= sx and x <= -sx and y <= -sy and y >= sy:
                    break
        else:
            print("Please make sure none of the interval endpoints is not zero.")
            sys.exit()

    return (x * math.tanh(x*b[0]+y*b[1]), y * math.tanh(x*b[0]+y*b[1]))


# sample_mean and est_mean are tuples
# s is a tuple of two tuples
def get_real_mean(steps, sample_mean, est_mean, sx,sy):
    plt.ylabel('Distance')
    plt.xlabel('Number of steps')
    plt.title('Distance vs. number of steps')

    starting_est_real_mean = est_mean
    est_mean_x = est_mean[0]
    est_mean_y = est_mean[1]

    #mean_values = []
    step_values = []
    distance_values = []

    for step in range(steps):
        est_mean = (est_mean_x, est_mean_y)

        step_values.append(step + 1)
        #mean_values.append(est_mean)
        dist = euclidean_distance(est_mean,sample_mean)
        distance_values.append(dist)

        if (step + 1) % 1000 == 0:
            print('Number of steps: ' + str(step + 1))
            print('Starting sample mean: ' + str(sample_mean))
            print('Starting estimated real mean: ' + str(starting_est_real_mean))
            if sx > 0 and sy > 0:
                print('Intervals: ((' + str(-sx) + ', ' + str(sx) + '), (' + str(-sy) + ', ' + str(sy) + '))')
            elif sx < 0 and sy>0:
                print('Intervals: ((' + str(sx) + ', ' + str(-sx) + '), (' + str(-sy) + ', ' + str(sy) + '))')
            elif sx > 0 and sy < 0:
                print('Intervals: ((' + str(-sx) + ', ' + str(sx) + '), (' + str(sy) + ', ' + str(-sy) + '))')
            elif sx < 0 and sy < 0:
                print('Intervals: ((' + str(sx) + ', ' + str(-sx) + '), (' + str(sy) + ', ' + str(-sy) + '))')
            print('Current estimated real mean: ' + str(est_mean))
            print('\n')

        f_sample_mean = sample_function_truncation(sample_mean, est_mean,sx,sy)
        f_est_mean = sample_function_truncation(est_mean, est_mean,sx,sy)

        est_mean_x = est_mean_x + (1/math.sqrt(step + 1)) * (f_sample_mean[0]-f_est_mean[0])
        est_mean_y = est_mean_y + (1/math.sqrt(step + 1)) * (f_sample_mean[1]-f_est_mean[1])

    plt.plot(step_values, distance_values)
    plt.show()


def euclidean_distance(one,two):
    return math.sqrt((one[0]-two[0])**2 + (one[1]-two[1])**2)


while True:
    steps = input('Enter the number of steps: ')
    sample_mean_x = input('Enter your sample mean x-coordinate: ')
    sample_mean_y = input('Enter your sample mean y-coordinate: ')
    est_mean_x = input('Enter your starting estimated x-coordinate for the real mean: ')
    est_mean_y = input('Enter your starting estimated y-coordinate for the real mean: ')
    sx = input('Enter the endpoint of your x interval: ')
    sy = input('Enter the endpoint of your y interval: ')
    get_real_mean(int(steps), (float(sample_mean_x),float(sample_mean_y)), (float(est_mean_x),float(est_mean_y)), float(sx), float(sy))
    cont = input('Do you want to continue [y/n]: ')
    if cont != 'y':
        break