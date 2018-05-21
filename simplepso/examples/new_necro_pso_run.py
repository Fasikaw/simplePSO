from pysb.core import *
from pysb.bng import *
from pysb.integrate import *
import matplotlib.pyplot as plt
import numpy as np
from pysb.util import alias_model_components
from necroptosismodule import model

from necro_pso_kd_plot import display

model.enable_synth_deg()

pars =  np.load('optimizer_best_5000_all_new_2.npy')

pars = np.append(pars, 1.0)
params = 10 ** pars
params = np.concatenate([initials1, params])


tspan = np.linspace(0, 1200, 1201)
sim1 = ScipyOdeSimulator(model, tspan=tspan)
sim2 = ScipyOdeSimulator(model, tspan=tspan)
L4 = sim1.run(param_values=params)
L3 = sim2.run()


plt.figure()
# plt.plot(tspan/60, L3.observables['MLKLa_obs'],color = 'purple',label = 'MLKLp')
plt.plot(tspan/60, sim_result1.observables['MLKLa_obs'],label = '100 ng/ml TNF')
plt.plot(tspan/60, sim_result2.observables['MLKLa_obs'],label = '10 ng/ml TNF')
plt.plot(tspan/60, sim_result3.observables['MLKLa_obs'],label = '1 ng/ml TNF')
plt.plot(tspan/60, sim_result4.observables['MLKLa_obs'],label = '0.1 ng/ml TNF')
# plt.plot(tspan/60, L3.observables['MLKL_obs'],color = 'red',label = 'MLKL')
# plt.plot(tspan/60, L4.observables['MLKL_obs'],color = 'red',label = 'MLKL_cal')
# plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("MLKLp [Molecules/Cell]", fontsize=15)
plt.title('MLKLp Trajectories')
plt.legend(loc ='best')
# plt.show()


print(L3.observables['C8a_obs'][:])
print(L4.observables['RIP13_obs'][:])

quit()

plt.figure(figsize = (18,7))
# # plt.figure()
plt.subplot(231)
# # plt.plot(tspan/60, L1.observables['TNF_obs'],label = 'TNF.1')
# # plt.plot(tspan/60, L2.observables['TNF_obs'],label = 'TNF1')
plt.plot(tspan/60, L3.observables['TNF_obs'],label = 'TNF')
plt.plot(tspan/60, L4.observables['TNF_obs'],label = 'TNFcal')
#
# plt.plot(tspan/60, simulation_result.observables['TNF_obs'], color = 'r', label = 'TNF_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
# plt.ylim(ymin = -10, ymax =100)
plt.legend(loc=0)
#
# # plt.figure()
plt.subplot(232)
# # plt.plot(tspan/60, simulation_result.observables['CI_k63_obs'],label = 'CI_k63')
# # plt.plot(tspan/60, L1.observables['CI_k63_obs'],label = 'CI_k63.1')
# # plt.plot(tspan/60, L2.observables['CI_k63_obs'],label = 'CI_k631')
plt.plot(tspan/60, L3.observables['CI_k63_obs'],label = 'CI_k63')
plt.plot(tspan/60, L4.observables['CI_k63_obs'],label = 'CI_k63cal')
# plt.plot(tspan/60, simulation_result.observables['CI_k63_obs'],label = 'CI_k63')
# plt.plot(tspan/60, simulation_result.observables['CI_k63_obs'],label = 'CI_k63')
# plt.plot(tspan/60, simulation_result.observables['TNFR_obs'], color = 'r', label = 'TNFR_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
# plt.ylim(ymin = -10, ymax =100)
plt.legend(loc=0)
# #
# # plt.figure()
plt.subplot(233)
# plt.plot(tspan/60, L1.observables['RIP13po4_obs'],label = 'RIP13po4.1')
# plt.plot(tspan/60, L3.observables['RIP13po4_obs'],label = 'RIP13po4_obs')
plt.plot(tspan/60, L3.observables['RIP13_obs'],label = 'RIP13')
plt.plot(tspan/60, L4.observables['RIP13_obs'],label = 'RIP13cal')

# plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
# plt.ylim(ymin = -10, ymax =100)
plt.legend(loc=0)

plt.subplot(234)
# plt.plot(tspan/60, L3.observables['RIP1deub_obs'],label = 'RIP1deub_obs')
# plt.plot(tspan/60, L3.observables['RIP1k63_obs'],label = 'RIP1k63_obs')
plt.plot(tspan/60, L3.observables['CI'],label = 'CI')
plt.plot(tspan/60, L4.observables['CI'],label = 'CIcal')
# plt.plot(tspan/60, L4.observables['MLKLa_obs'],label = 'MLKLpcal')
# # plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
plt.legend(loc = 0)

