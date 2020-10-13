import ast
import matplotlib.pyplot as plt
from math import sqrt
import seaborn as sns
import argparse
import matplotlib.patches as patches


def euclidean_distance(real, est):
    distance_list = []
    est_x1 = est[0]
    est_x2 = est[1]
    distance_list.append(sqrt(pow((real[0] - (-est_x1)), 2) + pow((real[1] - est_x2), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x1), 2) + pow((real[1] - (-est_x2)), 2)))
    distance_list.append(sqrt(pow((real[0] - est_x1), 2) + pow((real[1] - est_x2), 2)))
    distance_list.append(sqrt(pow((real[0] - (-est_x1)), 2) + pow((real[1] - (-est_x2)), 2)))
    return min(distance_list)

def main(exp_type, data_file_path, graph_type):
    if exp_type == 'random_points_epsilon_and_step':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        # get histogram
        plt.hist(data_dict['epsilon_steps'])
        if graph_type == 'title':
            plt.title("Epsilon Steps")
        elif graph_type == 'axes':
            pass
        plt.show()

        # get scatter plot
        distances = []
        true_mean = ast.literal_eval(data_dict['true_means'])

        for est_mean in data_dict['est_means']:
            distances.append(euclidean_distance(true_mean, est_mean))

        sns.regplot(distances, data_dict['epsilon_steps'])
        if graph_type == 'title':
            plt.title("Epsilon Step vs. Initial Distance")
        elif graph_type == 'axes':
            pass
        plt.show()

    elif exp_type == 'single_point_vary_s':
        # get graph for interval stretch
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        if graph_type == 'title':
            plt.title('Epsilon Step vs. Denominator')
        elif graph_type == 'axes':
            plt.xlabel('Measure of Truncated Set', fontsize=14)
            plt.ylabel('No of Steps for Convergence', fontsize=14)
        plt.plot(data_dict['denominators'], data_dict['epsilon_steps'])
        plt.show()

    elif exp_type == '3d_random_points_error_vs_step':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        if graph_type == 'title':
            plt.title('3D Error vs. Step')
        elif graph_type == 'axes':
            plt.xlabel('No of Steps', fontsize=14)
            plt.ylabel('Error with respect to True Mean', fontsize=14)
        plt.plot(data_dict['steps'], data_dict['average_error_list'])
        plt.show()

    elif exp_type == 'random_points_error_vs_step':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        if graph_type == 'title':
            plt.title('2D Error vs. Step')
        elif graph_type == 'axes':
            plt.xlabel('No of Steps', fontsize=14)
            plt.ylabel('Error with respect to True Mean', fontsize=14)
        plt.plot(data_dict['steps'], data_dict['errors'])
        plt.show()

    elif exp_type == 'trajectory':
        data_dict = open(str(data_file_path), 'r').readlines()
        data_dict = ast.literal_eval(data_dict[0])

        true_means = data_dict['true_means']
        est_means = data_dict['est_means']
        lambda_means = (1,0)

        # plot setup
        fig = plt.figure()
        plt.rcParams.update({'mathtext.default':  'regular' })
        if graph_type == 'title':
            plt.title('Trajectory')
        elif graph_type == 'axes':
            plt.xlabel('x', fontsize=14)
            plt.ylabel('y', fontsize=14)

        # plot
        plt.annotate("γ", (lambda_means[0] + .1, lambda_means[1] - .25))
        plt.plot(lambda_means[0], lambda_means[1], "ko", markersize=2)
        plt.annotate("μ", (true_means[0] + .1, true_means[1]))
        plt.plot(true_means[0], true_means[1], "ko", markersize=4)

        for i in range(len(est_means)):
            x_list = []
            y_list = []
            for j in data_dict['all_est_means'][i]:
                x_list.append(j[0])
                y_list.append(j[1])
            plt.plot(x_list, y_list)
            start_est_means = est_means[i]
            if i == 0:
                plt.annotate("$λ_0^" + str(i+1) + "$:" + str(est_means[i]), (start_est_means[0] - .7, start_est_means[1] - .9))
            else:
                plt.annotate("$λ_0^" + str(i+1) + "$:" + str(est_means[i]), (start_est_means[0] - .9, start_est_means[1] + .3))
            plt.plot(start_est_means[0], start_est_means[1], "ro", markersize=2)
            plt.arrow(data_dict['all_est_means'][i][-2][0], data_dict['all_est_means'][i][-2][1], 
                data_dict['all_est_means'][i][-1][0] - data_dict['all_est_means'][i][-2][0], data_dict['all_est_means'][i][-1][1] - data_dict['all_est_means'][i][-2][1],
                head_width=0.1, length_includes_head=True)

        # rectangle patch
        interval_rect = patches.Rectangle((1, -3), 1, 4.5, linewidth=1, edgecolor='r', facecolor='none')
        ax = fig.add_subplot()
        ax.add_patch(interval_rect)

        # axes limits
        plt.xlim([-2.75, 5.75])
        plt.ylim([-5, 11])

        plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_type')
    parser.add_argument('--data_file_path')
    parser.add_argument('--graph_type')
    args = parser.parse_args()

    main(args.exp_type, args.data_file_path, args.graph_type)