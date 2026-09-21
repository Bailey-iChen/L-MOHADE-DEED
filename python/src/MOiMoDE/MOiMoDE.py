#encoding: utf-8
import numpy as np
from public import init,update,plot,P_objective
from public import constants_40unit as deed

import time

class MOiMoDE:
    def __init__(self,particals,max_,min_,thresh,mesh_div=10):


        self.mesh_div = mesh_div
        self.particals = particals
        self.thresh = thresh
        self.max_ = max_
        self.min_ = min_
        self.CR = 0.5
        self.STEP_LENGTH = 0.5
        self.m = 0
        self.S = 0
        self.cur_iter = 0
        
        

        self.max_v = 100 * np.ones(deed.NO_OF_GENERATORS * deed.NO_OF_HOURS, )  
        self.min_v = -100 * np.ones(deed.NO_OF_GENERATORS * deed.NO_OF_HOURS, )  

        self.plot_ = plot.Plot_pareto()

    def evaluation_fitness(self):
        self.fitness_ = P_objective.P_objective("value", "DEED", 2, self.in_)

    def initialize(self):

        
        self.in_ = init.init_designparams(self.particals,self.min_,self.max_)
        
        self.evaluation_fitness()
        
        self.in_p,self.fitness_p = init.init_pbest(self.in_,self.fitness_)
        
        self.archive_in,self.archive_fitness = init.init_archive(self.in_,self.fitness_)
        
        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in,self.archive_fitness,self.mesh_div,self.particals)
    def update_(self):

        
        self.in_ = update.update_iMoDE(self.in_, self.CR, self.STEP_LENGTH, self.in_g, self.in_p, self.S, self.cur_iter)

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
            self.m = np.e ** ((-1) * ((i / cycle_) ** 2))
            self.S = 1 - abs((i - 1) / (i + 1)) ** self.m
            self.cur_iter = i
            self.update_()

            print('Iteration ',i,' completed, MO_iMoDE best_emission, MO_iMoDE best_cost: ', np.min(self.fitness_g[:, 1]), np.min(self.fitness_g[:, 0]))

            # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,i)
        return self.archive_in,self.archive_fitness

