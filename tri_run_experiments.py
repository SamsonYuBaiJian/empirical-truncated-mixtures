import trivariate
import numpy as np
import os
import argparse

def main():
    all_est_means = []
    learning_rate = 0.01
    
    path = './graphs/3d_random_points_error_vs_step'
    if not os.path.exists(path):
        os.makedirs(path)

    # parameters
    epsilon = 0.1
    step_limit = 10000
    # num_of_points = 100
    num_of_points = 10
    seed = 42
    np.random.seed(seed)
    true_means = (5, 2, 1)
    # s_intervals = [(-2, 2), (-2, 2)]
    print_every = 10

    x_points = np.random.uniform(-7,7,num_of_points)
    y_points = np.random.uniform(-7,7,num_of_points)
    z_points = np.random.uniform(-7,7,num_of_points)
    all_est_means = []
    final_error_list = [0] * step_limit

    print("Doing " + str(num_of_points) + " random points for 3D Error vs Step experiment...")
    for i in range(num_of_points):
        est_means = (x_points[i],y_points[i],z_points[i])

        step_list, error_list = trivariate.run(learning_rate, true_means, est_means, epsilon)
        
        all_est_means.append(est_means)
        for j in range(step_limit):
            final_error_list[j] += error_list[j]
        if (i + 1) % print_every == 0:
            print(str(i + 1) + "/" + str(num_of_points) + " random point(s) done.")
    for i in range(step_limit):
        final_error_list[i] /= num_of_points

    # save metrics
    experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if len(experiment_nos) == 0:
        target_no = 1
    else:
        target_no = max(experiment_nos) + 1
    f = open(path + '/experiment-' + str(target_no), 'w')
    save_dict = {}
    save_dict['steps'] = step_list
    save_dict['errors'] = final_error_list
    save_dict['learning_rate'] = str(learning_rate)
    save_dict['true_means'] = str(true_means)
    save_dict['est_means'] = all_est_means
    # save_dict['s_intervals'] = str(s_intervals)
    save_dict['step_limit'] = str(step_limit)
    save_dict['num_of_points'] = str(num_of_points)
    save_dict['seed'] = str(seed)
    f.write(str(save_dict))
    f.close()
    print("Done.")


if __name__ == '__main__':
    if not os.path.exists('./graphs'):
        os.makedirs('./graphs')

    main()