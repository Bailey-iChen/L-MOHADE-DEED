#encoding: utf-8
import random
import numpy as np
import pareto,NDsort
import update
import constants_15unit as deed


def init_designparams(particals,in_min,in_max):
    in_dim = 24 * deed.NO_OF_GENERATORS    
    in_temp = np.random.uniform(100, 600, (particals, in_dim))
    # in_temp = np.zeros((particals, in_dim))
    # for i in range(particals):
    #     X_i_reshape = np.reshape(in_temp[i, :], (24, deed.NO_OF_GENERATORS))
    #     for h_i in range(24):
    #         for g_i in range(deed.NO_OF_GENERATORS):
    #             X_i_reshape[h_i, g_i] = in_min[g_i] + (in_max[g_i] - in_min[g_i]) * np.random.rand()
    #     X_i_reshape = np.reshape(X_i_reshape, 24 * deed.NO_OF_GENERATORS)
    #     in_temp[i, :] = X_i_reshape.copy()
    # in_temp = chaotic_init(in_temp, particals, in_dim, ub, lb)
    for i in range(particals):
        in_temp[i] = update.ensure_min_max_constraints(in_temp[i])
        in_temp[i] = update.adjust_slack_power(in_temp[i])

    return in_temp

def init_v(particals,v_max,v_min):
    v_dim = len(v_max)     
    # v_ = np.random.uniform(0,1,(particals,v_dim))*(v_max-v_min)+v_min

    v_ = np.zeros((particals,v_dim))
    return v_

def init_pbest(in_,fitness_):
    return in_,fitness_


def init_archive(in_,fitness_):

    FrontValue_1_index = NDsort.NDSort(fitness_, in_.shape[0])[0]==1
    FrontValue_1_index = np.reshape(FrontValue_1_index,(-1,))

    # print('FrontValue_1_index:', FrontValue_1_index)

    curr_archiving_in=in_[FrontValue_1_index]

    curr_archiving_fit=fitness_[FrontValue_1_index]

    # pareto_c = pareto.Pareto_(in_,fitness_)
    # curr_archiving_in_,curr_archiving_fit_ = pareto_c.pareto()
    return curr_archiving_in,curr_archiving_fit

def init_hunger_list(particles):
    hunger_list = np.ones([particles, 1])
    return hunger_list
