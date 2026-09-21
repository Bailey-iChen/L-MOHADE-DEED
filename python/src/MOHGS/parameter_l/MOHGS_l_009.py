#encoding: utf-8
import numpy as np
from public import init, plot, update, P_objective

import time

class MoHGS_l_009:
    def __init__(self,particals,max_,min_,thresh,mesh_div=10, LH=10000, L=0.09):


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

        self.plot_ = plot.Plot_pareto()

    def evaluation_fitness(self):
        self.fitness_ = P_objective.P_objective("value", "DEED", 2, self.in_)

    def initialize(self):

        
        self.hunger_list = init.init_hunger_list(self.particals)

        self.in_ = init.init_designparams(self.particals, self.min_, self.max_)
        
        self.evaluation_fitness()
        
        self.archive_in,self.archive_fitness = init.init_archive(self.in_, self.fitness_)
        
        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in, self.archive_fitness, self.mesh_div, self.particals)
    def update_(self):

        
        self.fitness_w = np.max(self.fitness_[:, 0]), np.max(self.fitness_[:, 1])

        self.hunger_list, self.total_hunger = update.update_hunger_value(self.hunger_list, self.particals,
                                                                         self.fitness_, self.min_,
                                                                         self.max_, self.fitness_g, self.fitness_w,
                                                                         self.eps, self.LH)

        self.in_ = update.update_animals_0001(self.particals, self.fitness_, self.in_g, self.fitness_g, self.shrink, self.L,
                                         self.hunger_list, self.total_hunger, self.eps, self.in_, self.max_, self.min_)

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
            self.update_()

            
            print('Iteration ',i,' completed, MOHGS_l=009 best_emission, MOHGS best_cost: ', np.min(self.fitness_g[:, 1]), np.min(self.fitness_g[:, 0]))

            # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,i)
        return self.archive_in,self.archive_fitness

