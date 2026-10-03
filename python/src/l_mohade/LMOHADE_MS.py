#encoding: utf-8
import jmetal.operator
import numpy as np
from public import init, plot, update, P_objective
from public import constants_30unit as deed
import time
class LMOHADE_MS:
    def __init__(self,particals,max_,min_,thresh,mesh_div=10, LH=10000, L=0.08):


        self.mesh_div = mesh_div
        self.particals = particals
        self.thresh = thresh
        self.max_ = max_
        self.min_ = min_
        self.LH = LH
        self.L = L
        self.shrink = 0
        self.total_hunger = 0
        self.eps = 10E-10
        self.m = 0
        self.S = 0
        self.cur_iter = 0
        self.cr = np.ones(particals) * .9
        self.T1 = 0.1
        self.T2 = 0.1
        self.probability = 1 / 2
        self.distribution_index = 20
        self.proC = 1
        self.disC = 20
        self.proM = 1
        self.disM = 20

        self.plot_ = plot.Plot_pareto()

        self.lower = np.zeros([deed.NO_OF_HOURS, deed.NO_OF_GENERATORS])
        self.upper = np.zeros([deed.NO_OF_HOURS, deed.NO_OF_GENERATORS])
        for h_i in range(deed.NO_OF_HOURS):
            for g_i in range(deed.NO_OF_GENERATORS):
                self.upper[h_i, g_i] = deed.GENERATORS_MAX_POWER[g_i]
                self.lower[h_i, g_i] = deed.GENERATORS_MIN_POWER[g_i]
        self.lower = np.reshape(self.lower, deed.NO_OF_HOURS * deed.NO_OF_GENERATORS)
        self.upper = np.reshape(self.upper, deed.NO_OF_HOURS * deed.NO_OF_GENERATORS)

    def evaluation_fitness(self):
        self.fitness_ = P_objective.P_objective("value", "DEED", 2, self.in_)

    def initialize(self):

        
        self.hunger_list = init.init_hunger_list(self.particals)

        self.in_ = init.init_designparams(self.particals, self.min_, self.max_)
        
        self.evaluation_fitness()
        
        self.in_p,self.fitness_p = init.init_pbest(self.in_,self.fitness_)
        
        self.archive_in,self.archive_fitness = init.init_archive(self.in_, self.fitness_)
        
        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in, self.archive_fitness, self.mesh_div, self.particals)
    def update_(self):

        
        self.fitness_w = np.max(self.fitness_[:, 0]), np.max(self.fitness_[:, 1])

        self.hunger_list, self.total_hunger = update.update_hunger_value(self.hunger_list, self.particals,
                                                                         self.fitness_, self.min_,
                                                                         self.max_, self.fitness_g, self.fitness_w,
                                                                         self.eps, self.LH)

        self.in_p,self.fitness_p = update.update_pbest(self.in_,self.fitness_,self.in_p,self.fitness_p)

        # self.parents = self.in_

        self.in_ = update.update_animals_with_archive_MS(self.in_g, self.shrink, self.L, self.hunger_list, self.total_hunger, self.eps, self.in_, self.fitness_, self.fitness_g, self.cur_iter, self.archive_in, self.in_p)

        # environment selection
        # self.in_ = [self.parents, self.in_][np.random.rand() < 0.5]

        self.evaluation_fitness()

        self.archive_in, self.archive_fitness = update.update_archive_1(self.in_, self.fitness_, self.archive_in,
                                                                        self.archive_fitness,
                                                                        self.thresh, self.mesh_div)

        # print('archive_size:', self.archive_in.shape[0])
        if self.archive_in.shape[0] == self.thresh:

            archive_s = update.operatorGAhalf(self.archive_in, self.proC, self.disC, self.proM, self.disM, self.lower, self.upper)

            self.fitness_s = P_objective.P_objective("value", "DEED", 2, archive_s)
            self.archive_in, self.archive_fitness = update.update_archive_1(archive_s, self.fitness_s, self.archive_in,
                                                                            self.archive_fitness,
                                                                            self.thresh, self.mesh_div)

        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in, self.archive_fitness, self.mesh_div, self.particals)


    def done(self,cycle_):
        self.initialize()
        for i in range(cycle_):
            self.shrink = 2 * (1 - (i + 1) / cycle_)
            self.m = np.e ** ((-1) * ((i / cycle_) ** 2))
            self.S = 1 - abs((i - 1) / (i + 1)) ** self.m
            self.update_()
            self.cur_iter = i
            print('Iteration ', i, ' completed, L-MOHADE_MS best_emission, L-MOHADE_MS best_cost: ',
                  np.min(self.fitness_g[:, 1]), np.min(self.fitness_g[:, 0]))


        return self.archive_in,self.archive_fitness

