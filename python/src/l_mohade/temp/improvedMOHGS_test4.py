#encoding: utf-8
import numpy as np
from public import init, plot, update, P_objective

import time


# Unsupervised feature selection using an improved version of Differential Evolution
class MOIHGS:
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

        self.plot_ = plot.Plot_pareto()

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

        
        self.fitness_w = np.max(self.fitness_)

        self.hunger_list, self.total_hunger = update.update_hunger_value(self.hunger_list, self.particals,
                                                                         self.fitness_, self.min_,
                                                                         self.max_, self.fitness_g, self.fitness_w,
                                                                         self.eps, self.LH)

        self.in_p,self.fitness_p = update.update_pbest(self.in_,self.fitness_,self.in_p,self.fitness_p)

        self.in_, self.cr = update.update_animals_improvedHGS_test4(self.in_g, self.shrink, self.L, self.hunger_list, self.total_hunger, self.eps, self.in_, self.T2, self.cr, self.cur_iter, self.in_p)
        self.evaluation_fitness()

        self.archive_in, self.archive_fitness = update.update_archive_1(self.in_, self.fitness_, self.archive_in,
                                                                        self.archive_fitness,
                                                                        self.thresh, self.mesh_div)


        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in, self.archive_fitness, self.mesh_div, self.particals)


    def done(self,cycle_):
        self.initialize()
        # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,-1)
        since = time.time()
        for i in range(cycle_):
            self.shrink = 2 * (1 - (i + 1) / cycle_)
            self.m = np.e ** ((-1) * ((i / cycle_) ** 2))
            self.S = 1 - abs((i - 1) / (i + 1)) ** self.m
            self.update_()
            self.cur_iter = i

            
            print('Iteration ',i,' completed111, improvedHGS4 best_emission, improvedHGS4 best_cost: ', np.min(self.fitness_g[:, 1]), np.min(self.fitness_g[:, 0]))

            # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,i)
        return self.archive_in,self.archive_fitness

