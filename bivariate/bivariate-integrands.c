#include <math.h>

double top_x1_real(int n, double *x, double *user_data){
	return x[0] * tanh(x[0] * user_data[0] + x[1] * user_data[1]) * (exp(-0.5 * ((x[0] - user_data[2])*(x[0] - user_data[2]) + (x[1] - user_data[3])*(x[1] - user_data[3]))) + exp(-0.5 * ((x[0] + user_data[2])*(x[0] + user_data[2]) + (x[1] + user_data[3])*(x[1] + user_data[3]))));
}

double top_x2_real(int n, double *x, double *user_data){
	return x[1] * tanh(x[0] * user_data[0] + x[1] * user_data[1]) * (exp(-0.5 * ((x[0] - user_data[2])*(x[0] - user_data[2]) + (x[1] - user_data[3])*(x[1] - user_data[3]))) + exp(-0.5 * ((x[0] + user_data[2])*(x[0] + user_data[2]) + (x[1] + user_data[3])*(x[1] + user_data[3]))));
}

double bottom_real(int n, double *x, double *user_data){
	return exp(-0.5 * ((x[0] - user_data[2])*(x[0] - user_data[2]) + (x[1] - user_data[3])*(x[1] - user_data[3]))) + exp(-0.5 * ((x[0] + user_data[2])*(x[0] + user_data[2]) + (x[1] + user_data[3])*(x[1] + user_data[3])));
}

double top_x1_est(int n, double *x, double *user_data){
	return x[0] * tanh(x[0] * user_data[0] + x[1] * user_data[1]) * (exp(-0.5 * ((x[0] - user_data[0])*(x[0] - user_data[0]) + (x[1] - user_data[1])*(x[1] - user_data[1]))) + exp(-0.5 * ((x[0] + user_data[0])*(x[0] + user_data[0]) + (x[1] + user_data[1])*(x[1] + user_data[1]))));
}

double top_x2_est(int n, double *x, double *user_data){
	return x[1] * tanh(x[0] * user_data[0] + x[1] * user_data[1]) * (exp(-0.5 * ((x[0] - user_data[0])*(x[0] - user_data[0]) + (x[1] - user_data[1])*(x[1] - user_data[1]))) + exp(-0.5 * ((x[0] + user_data[0])*(x[0] + user_data[0]) + (x[1] + user_data[1])*(x[1] + user_data[1]))));
}

double bottom_est(int n, double *x, double *user_data){
	return exp(-0.5 * ((x[0] - user_data[0])*(x[0] - user_data[0]) + (x[1] - user_data[1])*(x[1] - user_data[1]))) + exp(-0.5 * ((x[0] + user_data[0])*(x[0] + user_data[0]) + (x[1] + user_data[1])*(x[1] + user_data[1])));
}

