#include <math.h>
#include <stdio.h>

double top_x_real(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return x[0] * tanh(x[0] * c[0] + x[1] * c[1] + x[2] * c[2]) * (1 / sqrt(pow((2 * M_PI),3))) *
		(exp(-0.5 * ((x[0] - c[3])*(x[0] - c[3]) + (x[1] - c[4])*(x[1] - c[4]) + (x[2] - c[5])*(x[2] - c[5])))
		+ exp(-0.5 * ((x[0] + c[3])*(x[0] + c[3]) + (x[1] + c[4])*(x[1] + c[4]) + (x[2] + c[5])*(x[2] + c[5])))) / c[6];
}

double top_y_real(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return x[1] * tanh(x[0] * c[0] + x[1] * c[1] + x[2] * c[2]) * (1 / sqrt(pow((2 * M_PI),3))) *
		(exp(-0.5 * ((x[0] - c[3])*(x[0] - c[3]) + (x[1] - c[4])*(x[1] - c[4]) + (x[2] - c[5])*(x[2] - c[5])))
		+ exp(-0.5 * ((x[0] + c[3])*(x[0] + c[3]) + (x[1] + c[4])*(x[1] + c[4]) + (x[2] + c[5])*(x[2] + c[5])))) / c[6];
}

double top_z_real(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return x[2] * tanh(x[0] * c[0] + x[1] * c[1] + x[2] * c[2]) * (1 / sqrt(pow((2 * M_PI),3))) *
		(exp(-0.5 * ((x[0] - c[3])*(x[0] - c[3]) + (x[1] - c[4])*(x[1] - c[4]) + (x[2] - c[5])*(x[2] - c[5])))
		+ exp(-0.5 * ((x[0] + c[3])*(x[0] + c[3]) + (x[1] + c[4])*(x[1] + c[4]) + (x[2] + c[5])*(x[2] + c[5])))) / c[6];
}

double top_x_est(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return x[0] * tanh(x[0] * c[0] + x[1] * c[1] + x[2] * c[2]) * (1 / sqrt(pow((2 * M_PI),3))) *
		(exp(-0.5 * ((x[0] - c[0])*(x[0] - c[0]) + (x[1] - c[1])*(x[1] - c[1]) + (x[2] - c[2])*(x[2] - c[2])))
		+ exp(-0.5 * ((x[0] + c[0])*(x[0] + c[0]) + (x[1] + c[1])*(x[1] + c[1]) + (x[2] + c[2])*(x[2] + c[2])))) / c[6];
}

double top_y_est(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return x[1] * tanh(x[0] * c[0] + x[1] * c[1] + x[2] * c[2]) * (1 / sqrt(pow((2 * M_PI),3))) *
		(exp(-0.5 * ((x[0] - c[0])*(x[0] - c[0]) + (x[1] - c[1])*(x[1] - c[1]) + (x[2] - c[2])*(x[2] - c[2])))
		+ exp(-0.5 * ((x[0] + c[0])*(x[0] + c[0]) + (x[1] + c[1])*(x[1] + c[1]) + (x[2] + c[2])*(x[2] + c[2])))) / c[6];
}

double top_z_est(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return x[2] * tanh(x[0] * c[0] + x[1] * c[1] + x[2] * c[2]) * (1 / sqrt(pow((2 * M_PI),3))) *
		(exp(-0.5 * ((x[0] - c[0])*(x[0] - c[0]) + (x[1] - c[1])*(x[1] - c[1]) + (x[2] - c[2])*(x[2] - c[2])))
		+ exp(-0.5 * ((x[0] + c[0])*(x[0] + c[0]) + (x[1] + c[1])*(x[1] + c[1]) + (x[2] + c[2])*(x[2] + c[2])))) / c[6];
}

double bottom(int n, double *x, void *user_data){
	double *c = (double *)user_data;
	return (1 / sqrt(pow((2 * M_PI),3))) * (exp(-0.5 * ((x[0] - c[0])*(x[0] - c[0]) + (x[1] - c[1])*(x[1] - c[1]) + (x[2] - c[2])*(x[2] - c[2]))) +
		exp(-0.5 * ((x[0] + c[0])*(x[0] + c[0]) + (x[1] + c[1])*(x[1] + c[1]) + (x[2] + c[2])*(x[2] + c[2]))));
}

double tetra(int n, double *x, void *user_data){
	return 1.;
}

double para(int n, double *x, void *user_data){
	return 1.;
}