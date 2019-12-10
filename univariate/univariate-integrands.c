#include <math.h>

// user_data = (current, real_mean)

double top_1(int n, double *x, double *user_data){
	return ( x[0]*x[0] -  x[0]*x[0]*tanh(x[0] * user_data[0])*tanh(x[0] * user_data[0]) ) * (exp(-0.5 * (x[0] - user_data[1])*(x[0] - user_data[1]) ) + exp(-0.5 * (x[0] + user_data[1])*(x[0] + user_data[1]) ));
}

double top_2(int n, double *x, double *user_data){
	return x[0]*x[0] * (exp(-0.5 * (x[0] - user_data[0])*(x[0] - user_data[0]) ) + exp(-0.5 * (x[0] + user_data[0])*(x[0] + user_data[0]) ));
}

double top_3(int n, double *x, double *user_data){
	return x[0]* tanh(x[0] * user_data[0]) * (exp(-0.5 * (x[0] - user_data[0])*(x[0] - user_data[0]) ) + exp(-0.5 * (x[0] + user_data[0])*(x[0] + user_data[0]) ));
}

double bottom_real(int n, double *x, double *user_data){
	return exp(-0.5 * (x[0] - user_data[1])*(x[0] - user_data[1])) + exp(-0.5 * (x[0] + user_data[1])*(x[0] + user_data[1]));
}

double bottom_est(int n, double *x, double *user_data){
	return exp(-0.5 * (x[0] - user_data[0])*(x[0] - user_data[0])) + exp(-0.5 * (x[0] + user_data[0])*(x[0] + user_data[0]));
}
