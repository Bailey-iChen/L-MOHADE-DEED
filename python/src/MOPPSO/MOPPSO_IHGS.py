#encoding: utf-8
import numpy as np
from public import init,update,plot,P_objective

import time

class MOPPSO:
    def __init__(self,particals,max_,min_,thresh,mesh_div=100):


        self.mesh_div = mesh_div
        self.particals = particals
        self.thresh = thresh
        self.max_ = max_
        self.min_ = min_
        
        

        self.max_v = 100 * np.ones(len(max_), )  
        self.min_v = -100 * np.ones(len(min_), )  

        self.plot_ = plot.Plot_pareto()
        self.delta_list = np.random.uniform(0, 2 * np.pi, particals)

    def evaluation_fitness(self):
        self.fitness_ = P_objective.P_objective("value", "DEED", 2, self.in_)

    def initialize(self):

        
        self.in_ = init.init_designparams(self.particals,self.min_,self.max_)
        
        self.v_ = init.init_v(self.particals,self.max_v,self.min_v)

        
        self.evaluation_fitness()
        
        self.in_p,self.fitness_p = init.init_pbest(self.in_,self.fitness_)
        
        self.archive_in,self.archive_fitness = init.init_archive(self.in_,self.fitness_)
        
        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in,self.archive_fitness,self.mesh_div,self.particals)
    def update_(self):

        
        self.v_, self.delta_list = update.update_ppso_v(self.particals, self.v_,self.min_v,self.max_v,self.in_,self.in_p,self.in_g, self.delta_list)
        self.in_ = update.update_in(self.in_,self.v_,self.min_,self.max_)

        self.evaluation_fitness()

        self.in_p,self.fitness_p = update.update_pbest(self.in_,self.fitness_,self.in_p,self.fitness_p)

        self.archive_in, self.archive_fitness = update.update_archive_1(self.in_, self.fitness_, self.archive_in,
                                                                      self.archive_fitness,
                                                                      self.thresh, self.mesh_div)


        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in,self.archive_fitness,self.mesh_div,self.particals)

    def done(self,cycle_):
        self.initialize()
        # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,-1)
        since = time.time()
        for i in range(cycle_):
            self.update_()

            
            print('Iteration ',i,' completed, MOPPSO best_emission, MOPPSO best_cost: ', np.min(self.fitness_g[:, 1]), np.min(self.fitness_g[:, 0]))

            # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,i)
        
        return self.archive_in,self.archive_fitness