plt.subplot(235)
# plt.plot(tspan/60, L1.observables['MLKLa_obs'],label = 'MLKLa.1')
# plt.plot(tspan/60, L2.observables['MLKLa_obs'],label = 'MLKLa1')
plt.plot(tspan/60, L3.observables['C8a_obs'],label = 'C8a')
plt.plot(tspan/60, L4.observables['C8a_obs'],label = 'C8acal')
# plt.plot(tspan/60, L4.observables['MLKLa_obs'],label = 'MLKLpcal')
# # plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
plt.legend(loc = 0)


plt.subplot(236)
# plt.plot(tspan/60, L1.observables['MLKLa_obs'],label = 'MLKLa.1')
# plt.plot(tspan/60, L2.observables['MLKLa_obs'],label = 'MLKLa1')
plt.plot(tspan/60, L3.observables['MLKLa_obs'],label = 'MLKLp')
# plt.plot(tspan/60, L4.observables['CIIa_obs'],label = 'CIIa')
plt.plot(tspan/60, L4.observables['MLKLa_obs'],label = 'MLKLpcal')
# # plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
plt.legend(loc = 0)



plt.figure(figsize = (18,7))
# # plt.figure()
plt.subplot(221)
# # plt.plot(tspan/60, L1.observables['TNF_obs'],label = 'TNF.1')
# # plt.plot(tspan/60, L2.observables['TNF_obs'],label = 'TNF1')
plt.plot(tspan/60, L3.observables['A20_obs'],label = 'A20')
plt.plot(tspan/60, L4.observables['A20_obs'],label = 'A20cal')
#
# plt.plot(tspan/60, simulation_result.observables['TNF_obs'], color = 'r', label = 'TNF_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
# plt.ylim(ymin = -10, ymax =100)
plt.legend(loc=0)
#
# # plt.figure()
plt.subplot(222)
# # plt.plot(tspan/60, simulation_result.observables['CI_k63_obs'],label = 'CI_k63')
# # plt.plot(tspan/60, L1.observables['CI_k63_obs'],label = 'CI_k63.1')
# # plt.plot(tspan/60, L2.observables['CI_k63_obs'],label = 'CI_k631')
plt.plot(tspan/60, L3.observables['Fadd_obs'],label = 'Fadd')
plt.plot(tspan/60, L4.observables['Fadd_obs'],label = 'Faddcal')
# plt.plot(tspan/60, simulation_result.observables['CI_k63_obs'],label = 'CI_k63')
# plt.plot(tspan/60, simulation_result.observables['CI_k63_obs'],label = 'CI_k63')
# plt.plot(tspan/60, simulation_result.observables['TNFR_obs'], color = 'r', label = 'TNFR_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
# plt.ylim(ymin = -10, ymax =100)
plt.legend(loc=0)
# #
# # plt.figure()
plt.subplot(223)
# plt.plot(tspan/60, L1.observables['RIP13po4_obs'],label = 'RIP13po4.1')
# plt.plot(tspan/60, L3.observables['RIP13po4_obs'],label = 'RIP13po4_obs')
plt.plot(tspan/60, L3.observables['Tradd_obs'],label = 'Tradd')
plt.plot(tspan/60, L4.observables['Tradd_obs'],label = 'Traddcal')

# plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
# plt.ylim(ymin = -10, ymax =100)
plt.legend(loc=0)

plt.subplot(224)
# plt.plot(tspan/60, L3.observables['RIP1deub_obs'],label = 'RIP1deub_obs')
# plt.plot(tspan/60, L3.observables['RIP1k63_obs'],label = 'RIP1k63_obs')
plt.plot(tspan/60, L3.observables['C8i_obs'],label = 'C8a')
plt.plot(tspan/60, L4.observables['C8i_obs'],label = 'C8acal')
# plt.plot(tspan/60, L4.observables['MLKLa_obs'],label = 'MLKLpcal')
# # plt.plot(tspan/60, simulation_result.observables['IKKa_obs'], color = 'r', label = 'IKKa_mat')
plt.xlabel("Time (in hr)", fontsize=15)
plt.ylabel("Molecules/Cell", fontsize=15)
plt.legend(loc = 0)


plt.tight_layout()
plt.show()
#
