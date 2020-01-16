import ast
import matplotlib.pyplot as plt
import math
import seaborn as sns

def euclidean_distance(real, est):
    return math.sqrt(pow((real[0] - est[0]),2) + pow((real[1] - est[1]),2))

data_file_path = './random-points/experiment-1'

data_dict = open(str(data_file_path), 'r').readlines()
data_dict = ast.literal_eval(data_dict[0])

# get histogram
plt.hist(data_dict['fixed_error_steps'])
plt.show()

# get scatter plot
distances = []
real = ast.literal_eval(data_dict['real_means'])

for est_point in data_dict['points']:
    distances.append(euclidean_distance(real, est_point))

sns.regplot(distances, data_dict['fixed_error_steps'])
plt.show()