import bivariate
import numpy as np
import os
import argparse
import time

def main(exp_type):
    all_est_means = []
    learning_rate = 0.01
    

    if exp_type == '3d_random_points_error_vs_step':
        path = './graphs/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)

        # parameters
        epsilon = 0.1
        step_limit = 10000
        # num_of_points = 100
        num_of_points = 1
        seed = 42
        np.random.seed(seed)
        true_means = (5, 2, 1)
        # s_intervals = [(-2, 2), (-2, 2)]
        print_every = 10

        points_1 = np.random.uniform(-7,7,num_of_points)
        points_2 = np.random.uniform(-7,7,num_of_points)
        all_est_means = []
        final_error_list = [0] * step_limit

        print("Doing " + str(num_of_points) + " random points for 3D Error vs Step experiment...")
        for i in range(num_of_points):
            est_means = (points_1[i],points_2[i])
            step_list, error_list = bivariate.run(exp_type, learning_rate, true_means, est_means, s_intervals, epsilon)
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
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['step_limit'] = str(step_limit)
        save_dict['num_of_points'] = str(num_of_points)
        save_dict['seed'] = str(seed)
        f.write(str(save_dict))
        f.close()
        print("Done.")


    # for 2D Error vs Step experiment with random points from uniform distribution
    if exp_type == 'random_points_error_vs_step':
        path = './graphs/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)

        # parameters
        epsilon = 0.1
        step_limit = 12000
        num_of_points = 50
        seed = 42
        np.random.seed(seed)
        # true_means = (2.534, 6.395)
        # s_intervals = [(1, 2), (-3, 1.5)]
        true_means = (2, 1)
        s_intervals = [(-2, 2), (-2, 2)]
        print_every = 10

        points_1 = np.random.uniform(-7,7,num_of_points)
        points_2 = np.random.uniform(-7,7,num_of_points)
        all_est_means = []
        full_error_list = []
        average_error_list = [0] * step_limit

        print("Doing " + str(num_of_points) + " random points for 2D Error vs Step experiment...")
        for i in range(num_of_points):
            start_time = time.time()
            est_means = (points_1[i],points_2[i])
            step_list, error_list = bivariate.run(exp_type, learning_rate, true_means, est_means, s_intervals, epsilon)
            all_est_means.append(est_means)
            for j in range(step_limit):
                average_error_list[j] += error_list[j]
            full_error_list.append(error_list)
            current_time = time.time()
            time_elapsed = current_time - start_time
            print(time_elapsed)
            if (i + 1) % print_every == 0:
                print(str(i + 1) + "/" + str(num_of_points) + " random point(s) done.")
        for i in range(step_limit):
            average_error_list[i] /= num_of_points

        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['steps'] = step_list
        save_dict['average_error_list'] = average_error_list
        save_dict['full_error_list'] = full_error_list
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = all_est_means
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['step_limit'] = str(step_limit)
        save_dict['num_of_points'] = str(num_of_points)
        save_dict['seed'] = str(seed)
        f.write(str(save_dict))
        f.close()
        print("Done.")


    # for histogram and scatter with random points from uniform distribution
    elif exp_type == 'random_points_epsilon_and_step':
        path = './graphs/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)
        all_epsilon_steps = []

        # parameters
        epsilon = 0.1
        num_of_points = 100
        seed = 42
        np.random.seed(seed)
        true_means = (2.534, 6.395)
        s_intervals = [(1, 2), (-3, 1.5)]
        print_every = 10

        points_1 = np.random.uniform(-7,7,num_of_points)
        points_2 = np.random.uniform(-7,7,num_of_points)
        all_est_means = []

        print("Doing " + str(num_of_points) + " random points for histogram and scatterplot experiments...")
        for i in range(num_of_points):
            est_means = (points_1[i],points_2[i])
            epsilon_step = bivariate.run(exp_type, learning_rate, true_means, est_means, s_intervals, epsilon)
            all_est_means.append(est_means)
            all_epsilon_steps.append(epsilon_step)
            if (i + 1) % print_every == 0:
                print(str(i + 1) + "/" + str(num_of_points) + " random point(s) done.")

        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['epsilon_steps'] = all_epsilon_steps
        save_dict['max_epsilon_step'] = str(max(all_epsilon_steps))
        save_dict['min_epsilon_step'] = str(min(all_epsilon_steps))
        save_dict['avg_epsilon_step'] = str(sum(all_epsilon_steps) / len(all_epsilon_steps))
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = all_est_means
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        save_dict['num_of_points'] = str(num_of_points)
        save_dict['seed'] = str(seed)
        f.write(str(save_dict))
        f.close()
        print("Done.")


    # for experiments with single point, varying S intervals
    elif exp_type == 'single_point_vary_s':
        path = './graphs/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)
        all_epsilon_steps = []
        all_denominators = []

        # parameters
        epsilon = 0.1
        interval_change = 0.5
        interval_increase = 20
        # est_means = (2.4, 6.2)
        est_means = (0.9, 0.1)
        true_means = (2.534, 6.395)
        s_intervals = [(1, 2), (-3, 1.5)]
        # est_means = (3, 2)
        # true_means = (2, 1)
        # s_intervals = [(-2, 2), (-2, 2)]

        x_interval_start = s_intervals[0][1]
        x_intervals = np.arange(x_interval_start, x_interval_start + interval_increase + interval_change, interval_change)
        y_interval_start = s_intervals[1][1]
        y_intervals = np.arange(y_interval_start, y_interval_start + interval_increase + interval_change, interval_change)
        
        print("Doing a single point for interval varying experiment...")
        for i in range(len(x_intervals)):
            s_intervals[0] = (s_intervals[0][0], round(x_intervals[i],1))
            s_intervals[1] = (s_intervals[1][0], round(y_intervals[i],1))
            epsilon_step, denominator = bivariate.run(exp_type, learning_rate, true_means, est_means, s_intervals, epsilon)
            all_epsilon_steps.append(epsilon_step)
            all_denominators.append(denominator)

        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['epsilon_steps'] = all_epsilon_steps
        save_dict['denominators'] = all_denominators
        save_dict['max_epsilon_step'] = str(max(all_epsilon_steps))
        save_dict['min_epsilon_step'] = str(min(all_epsilon_steps))
        save_dict['avg_epsilon_step'] = str(sum(all_epsilon_steps) / len(all_epsilon_steps))
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = str(true_means)
        save_dict['est_means'] = str(est_means)
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        f.write(str(save_dict))
        f.close()
        print("Done.")


    # for trajectory experiments
    elif exp_type == 'trajectory':
        path = './graphs/' + exp_type
        if not os.path.exists(path):
            os.makedirs(path)

        # parameters
        epsilon = 0.05
        est_means = [
            (0.95, 0.05),
            (-0.05, 0.05),
            (2, 6),
            (4, 1.5),
            (-1.5, 8)
        ]
        true_means = (2.534, 6.395)
        s_intervals = [(1, 2), (-3, 1.5)]

        print("Doing trajectory experiments...")
        all_est_means = []
        for i in range(len(est_means)):
            all_est_means_for_point = bivariate.run(exp_type, learning_rate, true_means, est_means[i], s_intervals, epsilon)
            all_est_means.append(all_est_means_for_point)

        # save metrics
        experiment_nos = [int(f.split('-')[-1]) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(experiment_nos) == 0:
            target_no = 1
        else:
            target_no = max(experiment_nos) + 1
        f = open(path + '/experiment-' + str(target_no), 'w')
        save_dict = {}
        save_dict['learning_rate'] = str(learning_rate)
        save_dict['true_means'] = true_means
        save_dict['all_est_means'] = all_est_means
        save_dict['est_means'] = est_means
        save_dict['s_intervals'] = str(s_intervals)
        save_dict['epsilon'] = str(epsilon)
        f.write(str(save_dict))
        f.close()
        print("Done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_type', required=True)
    args = parser.parse_args()

    if not os.path.exists('./graphs'):
        os.makedirs('./graphs')

    main(args.exp_type)