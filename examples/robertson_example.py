try:
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plot = True
except ImportError:
    plot = False
    pass

import numpy as np

from pysb.examples.robertson import model
from pysb.simulator import ScipyOdeSimulator
from simplepso.pso import PSO

obs_names = ['A_total', 'C_total']


# Defining a few helper functions to use
def normalize(trajectories):
    """Rescale a matrix of model trajectories to 0-1"""
    ymin = trajectories.min(0)
    ymax = trajectories.max(0)
    return (trajectories - ymin) / (ymax - ymin)


t = np.linspace(0, 40, 101)

solver = ScipyOdeSimulator(
    model,
    t,
    integrator='lsoda',
    integrator_options={'rtol': 1e-8, 'atol': 1e-8}
)
traj = solver.run()

# Creating ideal data
ysim_array = traj.dataframe[obs_names].values
norm_data = normalize(ysim_array)

# np.random.seed(0)
noise = 0.01
# Creating noisy data
noisy_data_A = ysim_array[:, 0] + np.random.uniform(-noise, noise, len(t))
norm_noisy_data_A = normalize(noisy_data_A)
noisy_data_C = ysim_array[:, 1] + np.random.uniform(-noise, noise, len(t))
norm_noisy_data_C = normalize(noisy_data_C)
ydata_norm = np.column_stack((norm_noisy_data_A, norm_noisy_data_C))

rate_params = model.parameters_rules()
param_values = np.array([p.value for p in model.parameters])
rate_mask = np.array([p in rate_params for p in model.parameters])

original_values = np.array([p.value for p in model.parameters])

# We search in log10 space for the parameters
log10_original_values = np.log10(original_values[rate_mask])

# We will use a best guess starting position for the model, up or down 1 order of magnitude
start_position = log10_original_values + [-1.5, 1.3, -.75]


# np.random.uniform(-1.5, 1.5, size=np.shape(log10_original_values))


# Defining some functions to help plot the output of the parameters
def display(parameter_1, parameter_2):
    Y = np.copy(parameter_1)
    param_values[rate_mask] = 10 ** Y
    traj = solver.run(param_values=param_values)
    ysim_array_1 = traj.dataframe[obs_names].values
    ysim_norm_1 = normalize(ysim_array_1)
    Y = np.copy(parameter_2)
    param_values[rate_mask] = 10 ** Y
    traj = solver.run(param_values=param_values)
    ysim_array_2 = traj.dataframe[obs_names].values
    ysim_norm_2 = normalize(ysim_array_2)

    param_values[rate_mask] = 10 ** log10_original_values
    traj = solver.run(param_values=param_values)
    ysim_array_3 = traj.dataframe[obs_names].values
    ysim_norm_3 = normalize(ysim_array_3)

    plt.figure()
    plt.subplot(111)
    plt.plot(t, ysim_norm_3[:, 0], 'r-^', linewidth=5, label='Ideal A')
    plt.plot(t, ysim_norm_3[:, 1], 'k-^', linewidth=5, label='Ideal C')
    plt.plot(t, ysim_norm_1[:, 0], 'r->', label='Starting A')
    plt.plot(t, ysim_norm_1[:, 1], 'k->', label='Starting C')
    plt.plot(t, norm_noisy_data_A, label='Noisy A')
    plt.plot(t, norm_noisy_data_C, label='Noisy C')
    plt.plot(t, ysim_norm_2[:, 0], 'r-o', label='Best fit A')
    plt.plot(t, ysim_norm_2[:, 1], 'k-o', label='Best fit C')
    plt.legend(loc=0)
    plt.ylabel('concentration')
    plt.xlabel('time (s)')
    plt.tight_layout()
    plt.savefig('results.png')
    plt.show()
    plt.close()


'''
Here we define the cost function. We pass it the parameter vector, unlog it,
and pass it to the solver. We choose a chi square cost function, but you can 
provide any metric of you choosing
'''


def obj_function(params):
    params_tmp = np.copy(params)
    param_values[rate_mask] = 10 ** params_tmp
    traj = solver.run(param_values=param_values)
    ysim_array = traj.dataframe[obs_names].values
    ysim_norm = normalize(ysim_array)
    err = np.sum((ydata_norm - ysim_norm) ** 2)
    return err


def run_example():
    # Here we initial the class
    # We must proivde the cost function and a starting value
    optimizer = PSO(cost_function=obj_function, start=start_position,
                    verbose=True, shrink_steps=True)
    # We also must set bounds. This can be a single scalar or an array of len(start_position)
    optimizer.set_bounds(parameter_range=3)
    optimizer.set_speed(speed_min=-.5, speed_max=.5)
    optimizer.run(num_particles=20, num_iterations=100, num_processes=12)
    if plot:
        display(start_position, optimizer.best.pos)

        print("Original values {0}".format(log10_original_values ** 10))
        print("Starting values {0}".format(start_position ** 10))
        print("Best PSO values {0}".format(optimizer.best.pos ** 10))
        fig = plt.figure()
        fig.add_subplot(221)
        plt.scatter(log10_original_values[0], log10_original_values[1],
                    marker='>', color='b', label='ideal')
        plt.scatter(start_position[0], start_position[1], marker='^',
                    color='r', label='start')
        plt.scatter(optimizer.history[:, 0], optimizer.history[:, 1],
                    c=optimizer.values, cmap=plt.cm.coolwarm)

        fig.add_subplot(223)
        plt.scatter(log10_original_values[0], log10_original_values[2],
                    marker='>', color='b', label='ideal')
        plt.scatter(start_position[0], start_position[2], marker='^',
                    color='r', label='start')
        plt.scatter(optimizer.history[:, 0], optimizer.history[:, 2],
                    c=optimizer.values, cmap=plt.cm.coolwarm)

        fig.add_subplot(222)
        plt.scatter(log10_original_values[1], log10_original_values[2],
                    marker='>', color='b', label='ideal')
        plt.scatter(start_position[1], start_position[2], marker='^',
                    color='r', label='start')
        plt.scatter(optimizer.history[:, 1], optimizer.history[:, 2],
                    c=optimizer.values, cmap=plt.cm.coolwarm)

        fig.add_subplot(224)
        plt.legend(loc=0)
        plt.colorbar()
        plt.tight_layout()
        plt.savefig('population.png')


if '__main__' == __name__:
    run_example()
