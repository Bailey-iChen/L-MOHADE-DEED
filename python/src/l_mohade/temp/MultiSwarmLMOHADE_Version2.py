#encoding: utf-8
import numpy as np
from public import init, plot, update, P_objective

import time



class MultiPopulationLMOHADE:
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
        self.cur_iter = 0
        self.probability = 1.0
        self.distribution_index = 20


        self.swarm1_size = particals // 3
        self.swarm2_size = particals // 3
        self.swarm3_size = particals - self.swarm1_size - self.swarm2_size

        # self.swarm1_size = 45
        # self.swarm2_size = 10
        # self.swarm3_size = particals - self.swarm1_size - self.swarm2_size

        self.plot_ = plot.Plot_pareto()

    def evaluation_fitness(self):
        self.fitness_swarm1 = P_objective.P_objective("value", "DEED", 2, self.in_swarm1)
        self.fitness_swarm2 = P_objective.P_objective("value", "DEED", 2, self.in_swarm2)
        self.fitness_swarm3 = P_objective.P_objective("value", "DEED", 2, self.in_swarm3)

    def initialize(self):

        
        self.hunger_list_swarm1 = init.init_hunger_list(self.swarm1_size)
        self.hunger_list_swarm2 = init.init_hunger_list(self.swarm2_size)
        self.hunger_list_swarm3 = init.init_hunger_list(self.swarm3_size)

        self.in_swarm1, self.in_swarm2, self.in_swarm3 = init.init_multi_swarms(self.swarm1_size,
                                                                                self.swarm2_size, self.swarm3_size)
        
        self.evaluation_fitness()
        
        self.in_swarm1_p, self.fitness_swarm1_p = init.init_pbest(self.in_swarm1,self.fitness_swarm1)
        self.in_swarm2_p, self.fitness_swarm2_p = init.init_pbest(self.in_swarm2, self.fitness_swarm2)
        self.in_swarm3_p, self.fitness_swarm3_p = init.init_pbest(self.in_swarm3, self.fitness_swarm3)

        self.in_ = np.concatenate((self.in_swarm1, self.in_swarm2, self.in_swarm3), axis=0)
        self.fitness_ = np.concatenate((self.fitness_swarm1, self.fitness_swarm2, self.fitness_swarm3), axis=0)

        
        self.archive_in,self.archive_fitness = init.init_archive(self.in_, self.fitness_)
        
        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in, self.archive_fitness, self.mesh_div, self.particals)
    def update_(self):

        
        self.fitness_w = np.max(self.fitness_)
        self.hunger_list_swarm1, self.total_hunger_swarm1 = update.update_hunger_value(self.hunger_list_swarm1,
                                                                                       self.swarm1_size,
                                                                                       self.fitness_swarm1, self.min_,
                                                                                       self.max_,
                                                                                       self.fitness_g, self.fitness_w,
                                                                                       self.eps,
                                                                                       self.LH)
        self.hunger_list_swarm2, self.total_hunger_swarm2 = update.update_hunger_value(self.hunger_list_swarm2,
                                                                                       self.swarm2_size,
                                                                                       self.fitness_swarm2, self.min_,
                                                                                       self.max_,
                                                                                       self.fitness_g, self.fitness_w,
                                                                                       self.eps,
                                                                                       self.LH)
        self.hunger_list_swarm3, self.total_hunger_swarm3 = update.update_hunger_value(self.hunger_list_swarm3,
                                                                                       self.swarm3_size,
                                                                                       self.fitness_swarm3, self.min_,
                                                                                       self.max_,
                                                                                       self.fitness_g, self.fitness_w,
                                                                                       self.eps,
                                                                                       self.LH)

        self.in_swarm1_p, self.fitness_swarm1_p = update.update_pbest(self.in_swarm1, self.fitness_swarm1,
                                                                      self.in_swarm1_p, self.fitness_swarm1_p)
        self.in_swarm2_p, self.fitness_swarm2_p = update.update_pbest(self.in_swarm2, self.fitness_swarm2,
                                                                      self.in_swarm2_p, self.fitness_swarm2_p)
        self.in_swarm3_p, self.fitness_swarm3_p = update.update_pbest(self.in_swarm3, self.fitness_swarm3,
                                                                      self.in_swarm3_p, self.fitness_swarm3_p)

        self.parents_swarm1 = self.in_swarm1
        self.parents_swarm2 = self.in_swarm2
        self.parents_swarm3 = self.in_swarm3

        # archive learning for exploration
        self.in_swarm1 = update.update_animals_with_multipopulation_archive(self.in_g, self.shrink, self.L,
                                                                            self.hunger_list_swarm1,
                                                                            self.total_hunger_swarm1, self.eps,
                                                                            self.in_swarm1, self.cur_iter,
                                                                            self.archive_in, self.in_swarm1_p)

        # PolynomialMutation for balancing exploration and exploitation
        self.in_swarm2 = update.update_animals_with_multipopulation_archive(self.in_g, self.shrink, self.L,
                                                                            self.hunger_list_swarm2,
                                                                            self.total_hunger_swarm2, self.eps,
                                                                            self.in_swarm2, self.cur_iter,
                                                                            self.archive_in, self.in_swarm2_p)

        # HGS operator for exploitation
        self.in_swarm3 = update.update_animals_with_multipopulation_archive(self.in_g, self.shrink, self.L,
                                                                            self.hunger_list_swarm3,
                                                                            self.total_hunger_swarm3, self.eps,
                                                                            self.in_swarm3, self.cur_iter,
                                                                            self.archive_in, self.in_swarm3_p)

        # environment selection
        self.in_swarm1 = [self.parents_swarm1, self.in_swarm1][np.random.rand() < 0.5]
        self.in_swarm2 = [self.parents_swarm2, self.in_swarm2][np.random.rand() < 0.5]
        self.in_swarm3 = [self.parents_swarm3, self.in_swarm3][np.random.rand() < 0.5]

        self.evaluation_fitness()

        self.in_ = np.concatenate((self.in_swarm1, self.in_swarm2, self.in_swarm3), axis=0)
        self.fitness_ = np.concatenate((self.fitness_swarm1, self.fitness_swarm2, self.fitness_swarm3), axis=0)

        self.archive_in, self.archive_fitness = update.update_archive_1(self.in_, self.fitness_, self.archive_in,
                                                                        self.archive_fitness,
                                                                        self.thresh, self.mesh_div)


        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in, self.archive_fitness, self.mesh_div, self.particals)


    def done(self,cycle_):
        self.initialize()
        for i in range(cycle_):
            self.shrink = 2 * (1 - (i + 1) / cycle_)
            self.update_()
            self.cur_iter = i
            print('Iteration ', i, ' completed, mpms_hgs_version2 best_emission, L-MOHADE best_cost: ',
                  np.min(self.fitness_g[:, 1]), np.min(self.fitness_g[:, 0]))


        return self.archive_in,self.archive_fitness

