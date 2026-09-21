#encoding: utf-8
import numpy as np
import random
from  public import NDsort
from public import constants_15unit as deed
from public import constants_5unit as deed_5
from random import shuffle
from math import gamma
import scipy.stats
from public import sortrows

def update_hunger_value(hunger_list, Popsize, fit, min, max, g_best, g_worst, eps, LH):
    for i in range(Popsize):
        r = np.random.rand()
        space = np.mean(max - min)
        H = (np.min(fit[i]) - np.min(g_best[i])) / (np.min(g_worst) - np.min(g_best[i]) + eps) * r * 2 * space
        if H < LH:
            H = LH * (1 + r)
            hunger_list[i] += H

    Sum_hunger = np.sum(hunger_list)
    return hunger_list, Sum_hunger

def update_ppso_v(particles, v_,v_min,v_max,in_,in_pbest,in_gbest, delta_list):

    for i in range(particles):
        aa = 2 * (np.sin(delta_list[i]))
        bb = 2 * (np.cos(delta_list[i]))
        ee = abs(np.cos(delta_list[i])) ** aa
        tt = abs(np.sin(delta_list[i])) ** bb

    w = 0.4
    N,D = v_.shape
    r1 = np.tile(np.random.rand(N,1),(1,D))
    r2 = np.tile(np.random.rand(N,1),(1,D))

    v_temp = ee * (in_pbest-in_) + tt * (in_gbest-in_)

    for i in range(particles):
        delta_list[i] += abs(aa + bb) * (2 * np.pi)

    
    Upper = np.tile(v_max,(N,1))
    Lower = np.tile(v_min,(N,1))
    
    return v_temp, delta_list


def update_v(v_,v_min,v_max,in_,in_pbest,in_gbest):
    

    w = 0.4
    N,D = v_.shape
    r1 = np.tile(np.random.rand(N,1),(1,D))
    r2 = np.tile(np.random.rand(N,1),(1,D))

    v_temp = w*v_ + r1*(in_pbest-in_) + r2*(in_gbest-in_)

    
    Upper = np.tile(v_max,(N,1))
    Lower = np.tile(v_min,(N,1))
    v_temp = np.maximum(np.minimum(Upper,v_temp), Lower) 
    return v_temp

def pick_3_random_agents(agents, agent_index, NO_OF_AGENTS):
    agents_indexes = range(0, NO_OF_AGENTS)
    all_other_agents_indexes = list(filter(lambda i: i != agent_index, agents_indexes))
    three_agents_indexes = random.sample(all_other_agents_indexes, 3)
    return agents[three_agents_indexes]

def update_DEpos(in_,in_min,in_max, CR, STEP_LENGTH):
    N, D = in_.shape

    for i in range(N):
        ids_except_current = [_ for _ in range(N) if _ != i]
        r1_, r2_, r3_ = random.sample(ids_except_current, 3)
        for j in range(D):
            if random.random() < CR:
                in_[i, j] = in_[r1_, j] + STEP_LENGTH * (in_[r2_, j] - in_[r3_, j])

        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])
    
    # Upper = np.tile(in_max, (N, 1))
    # Lower = np.tile(in_min, (N, 1))
    # in_temp = np.maximum(np.minimum(Upper,in_), Lower)
    return in_

def update_HjDE(in_, f, cr, T1, T2, Fl, Fu, in_min, in_max, gbest, shrink, L, hunger, total_hunger, eps):
    N, D = in_.shape

    R = 2 * shrink * np.random.rand() - shrink
    for i in range(N):
        if np.random.uniform(0, 1) < T1:
            f[i] = Fl + np.random.uniform(0, 1) * Fu
        if np.random.uniform(0, 1) < T2:
            cr[i] = np.random.uniform(0, 1)

    for i in range(N):

        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(N) if _ != i]
        r1_, r2_, r3_ = random.sample(ids_except_current, 3)
        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        for j in range(D):
            if np.random.rand() < 1:
                d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
            else:
                d_val = in_[r1_, j] + f[i] * (in_[r2_, j] - in_[r3_, j])
            if random.random() > cr[i] or j == j_rand:
                d_val = in_[i, j]
            mutant_sol[j] = d_val

        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_, f, cr


def update_iMoDE(in_, CR, STEP_LENGTH,gbest, pbest, S, cur_iter):

    if cur_iter == 0:
        alpha = 1
    else:
        alpha = 1 / (1 + (10 ** (- 10 / cur_iter)))

    particles, dim = in_.shape
    for i in range(particles):
        ids_except_current = [_ for _ in range(particles) if _ != i]
        r1_, r2_, r3_ = random.sample(ids_except_current, 3)
        for j in range(dim):
            if random.random() < CR:
                if np.random.rand() < alpha:
                    in_[i, j] = in_[r1_, j] + STEP_LENGTH * (in_[r2_, j] - in_[r3_, j])
                else:
                    in_[i, j] = gbest[i, j] + alpha * abs(pbest[i, j] - in_[r1_, j])

        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_


def update_in(in_,v_,in_min,in_max):
    N, D = in_.shape
    
    in_temp = in_ + v_
    for i in range(N):
        in_temp[i] = ensure_min_max_constraints(in_temp[i])
        in_temp[i] = adjust_slack_power(in_temp[i])
    
    # Upper = np.tile(in_max, (N, 1))
    # Lower = np.tile(in_min, (N, 1))
    # in_temp = np.maximum(np.minimum(Upper,in_temp), Lower)
    return in_temp


def update_pbest(in_,fitness_,in_pbest,out_pbest):
    temp = out_pbest - fitness_
    Dominate = np.int64(np.any(temp< 0, axis=1)) - np.int64(np.any(temp> 0, axis=1))

    remained_1 = Dominate==-1
    out_pbest[remained_1] = fitness_[remained_1]
    in_pbest[remained_1] = in_[remained_1]

    remained_2 = Dominate == 0
    remained_temp_rand = np.random.rand(len(Dominate),)<0.5
    remained_final = remained_2 & remained_temp_rand
    out_pbest[remained_final] = fitness_[remained_final]
    in_pbest[remained_final] = in_[remained_final]
    return in_pbest,out_pbest



def update_archive_1(in_,fitness_,archive_in,archive_fitness,thresh,mesh_div):
    
    total_Pop = np.vstack((archive_in,in_))
    total_Func = np.vstack((archive_fitness,fitness_))

    FrontValue_1_index = NDsort.NDSort(total_Func, total_Pop.shape[0])[0]==1
    FrontValue_1_index = np.reshape(FrontValue_1_index,(-1,))
    archive_in =total_Pop[FrontValue_1_index]
    archive_fitness = total_Func[FrontValue_1_index]

    if archive_in.shape[0] > thresh:

        Del_index = Delete(archive_fitness,archive_in.shape[0]-thresh,mesh_div)
        archive_in  = np.delete(archive_in,Del_index,0)
        archive_fitness = np.delete(archive_fitness,Del_index,0)
    return archive_in,archive_fitness

def Delete(archiving_fit,K,mesh_div):
    Nop, num_obj = archiving_fit.shape

    # %% Calculate the grid location of each solution
    fmax = np.max(archiving_fit, axis=0)
    fmin = np.min(archiving_fit, axis=0)
    d = (fmax - fmin) / mesh_div
    fmin = np.tile(fmin, (Nop, 1))
    d = np.tile(d, (Nop, 1))
    Gloc = np.floor((archiving_fit - fmin) / d)
    Gloc[Gloc >= mesh_div] = mesh_div - 1
    Gloc[np.isnan(Gloc)] = 0

    # Detect the grid of each solution belongs to
    _, _, Site = np.unique(Gloc, return_index=True, return_inverse=True, axis=0)


    # Calculate the crowd degree of each grid
    CrowdG = np.histogram(Site, np.max(Site)+1)[0]
    CrowdG_ =CrowdG.copy()

    Del_index = np.zeros(Nop,)==1

    while np.sum(Del_index)<K:
        maxGrid = np.where(CrowdG == max(CrowdG))[0]
        Temp = np.random.randint(0,len(maxGrid))
        Grid = maxGrid[Temp]

        InGrid = np.where(Site==Grid)[0]


        Temp = np.random.randint(0,len(InGrid))
        p = InGrid[Temp]
        Del_index[p] = True
        Site[p] = -100
        CrowdG[Grid] = CrowdG[Grid] -1

    return np.where(Del_index==1)[0]





def update_gworst_1(in_, fit):
    sorted_pop = np.argsort(fit)
    return in_[sorted_pop[-1]]

def update_gbest_1(archiving_in,archiving_fit,mesh_div,particals):
    Nop,num_obj =  archiving_fit.shape

    # %% Calculate the grid location of each solution
    fmax = np.max(archiving_fit,axis=0)
    fmin = np.min(archiving_fit,axis=0)
    d = (fmax-fmin)/mesh_div
    fmin = np.tile(fmin,(Nop,1))
    d = np.tile(d,(Nop,1))
    Gloc = np.floor((archiving_fit-fmin)/d)
    Gloc[Gloc >= mesh_div] = mesh_div-1
    Gloc[np.isnan(Gloc)] = 0

    #Detect the grid of each solution belongs to
    _,_,Site = np.unique(Gloc, return_index=True,return_inverse=True,axis=0)

    #Calculate the crowd degree of each grid
    CrowdG =  np.histogram(Site,np.max(Site)+1)[0]

    #  Roulette-wheel 1/Fitnessselection
    TheGrid = RouletteWheelSelection(particals,CrowdG)

    ReP = np.zeros(particals,)
    for i in range(particals):
        InGrid = np.where(Site==TheGrid[i])[0]
        Temp = np.random.randint(0,len(InGrid))
        ReP[i] = InGrid[Temp]
    ReP = np.int64(ReP)
    return archiving_in[ReP],archiving_fit[ReP]

def update_gbest_1_and_cr(archiving_in,archiving_fit,mesh_div,particals, cr):
    Nop,num_obj =  archiving_fit.shape

    # %% Calculate the grid location of each solution
    fmax = np.max(archiving_fit,axis=0)
    fmin = np.min(archiving_fit,axis=0)
    d = (fmax-fmin)/mesh_div
    fmin = np.tile(fmin,(Nop,1))
    d = np.tile(d,(Nop,1))
    Gloc = np.floor((archiving_fit-fmin)/d)
    Gloc[Gloc>=mesh_div] = mesh_div-1
    Gloc[np.isnan(Gloc)] = 0

    #Detect the grid of each solution belongs to
    _,_,Site = np.unique(Gloc, return_index=True,return_inverse=True,axis=0)

    #Calculate the crowd degree of each grid
    CrowdG =  np.histogram(Site,np.max(Site)+1)[0]

    #  Roulette-wheel 1/Fitnessselection
    TheGrid = RouletteWheelSelection(particals,CrowdG)

    ReP = np.zeros(particals,)
    for i in range(particals):
        InGrid = np.where(Site==TheGrid[i])[0]
        Temp = np.random.randint(0,len(InGrid))
        ReP[i] = InGrid[Temp]
    ReP = np.int64(ReP)
    return archiving_in[ReP],archiving_fit[ReP], cr[ReP]


def RouletteWheelSelection(N,Fitness):

    Fitness = np.reshape(Fitness,(-1,))
    Fitness  = Fitness + np.minimum(np.min(Fitness),0)
    Fitness = np.cumsum(1/Fitness)
    Fitness = Fitness/np.max(Fitness)
    index = np.sum(np.int64(~(np.random.rand(N,1)<Fitness)), axis=1)

    return index


def sech(x):
    return 2 / (np.exp(x) + np.exp(-x))



NO_OF_HOURS = 24

NO_OF_GENERATORS = deed.NO_OF_GENERATORS
NO_OF_VARIABLES = NO_OF_HOURS * NO_OF_GENERATORS

SLACK_GENERATOR_INDEX = deed.SLACK_GENERATOR_INDEX


def compute_slack_power(generators_power, hour):
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))

    a = deed.B_MATRIX[SLACK_GENERATOR_INDEX][SLACK_GENERATOR_INDEX]

    b = 0
    for i in range(NO_OF_GENERATORS - 1):
        b += (deed.B_MATRIX[SLACK_GENERATOR_INDEX][i] * generators_power_reshaped[hour][i])
    b = 2 * b - 1

    c = deed.POWER_DEMAND[hour]
    for i in range(NO_OF_GENERATORS - 1):
        for j in range(NO_OF_GENERATORS - 1):
            power_i = generators_power_reshaped[hour][i]
            power_j = generators_power_reshaped[hour][j]
            c += power_i * power_j * deed.B_MATRIX[i][j]
    for i in range(NO_OF_GENERATORS - 1):
        c -= generators_power_reshaped[hour][i]

    roots = np.roots([a, b, c])
    return np.min(roots)

def ensure_min_max_constraints(generators_power):
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))

    # print('power:', generators_power_reshaped)

    for h_i in range(NO_OF_HOURS):
        for g_i in range(NO_OF_GENERATORS):
            generator_power = generators_power_reshaped[h_i][g_i]
            if (generator_power > deed.GENERATORS_MAX_POWER[g_i]):
                generators_power_reshaped[h_i][g_i] = deed.GENERATORS_MAX_POWER[g_i]
            elif (generator_power < deed.GENERATORS_MIN_POWER[g_i]):
                generators_power_reshaped[h_i][g_i] = deed.GENERATORS_MIN_POWER[g_i]

    return np.reshape(generators_power_reshaped, NO_OF_VARIABLES)


def adjust_slack_power(generators_power):
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))


    for h_i in range(NO_OF_HOURS):
        slack_power = compute_slack_power(generators_power, h_i)
        if (slack_power < 0):
            slack_power = deed.GENERATORS_MIN_POWER[SLACK_GENERATOR_INDEX]
        generators_power_reshaped[h_i][SLACK_GENERATOR_INDEX] = slack_power

    return np.reshape(generators_power_reshaped, NO_OF_VARIABLES)


def check_bound(NO_OF_AGENTS, Ns):
    lb = 1
    ub = NO_OF_AGENTS
    if Ns <= lb:
        Ns = 1
    if Ns > ub:
        Ns = NO_OF_AGENTS
    return Ns

# countGau = 0
# countCau = 0
# countLevy = 0
def check_strategy(NO_OF_AGENTS, gauFit, cauFit, levyFit, Ns1, Ns2, Ns3, hunger_list_Gau, hunger_list_Cau, hunger_list_Levy, sum_hunger_list, countGau, countCau, countLevy):
    # global countGau
    # global countCau
    # global countLevy

    hungerGau = sum(hunger_list_Gau[:]) / (sum_hunger_list)
    hungerCau = sum(hunger_list_Cau[:]) / (sum_hunger_list)
    hungerLevy = sum(hunger_list_Levy[:]) / (sum_hunger_list)
    thetaGau = 0.5 * (1 / hungerGau) + 0.5 * (np.mean(gauFit) / (np.mean(gauFit) + np.mean(cauFit) + np.mean(levyFit)))
    thetaCau = 0.5 * (1 / hungerCau) + 0.5 * (np.mean(cauFit) / (np.mean(gauFit) + np.mean(cauFit) + np.mean(levyFit)))
    thetaLevy = 0.5 * (1 / hungerLevy) + 0.5 * (
                np.mean(levyFit) / (np.mean(gauFit) + np.mean(cauFit) + np.mean(levyFit)))
    # thetaGau = np.mean(gauFit) / (np.mean(gauFit) + np.mean(deFit) + np.mean(levyFit))
    # thetaCau = np.mean(deFit) / (np.mean(gauFit) + np.mean(deFit) + np.mean(levyFit))
    # thetaLevy = np.mean(levyFit) / (np.mean(gauFit) + np.mean(deFit) + np.mean(levyFit))
    if Ns1 != 1:
        if thetaGau == max(thetaGau, thetaCau, thetaLevy):
            if Ns1 != 1:
                countGau += 1
        if thetaCau == max(thetaGau, thetaCau, thetaLevy) and Ns2 != 1:
            if Ns2 != 1:
                countCau += 1
        if thetaLevy == max(thetaGau, thetaCau, thetaLevy) and Ns3 != 1:
            if Ns3 != 1:
                countLevy += 1
    elif Ns1 == 1:
        if thetaCau == max(thetaCau, thetaLevy) and Ns2 != 1:
            if Ns2 != 1:
                countCau += 1
        if thetaLevy == max(thetaCau, thetaLevy) and Ns3 != 1:
            if Ns3 != 1:
                countLevy += 1


    # print('countGau:', countGau)
    # print('countCau:', countCau)
    # print('countLevy:', countLevy)
    if Ns1 != 1:
        if countCau == 1:
            Ns2 -= 1
            countCau = 0
            if np.random.rand() < 0.5:
                Ns1 += 1
            else:
                Ns3 += 1
        if countGau == 1:
            Ns1 -= 1
            countGau = 0
            if np.random.rand() < 0.5:
                Ns2 += 1
            else:
                Ns3 += 1
        if countLevy == 1:
            Ns3 -= 1
            countLevy = 0
            if np.random.rand() < 0.5:
                Ns1 += 1
            else:
                Ns2 += 1
    elif Ns1 == 1:
        if countCau == 1:
            Ns2 -= 1
            countCau = 0
            Ns3 += 1
        if countLevy == 1:
            Ns3 -= 1
            countLevy = 0
            Ns2 += 1

    Ns1 = check_bound(NO_OF_AGENTS, Ns1)
    Ns2 = check_bound(NO_OF_AGENTS, Ns2)
    Ns3 = check_bound(NO_OF_AGENTS, Ns3)

    N = Ns1 + Ns2 +Ns3
    while N > NO_OF_AGENTS:
        N = Ns1 + Ns2 + Ns3
        if Ns1 == max(Ns1, Ns2, Ns3):
            if N > NO_OF_AGENTS:
                Ns1 -= 1
        if Ns2 == max(Ns1, Ns2, Ns3):
            if N > NO_OF_AGENTS:
                Ns2 -= 1
        if Ns3 == max(Ns1, Ns2, Ns3):
            if N > NO_OF_AGENTS:
                Ns3 -= 1


    return Ns1, Ns2, Ns3, countGau, countCau, countLevy


def update_animals(particles, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, vmax, vmin):
    # for i in range(particles):
    R = 2 * shrink * np.random.rand() - shrink

    for i in range(particles):
        E = sech(np.min(fit[i]) - np.min(fitness_g[i]))
        if np.random.rand() < L:
            W1 = hunger[i, 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        r1 = np.random.rand()
        r2 = np.random.rand()
        if r1 < L:
            in_[i] = in_[i] * (1 + np.random.normal(0, 1))
        else:
            if r2 > E:
                in_[i] = W1 * gbest[i] + R * W2 * abs(gbest[i] - in_[i])
            else:
                in_[i] = W1 * gbest[i] - R * W2 * abs(gbest[i] - in_[i])

        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])
        
    return in_



def update_animals_Co(particles, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, vmax, vmin):
    # for i in range(particles):
    R = 2 * shrink * np.random.rand() - shrink

    xmean = np.mean(in_, axis=1)

    aux = np.ones((particles, 1), dtype=np.bool)
    xsel = in_.T
    c = 1 / (particles - 1) * np.dot(in_.T - xmean, (in_.T - xmean).T)
    c = np.triu(c) + np.triu(c, 1).T
    r, d = np.linalg.eig(c)
    if np.max(np.diag(d)) > 1e20 * np.min(np.diag(d)):
        tmp = np.max(np.diag(d)) / 1e20 - np.min(np.diag(d))
        c = c + tmp * np.eye(in_.shape[1])
        r, d = np.linalg.eig(c)

    tm = d
    tm_ = d.T
    in_ = np.dot(in_, tm_.T)

    for i in range(particles):
        E = sech(np.min(fit[i]) - np.min(fitness_g[i]))
        if np.random.rand() < L:
            W1 = hunger[i, 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        r1 = np.random.rand()
        r2 = np.random.rand()
        if r1 < L:
            in_[i] = in_[i] * (1 + np.random.normal(0, 1))
        else:
            if r2 > E:
                in_[i] = W1 * gbest[i] + R * W2 * abs(gbest[i] - in_[i])
            else:
                in_[i] = W1 * gbest[i] - R * W2 * abs(gbest[i] - in_[i])

        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_


# def update_animals_improvedHGS(particles, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, pbest,S, cur_iter):
#     # for i in range(particles):
#     R = 2 * shrink * np.random.rand() - shrink
#
#     if cur_iter == 0:
#         alpha = 1
#     else:
#         alpha = 1 / (1 + (10 ** (- 10 / cur_iter)))
#
#     for i in range(particles):
#         ids_except_current = [_ for _ in range(particles) if _ != i]
#         r1_, r2_, r3_ = random.sample(ids_except_current, 3)
#
#         E = sech(np.min(fit[i]) - np.min(fitness_g[i]))
#         if np.random.rand() < L:
#             W1 = hunger[i, 0] * particles / (total_hunger + eps) * np.random.rand()
#         else:
#             W1 = 1
#         W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2
#
#         r1 = np.random.rand()
#         r2 = np.random.rand()
#         if r1 < L:
#             in_[i] = in_[i] * (1 + np.random.normal(0, 1))
#         else:
#             if r2 > E:
#                 if np.random.rand() < alpha:
#                     in_[i] = W1 * gbest[i] + R * W2 * abs(gbest[i] - in_[i])
#                 else:
#                     in_[i] = gbest[i] + alpha * abs(pbest[i] - in_[r1_])
#                     # in_[i] = W1 * gbest[i] + R * W2 * abs(pbest[i] - in_[r1_])
#             else:
#                 in_[i] = (1 - S) * gbest[i] + S * (3.98 * np.random.rand() * (1 - np.random.rand()))
#
#         in_[i] = ensure_min_max_constraints(in_[i])
#         in_[i] = adjust_slack_power(in_[i])
#
#     return in_

def archive_learning(in_, shrink, cur_iter, L, hunger, total_hunger, eps, archive_in, pbest):
    N, D = in_.shape
    R = 2 * shrink * np.random.rand() - shrink
    cr_ = 1 - (0.55 + 1 / np.pi * np.arctan((1 - cur_iter / 1000 - 0.8) / 0.3))
    for i in range(N):
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        indexes_, _ = archive_in.shape
        randNum_ = np.random.randint(0, indexes_)
        for j in range(D):
            if random.random() > cr_ or j == j_rand:  # uncooperative animals
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                d_val = W1 * archive_in[randNum_, j] + R * W2 * abs(pbest[i, j] - in_[i, j])
            mutant_sol[j] = d_val

        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])
    return in_

def PolynomialMutation(parents, eta_c, eta_m, pm):

    # crossover
    p = 0
    children = np.empty((0, parents.shape[1]))
    while (p < parents.shape[0]):
        children =np.append(children, cxSimulatedBinary(parents[p], parents[p + 1], eta_c), axis=0)
        p += 2

    N, D = children.shape
    for i in range(N):
        mutant_sol = np.zeros(D)
        for j in range(D):
            rand = np.random.rand()
            if rand <= pm:
                y = children[i, j]
                yl, yu = np.min(children[:, j]), np.max(children[:, j])
                if yl == yu:
                    yl = yu
                else:
                    delta1 = (y - yl) / (yu - yl)
                    delta2 = (yu - y) / (yu - yl)
                    rnd = np.random.rand()
                    mut_pow = 1.0 / (eta_c + 1.0)
                    if rnd <= 0.5:
                        xy = 1.0 - delta1
                        val = 2.0 * rnd + (1.0 - 2.0 * rnd) * (pow(xy, eta_c + 1.0))
                        deltaq = pow(val, mut_pow) - 1.0
                    else:
                        xy = 1.0 - delta2
                        val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) * (pow(xy, eta_c + 1.0))
                        deltaq = 1.0 - pow(val, mut_pow)


                    y += deltaq * (yu - yl)
                mutant_sol[j] = y
        children[i] = mutant_sol
        children[i] = ensure_min_max_constraints(children[i])
        children[i] = adjust_slack_power(children[i])

    return children

def mutPolynomialBounded(individual, eta, low, up, indpb):

    size = len(individual)
    for i, xl, xu in zip(range(size), low, up):
        if random.random() <= indpb:
            x = individual[i]
            delta_1 = (x - xl) / (xu - xl)
            delta_2 = (xu - x) / (xu - xl)
            rand = random.random()
            mut_pow = 1.0 / (eta + 1.)

            if rand < 0.5:
                xy = 1.0 - delta_1
                val = 2.0 * rand + (1.0 - 2.0 * rand) * xy ** (eta + 1)
                delta_q = val ** mut_pow - 1.0
            else:
                xy = 1.0 - delta_2
                val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * xy ** (eta + 1)
                delta_q = 1.0 - val ** mut_pow

            x = x + delta_q * (xu - xl)
            x = min(max(x, xl), xu)
            individual[i] = x
    return individual

def cxSimulatedBinary(ind1, ind2, eta):

    for i, (x1, x2) in enumerate(zip(ind1, ind2)):
        rand = random.random()
        if rand <= 0.5:
            beta = 2. * rand
        else:
            beta = 1. / (2. * (1. - rand))
        beta **= 1. / (eta + 1.)
        ind1[i] = 0.5 * (((1 + beta) * x1) + ((1 - beta) * x2))
        ind2[i] = 0.5 * (((1 - beta) * x1) + ((1 + beta) * x2))

    return ind1, ind2

def modifiedHGSoperator(in_, shrink, cur_iter, L, hunger, total_hunger, eps, gbest):
    N, D = in_.shape
    R = 2 * shrink * np.random.rand() - shrink
    cr_ = 1 - (0.55 + 1 / np.pi * np.arctan((1 - cur_iter / 1000 - 0.8) / 0.3))
    for i in range(N):
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        for j in range(D):
            if random.random() > cr_ or j == j_rand:  # uncooperative animals
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
            mutant_sol[j] = d_val
        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])
    return in_

def update_animals_with_multipopulation_archive(gbest, shrink, L, hunger, total_hunger, eps, in_, cur_iter, archive_in, pbest):
    N, D = in_.shape
    R = 2 * shrink * np.random.rand() - shrink
    cr_ = 1 - (0.55 + 1 / np.pi * np.arctan((1 - cur_iter / 1000 - 0.8) / 0.3))
    for i in range(N):
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        indexes_, _ = archive_in.shape
        randNum_ = np.random.randint(0, indexes_)
        for j in range(D):
            if random.random() > cr_ or j == j_rand:  # uncooperative animals
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                if cur_iter < 400:  # exploration
                    d_val = W1 * archive_in[randNum_, j] + R * W2 * abs(pbest[i, j] - in_[i, j])
                else:  # exploitation
                    d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])

            mutant_sol[j] = d_val


        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_

# test-2022/7/18/
def update_animals_with_archive(gbest, shrink, L, hunger, total_hunger, eps, in_, T2, cr, fit, fit_g, cur_iter, archive_in, pbest):
    N, D = in_.shape
    R = 2 * shrink * np.random.rand() - shrink
    cr_ = 1 - (0.55 + 1 / np.pi * np.arctan((1 - cur_iter / 1000 - 0.8) / 0.3))
    for i in range(N):
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        indexes_, _ = archive_in.shape
        randNum_ = np.random.randint(0, indexes_)
        for j in range(D):
            if random.random() > cr_ or j == j_rand:  # uncooperative animals
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                if cur_iter < 400:  # exploration
                    d_val = W1 * archive_in[randNum_, j] + R * W2 * abs(pbest[i, j] - in_[i, j])
                else:  # exploitation
                    d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])

            mutant_sol[j] = d_val


        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_, cr

# test-2022/5/9/19:59
def update_animals_improvedHGS_test1(gbest, shrink, L, hunger, total_hunger, eps, in_, T2, cr, fit, fit_g, cur_iter, archive_in, pbest):
    N, D = in_.shape
    c1 = 1.845
    c2 = 1.845
    c3 = 0.205
    c4 = 0.205

    for i in range(N):
        if np.random.uniform(0, 1) < T2:
            cr[i] = np.random.uniform(0, 1)

    R = 2 * shrink * np.random.rand() - shrink
    cr_ = 1 - (0.55 + 1 / np.pi * np.arctan((1 - cur_iter / 1000 - 0.8) / 0.3))
    for i in range(N):
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        indexes_, _ = archive_in.shape
        randNum_ = np.random.randint(0, indexes_)
        for j in range(D):
            if random.random() > cr_ or j == j_rand:  
                # d_val = in_[i, j]
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                if cur_iter < 400:
                    # d_val = in_[i, j] + gbest[i, j] - in_[i, j] * np.exp(
                    #     (min(fit_g[i]) - min(fit[i])) * np.random.rand())  # ISFO - global search

                    # d_val = in_[i, j] * get_levy_flight_step(beta=1, multiplier=0.01, case=-1)  # levy flight
                    # d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
                    # t1 = np.random.rand() * c1 * pbest[i, j] - in_[i, j]
                    # t2 = np.random.rand() * c2 * gbest[i, j] - in_[i, j]
                    # d_val = abs(0.7298437881 * (t1 + t2))

                    d_val = W1 * archive_in[randNum_, j] + R * W2 * abs(pbest[i, j] - in_[i, j])
                    # if np.random.rand() < 0.2:
                    #     d_val = scipy.stats.cauchy.rvs(loc=in_[i, j], scale=0.0001)
                    # else:
                    #     d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
                else:
                    d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])

            # mutant_sol[j] = d_val + get_levy_flight_step(beta=1, multiplier=0.01, case=-1)
            mutant_sol[j] = d_val


        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_, cr

# test-2022/5/28: adaptive parameters
def update_animals_improvedHGS_test2(gbest, shrink, L, hunger, total_hunger, eps, in_, T2, cr, p_best, cur_iter, v_max, v_min, delta_list):
    wMax = 0.9
    wMin = 0.2
    c1 = 2
    c2 = 2
    if cur_iter == 0:
        alpha = 1
    else:
        alpha = 1 / (1 + (10 ** (- 10 / cur_iter)))


    N, D = in_.shape

    for i in range(N):
        if np.random.uniform(0, 1) < T2:
            cr[i] = np.random.uniform(0, 1)

    R = 2 * shrink * np.random.rand() - shrink
    for i in range(N):
        aa = 2 * (np.sin(delta_list[i]))
        bb = 2 * (np.cos(delta_list[i]))
        ee = abs(np.cos(delta_list[i])) ** aa
        tt = abs(np.sin(delta_list[i])) ** bb
        w = wMax - i * ((wMax - wMin) / N)
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)

        r1 = np.random.rand()
        r2 = np.random.rand()
        for j in range(D):
            if random.random() > cr[i] or j == j_rand:  
                # d_val = in_[i, j]
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                if np.random.rand() < alpha:
                    d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
                else:
                    v = ee * (p_best[i, j] - in_[i, j]) + tt * (gbest[i, j] - in_[i, j])
                    v = np.maximum(np.minimum(v_max[0], v), v_min[0])
                    d_val = in_[i, j] + v
            mutant_sol[j] = d_val

        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])
        delta_list[i] += abs(aa + bb) * (2 * np.pi)

    return in_, cr

def update_animals_improvedHGS_test3(gbest, shrink, L, hunger, total_hunger, eps, in_, T2, cr, fitness, fitness_g, cur_iter, max_iter, pbest):
    N, D = in_.shape

    # for i in range(N):
    #     if np.random.uniform(0, 1) < T2:
    #         cr[i] = np.random.uniform(0, 1)
    cr = np.random.normal(0.5, 0.1, N)
    R = 2 * shrink * np.random.rand() - shrink

    cr = 1 - (0.55 + 1 / np.pi * np.arctan((1 - cur_iter / max_iter - 0.8) / 0.1))

    for i in range(N):
        # parameter_I = (fitness[i, 0] - np.min(fitness[i, 0])) / (np.max(fitness[i, 0]) - np.min(fitness[i, 0]))
        # if parameter_I >= ((1 - 0.6) * np.random.rand() + 0.6):
        #     cr[i] = 0.6 * np.mean(cr_best) + (1 - 0.6) * (5 / N)
        # else:
        #     cr[i] = 0.6 * np.mean(cr_best) + (0.6) * (5 / N)
        ids_except_current = [_ for _ in range(N) if _ != i]
        r1_, r2_, r3_ = random.sample(ids_except_current, 3)
        E = sech(np.min(fitness[i]) - np.min(fitness_g[i]))
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)
        for j in range(D):
            if random.random() > cr or j == j_rand:  
                # d_val = in_[i, j]
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                d_val = W1 * gbest[i, j] - R * W2 * abs(gbest[i, j] - in_[i, j])
                # if np.random.rand() < E:
                #     d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
                #     # d_val = W1 * pbest[i, j] + R * W2 * abs(pbest[i, j] - in_[i, j])
                
                #     d_val = W1 * gbest[i, j] - R * W2 * abs(gbest[i, j] - in_[i, j])
                #     # d_val = in_[r1_, j] + 0.5 * (in_[r2_, j] - in_[r3_, j])
            mutant_sol[j] = d_val

        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_, cr

def update_animals_improvedHGS_test4(gbest, shrink, L, hunger, total_hunger, eps, in_, T2, cr, cur_iter, pbest):
    N, D = in_.shape

    if cur_iter == 0:
        alpha = 1
    else:
        alpha = 1 / (1 + (10 ** (- 10 / cur_iter)))

    for i in range(N):
        if np.random.uniform(0, 1) < T2:
            cr[i] = np.random.uniform(0, 1)

    R = 2 * shrink * np.random.rand() - shrink
    for i in range(N):
        if np.random.rand() < L:
            W1 = hunger[i, 0] * N / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        j_rand = np.random.randint(0, D)
        mutant_sol = np.zeros(D)

        ids_except_current = [_ for _ in range(N) if _ != i]
        r1_, r2_, r3_ = random.sample(ids_except_current, 3)
        for j in range(D):
            if random.random() > cr[i] or j == j_rand:  
                # d_val = in_[i, j]
                d_val = in_[i, j] * (1 + np.random.normal(0, 0.0001))
            else:
                if np.random.rand() > alpha:
                    # d_val = in_[r1_, j] + 0.5 * (in_[r2_, j] - in_[r3_, j])
                    d_val = W1 * pbest[i, j] + R * W2 * abs(pbest[i, j] - in_[i, j])

                else:
                    d_val = W1 * gbest[i, j] + R * W2 * abs(gbest[i, j] - in_[i, j])
            mutant_sol[j] = d_val

        in_[i] = mutant_sol
        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_, cr


def update_animals_DEHGS(particles, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, vmax, vmin):
    # for i in range(particles):
    R = 2 * shrink * np.random.rand() - shrink
    param_pool = [[1.0, 0.1], [1.0, 0.9], [0.8, 0.2]]
    for i in range(particles):
        E = sech(np.min(fit[i]) - np.min(fitness_g[i]))
        if np.random.rand() < L:
            W1 = hunger[i, 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[i, 0] - total_hunger))) * np.random.rand() * 2

        r1 = np.random.rand()
        r2 = np.random.rand()
        shuffle(param_pool)
        ids_except_current = [_ for _ in range(particles) if _ != i]
        rand1_, rand2_, rand3_ = random.sample(ids_except_current, 3)
        if r1 < L:
            in_[i] = in_[rand1_] + param_pool[0][0] * (in_[rand2_] - in_[rand3_])
        else:
            if r2 > E:
                in_[i] = W1 * gbest[i] + R * W2 * abs(gbest[i] - in_[i])
            else:
                in_[i] = W1 * gbest[i] - R * W2 * abs(gbest[i] - in_[i])

        in_[i] = ensure_min_max_constraints(in_[i])
        in_[i] = adjust_slack_power(in_[i])

    return in_


def update_animals_mHGS(particles, Ns1, Ns2, Ns3, f, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, countGau, countCau, countLevy, current_iteration):
    # for i in range(particles):
    R = 2 * shrink * np.random.rand() - shrink

    sortedFit = np.argsort(hunger[:, 0])
    # print('sortedFit:', sortedFit)

    for a_i in range(Ns1):
        E = sech(fit[sortedFit[a_i]] - fitness_g[sortedFit[a_i]])
        if np.random.rand() < L:
            W1 = hunger[sortedFit[a_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[a_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != a_i]
        id_1, id_2, id_3 = random.sample(ids_except_current, 3)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            in_[sortedFit[a_i]] = in_[sortedFit[a_i]] * (1 + np.random.normal(0, 1))
            # in_[sortedFit[a_i]] = in_[id_1] + f[sortedFit[a_i]] * (in_[id_2] - in_[id_3])
        else:
            if r2 > E.any():
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] + c * R * W2 * abs(
                    gbest[sortedFit[a_i]] - in_[sortedFit[a_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[a_i]])
            else:
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] - (
                        c * R * W2 * abs(gbest[sortedFit[a_i]] - in_[sortedFit[a_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[a_i]]))

        in_[sortedFit[a_i]] = ensure_min_max_constraints(in_[sortedFit[a_i]])
        in_[sortedFit[a_i]] = adjust_slack_power(in_[sortedFit[a_i]])

    for b_i in range(Ns2):
        E = sech(fit[sortedFit[Ns1 + b_i]] - fitness_g[sortedFit[Ns1 + b_i]])
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + b_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[Ns1 + b_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != b_i]
        id_1, id_2, id_3 = random.sample(ids_except_current, 3)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            in_[sortedFit[Ns1 + b_i]] = in_[sortedFit[Ns1 + b_i]] + f[sortedFit[Ns1 + b_i]] * (
                        in_[id_1] - in_[sortedFit[Ns1 + b_i]]) + f[sortedFit[Ns1 + b_i]] * (in_[id_2] - in_[id_2])
        else:
            if r2 > E.any():
                in_[sortedFit[Ns1 + b_i]] = W1 * gbest[sortedFit[Ns1 + b_i]] + c * R * W2 * abs(
                    gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[Ns1 + b_i]])
            else:
                in_[sortedFit[Ns1 + b_i]] = W1 * gbest[sortedFit[Ns1 + b_i]] - (
                        c * R * W2 * abs(gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]]) + (
                            1 - c) * R * W2 * abs(in_avg - in_[sortedFit[Ns1 + b_i]]))

        in_[sortedFit[Ns1 + b_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + b_i]])
        in_[sortedFit[Ns1 + b_i]] = adjust_slack_power(in_[sortedFit[Ns1 + b_i]])

    for c_i in range(Ns3):
        E = sech(fit[sortedFit[Ns1 + Ns2 + c_i]] - fitness_g[sortedFit[Ns1 + Ns2 + c_i]])
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + Ns2 + c_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[Ns1 + Ns2 + c_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != c_i]
        id_1, id_2, id_3, id_4, id_5 = random.sample(ids_except_current, 5)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            # DE/rand/2
            in_[sortedFit[Ns1 + Ns2 + c_i]] = in_[id_1] + f[sortedFit[Ns1 + Ns2 + c_i]] * (in_[id_2] - in_[id_3]) + f[sortedFit[Ns1 + Ns2 + c_i]] * (
                        in_[id_4] - in_[id_5])
        else:
            if r2 > E.any():
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] + c * R * W2 * abs(
                    gbest[sortedFit[Ns1 + Ns2 + c_i]] - in_[sortedFit[Ns1 + Ns2 + c_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[Ns1 + Ns2 + c_i]])
            else:
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] - (
                        c * R * W2 * abs(gbest[sortedFit[Ns1 + Ns2 + c_i]] - in_[sortedFit[Ns1 + Ns2 + c_i]]) + (
                            1 - c) * R * W2 * abs(in_avg - in_[sortedFit[Ns1 + Ns2 + c_i]]))

        in_[sortedFit[Ns1 + Ns2 + c_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + Ns2 + c_i]])
        in_[sortedFit[Ns1 + Ns2 + c_i]] = adjust_slack_power(in_[sortedFit[Ns1 + Ns2 + c_i]])

    # if current_iteration % 10 ==0:
    Ns1, Ns2, Ns3, countGau, countCau, countLevy = check_strategy(NO_OF_AGENTS=particles, gauFit=fit[sortedFit[:Ns1]],
                                   cauFit=fit[sortedFit[Ns1:(Ns1 + Ns2)]],
                                   levyFit=fit[sortedFit[Ns2:]], Ns1=Ns1, Ns2=Ns2, Ns3=Ns3, hunger_list_Gau=hunger[sortedFit[:Ns1], 0], hunger_list_Cau=hunger[sortedFit[Ns1:(Ns1 + Ns2)], 0],
                                       hunger_list_Levy=hunger[sortedFit[Ns2:], 0],
                                       sum_hunger_list=total_hunger,countGau=countGau, countCau=countCau, countLevy=countLevy)

    # for i in range(particles):
    #     E = sech(fit[i] - fitness_g[i])
    #     if np.random.rand() < L:
    #         W1 = hunger[i] * particles / (total_hunger + eps) * np.random.rand()
    #     else:
    #         W1 = 1
    #     W2 = (1 - np.exp(-abs(hunger[i] - total_hunger))) * np.random.rand() * 2
    #
    #     r1 = np.random.rand()
    #     r2 = np.random.rand()
    #     if r1 < L:
    #         in_[i] = in_[i] * (1 + np.random.normal(0, 1))
    #     else:
    #         if r2 > E.any():
    #             in_[i] = W1 * gbest[i] + R * W2 * abs(gbest[i] - in_[i])
    #         else:
    #             in_[i] = W1 * gbest[i] - R * W2 * abs(gbest[i] - in_[i])
    #
    #     in_[i] = ensure_min_max_constraints(in_[i])
    #     in_[i] = adjust_slack_power(in_[i])

    return in_, Ns1, Ns2, Ns3, countGau, countCau, countLevy

def update_animals_mHGS_withoutAVG(particles, Ns1, Ns2, Ns3, f, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, countGau, countCau, countLevy, current_iteration):
    # for i in range(particles):
    R = 2 * shrink * np.random.rand() - shrink

    sortedFit = np.argsort(hunger[:, 0])
    # print('sortedFit:', sortedFit)

    for a_i in range(Ns1):
        E = sech(fit[sortedFit[a_i]] - fitness_g[sortedFit[a_i]])
        if np.random.rand() < L:
            W1 = hunger[sortedFit[a_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[a_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != a_i]
        id_1, id_2, id_3 = random.sample(ids_except_current, 3)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            in_[sortedFit[a_i]] = in_[sortedFit[a_i]] * (1 + np.random.normal(0, 1))
            # in_[sortedFit[a_i]] = in_[id_1] + f[sortedFit[a_i]] * (in_[id_2] - in_[id_3])
        else:
            if r2 > E.any():
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] + R * W2 * abs(
                    gbest[sortedFit[a_i]] - in_[sortedFit[a_i]])
            else:
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] - R * W2 * abs(gbest[sortedFit[a_i]] - in_[sortedFit[a_i]])

        in_[sortedFit[a_i]] = ensure_min_max_constraints(in_[sortedFit[a_i]])
        in_[sortedFit[a_i]] = adjust_slack_power(in_[sortedFit[a_i]])

    for b_i in range(Ns2):
        E = sech(fit[sortedFit[Ns1 + b_i]] - fitness_g[sortedFit[Ns1 + b_i]])
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + b_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[Ns1 + b_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != b_i]
        id_1, id_2, id_3 = random.sample(ids_except_current, 3)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            in_[sortedFit[Ns1 + b_i]] = in_[sortedFit[Ns1 + b_i]] + f[sortedFit[Ns1 + b_i]] * (
                        in_[id_1] - in_[sortedFit[Ns1 + b_i]]) + f[sortedFit[Ns1 + b_i]] * (in_[id_2] - in_[id_2])
        else:
            if r2 > E.any():
                in_[sortedFit[Ns1 + b_i]] = W1 * gbest[sortedFit[Ns1 + b_i]] + R * W2 * abs(
                    gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]])
            else:
                in_[sortedFit[Ns1 + b_i]] = W1 * gbest[sortedFit[Ns1 + b_i]] - R * W2 * abs(gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]])

        in_[sortedFit[Ns1 + b_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + b_i]])
        in_[sortedFit[Ns1 + b_i]] = adjust_slack_power(in_[sortedFit[Ns1 + b_i]])

    for c_i in range(Ns3):
        E = sech(fit[sortedFit[Ns1 + Ns2 + c_i]] - fitness_g[sortedFit[Ns1 + Ns2 + c_i]])
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + Ns2 + c_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[Ns1 + Ns2 + c_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != c_i]
        id_1, id_2, id_3, id_4, id_5 = random.sample(ids_except_current, 5)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            # DE/rand/2
            in_[sortedFit[Ns1 + Ns2 + c_i]] = in_[id_1] + f[sortedFit[Ns1 + Ns2 + c_i]] * (in_[id_2] - in_[id_3]) + f[sortedFit[Ns1 + Ns2 + c_i]] * (
                        in_[id_4] - in_[id_5])
        else:
            if r2 > E.any():
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] + R * W2 * abs(
                    gbest[sortedFit[Ns1 + Ns2 + c_i]] - in_[sortedFit[Ns1 + Ns2 + c_i]])
            else:
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] - R * W2 * abs(gbest[sortedFit[Ns1 + Ns2 + c_i]] - in_[sortedFit[Ns1 + Ns2 + c_i]])

        in_[sortedFit[Ns1 + Ns2 + c_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + Ns2 + c_i]])
        in_[sortedFit[Ns1 + Ns2 + c_i]] = adjust_slack_power(in_[sortedFit[Ns1 + Ns2 + c_i]])

    # if current_iteration % 10 ==0:
    Ns1, Ns2, Ns3, countGau, countCau, countLevy = check_strategy(NO_OF_AGENTS=particles, gauFit=fit[sortedFit[:Ns1]],
                                   cauFit=fit[sortedFit[Ns1:(Ns1 + Ns2)]],
                                   levyFit=fit[sortedFit[Ns2:]], Ns1=Ns1, Ns2=Ns2, Ns3=Ns3, hunger_list_Gau=hunger[sortedFit[:Ns1], 0], hunger_list_Cau=hunger[sortedFit[Ns1:(Ns1 + Ns2)], 0],
                                       hunger_list_Levy=hunger[sortedFit[Ns2:], 0],
                                       sum_hunger_list=total_hunger,countGau=countGau, countCau=countCau, countLevy=countLevy)

    # for i in range(particles):
    #     E = sech(fit[i] - fitness_g[i])
    #     if np.random.rand() < L:
    #         W1 = hunger[i] * particles / (total_hunger + eps) * np.random.rand()
    #     else:
    #         W1 = 1
    #     W2 = (1 - np.exp(-abs(hunger[i] - total_hunger))) * np.random.rand() * 2
    #
    #     r1 = np.random.rand()
    #     r2 = np.random.rand()
    #     if r1 < L:
    #         in_[i] = in_[i] * (1 + np.random.normal(0, 1))
    #     else:
    #         if r2 > E.any():
    #             in_[i] = W1 * gbest[i] + R * W2 * abs(gbest[i] - in_[i])
    #         else:
    #             in_[i] = W1 * gbest[i] - R * W2 * abs(gbest[i] - in_[i])
    #
    #     in_[i] = ensure_min_max_constraints(in_[i])
    #     in_[i] = adjust_slack_power(in_[i])

    return in_, Ns1, Ns2, Ns3, countGau, countCau, countLevy


def update_animals_mHGS_withoutM(particles, Ns1, Ns2, Ns3, f, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_, vmax, vmin):
    # for i in range(particles):
    R = 2 * shrink * np.random.rand() - shrink

    sortedFit = np.argsort(hunger[:, 0])
    # print('sortedFit:', sortedFit)

    for a_i in range(Ns1):
        E = sech(np.min(fit[sortedFit[a_i]]) - np.min(fitness_g[sortedFit[a_i]]))
        if np.random.rand() < L:
            W1 = hunger[sortedFit[a_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[a_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != a_i]
        id_1, id_2, id_3 = random.sample(ids_except_current, 3)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            in_[sortedFit[a_i]] = in_[id_1] + f[sortedFit[a_i]] * (in_[id_2] - in_[id_3])
        else:
            if r2 > E:
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] + c * R * W2 * abs(
                    gbest[sortedFit[a_i]] - in_[sortedFit[a_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[a_i]])
            else:
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] - (
                        c * R * W2 * abs(gbest[sortedFit[a_i]] - in_[sortedFit[a_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[a_i]]))

        in_[sortedFit[a_i]] = ensure_min_max_constraints(in_[sortedFit[a_i]])
        in_[sortedFit[a_i]] = adjust_slack_power(in_[sortedFit[a_i]])

    for b_i in range(Ns2):
        E = sech(np.min(fit[sortedFit[Ns1 + b_i]]) - np.min(fitness_g[sortedFit[Ns1 + b_i]]))
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + b_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[Ns1 + b_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != b_i]
        id_1, id_2, id_3 = random.sample(ids_except_current, 3)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            in_[sortedFit[Ns1 + b_i]] = in_[sortedFit[Ns1 + b_i]] + f[sortedFit[Ns1 + b_i]] * (
                        in_[id_1] - in_[sortedFit[Ns1 + b_i]]) + f[sortedFit[Ns1 + b_i]] * (in_[id_2] - in_[id_2])
        else:
            if r2 > E:
                in_[sortedFit[Ns1 + b_i]] = W1 * gbest[sortedFit[Ns1 + b_i]] + c * R * W2 * abs(
                    gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[Ns1 + b_i]])
            else:
                in_[sortedFit[Ns1 + b_i]] = W1 * gbest[sortedFit[Ns1 + b_i]] - (
                        c * R * W2 * abs(gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]]) + (
                            1 - c) * R * W2 * abs(in_avg - in_[sortedFit[Ns1 + b_i]]))

        in_[sortedFit[Ns1 + b_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + b_i]])
        in_[sortedFit[Ns1 + b_i]] = adjust_slack_power(in_[sortedFit[Ns1 + b_i]])

    for c_i in range(Ns3):
        E = sech(np.min(fit[sortedFit[Ns1 + Ns2 + c_i]]) - np.min(fitness_g[sortedFit[Ns1 + Ns2 + c_i]]))
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + Ns2 + c_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[Ns1 + Ns2 + c_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in range(particles) if _ != c_i]
        id_1, id_2, id_3, id_4, id_5 = random.sample(ids_except_current, 5)
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()
        c = np.random.rand()

        if r1 < L:
            # DE/rand/2
            in_[sortedFit[Ns1 + Ns2 + c_i]] = in_[id_1] + f[sortedFit[Ns1 + Ns2 + c_i]] * (in_[id_2] - in_[id_3]) + f[sortedFit[Ns1 + Ns2 + c_i]] * (
                        in_[id_4] - in_[id_5])
        else:
            if r2 > E:
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] + c * R * W2 * abs(
                    gbest[sortedFit[Ns1 + Ns2 + c_i]] - in_[sortedFit[Ns1 + Ns2 + c_i]]) + (1 - c) * R * W2 * abs(
                    in_avg - in_[sortedFit[Ns1 + Ns2 + c_i]])
            else:
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] - (
                        c * R * W2 * abs(gbest[sortedFit[Ns1 + Ns2 + c_i]] - in_[sortedFit[Ns1 + Ns2 + c_i]]) + (
                            1 - c) * R * W2 * abs(in_avg - in_[sortedFit[Ns1 + Ns2 + c_i]]))

        in_[sortedFit[Ns1 + Ns2 + c_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + Ns2 + c_i]])
        in_[sortedFit[Ns1 + Ns2 + c_i]] = adjust_slack_power(in_[sortedFit[Ns1 + Ns2 + c_i]])

    return in_

def update_animals_PhasorDMPHGS(Ns1, Ns2, Ns3, fit, gbest, fitness_g, shrink, L, hunger, total_hunger, eps, in_,
                                delta_list, in_pbest, archive_in):
    particles, dim = in_.shape
    R = 2 * shrink * np.random.rand() - shrink

    # sortedFit = np.argsort(hunger[:, 0])
    sortedFit = [_ for _ in range(particles)]

    for a_i in range(Ns1):
        E = sech(np.min(fit[sortedFit[a_i]]) - np.min(fitness_g[sortedFit[a_i]]))
        if np.random.rand() < L:
            W1 = hunger[sortedFit[a_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1
        W2 = (1 - np.exp(-abs(hunger[sortedFit[a_i], 0] - total_hunger))) * np.random.rand() * 2

        ids_except_current = [_ for _ in archive_in.tolist() if _ != sortedFit[a_i]]
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (np.asarray(id_A) + np.asarray(id_B) + np.asarray(id_C)) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()

        if r1 < L:
            in_[sortedFit[a_i]] = in_[sortedFit[a_i]] * (1 + np.random.normal(0, 1))
        else:
            if r2 > E:
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] + R * W2 * abs(
                    gbest[sortedFit[a_i]] - in_[sortedFit[a_i]]) + R * W2 * abs(
                    in_avg - in_[sortedFit[a_i]])
            else:
                in_[sortedFit[a_i]] = W1 * gbest[sortedFit[a_i]] - (
                        R * W2 * abs(gbest[sortedFit[a_i]] - in_[sortedFit[a_i]]) + R * W2 * abs(
                    in_avg - in_[sortedFit[a_i]]))

        in_[sortedFit[a_i]] = ensure_min_max_constraints(in_[sortedFit[a_i]])
        in_[sortedFit[a_i]] = adjust_slack_power(in_[sortedFit[a_i]])

    for b_i in range(Ns2):
        aa = 2 * (np.sin(delta_list[b_i]))
        bb = 2 * (np.cos(delta_list[b_i]))
        ee = abs(np.cos(delta_list[b_i])) ** aa
        tt = abs(np.sin(delta_list[b_i])) ** bb

        in_[sortedFit[Ns1 + b_i]] = ee * (in_pbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]]) + tt * (
                    gbest[sortedFit[Ns1 + b_i]] - in_[sortedFit[Ns1 + b_i]])

        delta_list[b_i] += abs(aa + bb) * (2 * np.pi)
        in_[sortedFit[Ns1 + b_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + b_i]])
        in_[sortedFit[Ns1 + b_i]] = adjust_slack_power(in_[sortedFit[Ns1 + b_i]])


    for c_i in range(Ns3):
        E = sech(np.min(fit[sortedFit[Ns1 + Ns2 + c_i]]) - np.min(fitness_g[sortedFit[Ns1 + Ns2 + c_i]]))
        if np.random.rand() < L:
            W1 = hunger[sortedFit[Ns1 + Ns2 + c_i], 0] * particles / (total_hunger + eps) * np.random.rand()
        else:
            W1 = 1

        ids_except_current = [_ for _ in range(particles) if _ != c_i]
        id_A, id_B, id_C = random.sample(ids_except_current, 3)

        in_avg = (in_[id_A] + in_[id_B] + in_[id_C]) / 3

        r1 = np.random.rand()
        r2 = np.random.rand()

        if r1 < L:
            in_[sortedFit[Ns1 + Ns2 + c_i]] = in_[sortedFit[Ns1 + Ns2 + c_i]] * (1 + np.random.normal(0, 1))
        else:
            levy = get_levy_flight_step(multiplier=0.01, case=-1)
            if r2 > E:
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] + levy * abs(in_avg - in_[sortedFit[Ns1 + Ns2 + c_i]])
            else:
                in_[sortedFit[Ns1 + Ns2 + c_i]] = W1 * gbest[sortedFit[Ns1 + Ns2 + c_i]] - levy * abs(in_avg - in_[sortedFit[Ns1 + Ns2 + c_i]])

        in_[sortedFit[Ns1 + Ns2 + c_i]] = ensure_min_max_constraints(in_[sortedFit[Ns1 + Ns2 + c_i]])
        in_[sortedFit[Ns1 + Ns2 + c_i]] = adjust_slack_power(in_[sortedFit[Ns1 + Ns2 + c_i]])

    return in_, delta_list


def get_levy_flight_step(beta=1.0, multiplier=0.001, case=0):
    """
            Parameters
            ----------
            multiplier (float, optional): 0.01
            beta: [0-2]
                + 0-1: small range --> exploit
                + 1-2: large range --> explore
            case: 0, 1, -1
                + 0: return multiplier * s * np.random.uniform()
                + 1: return multiplier * s * np.random.normal(0, 1)
                + -1: return multiplier * s
            """
    # u and v are two random variables which follow np.random.normal distribution
    # sigma_u : standard deviation of u
    sigma_u = np.power(
        gamma(1 + beta) * np.sin(np.pi * beta / 2) / (gamma((1 + beta) / 2) * beta * np.power(2, (beta - 1) / 2)),
        1 / beta)
    # sigma_v : standard deviation of v
    sigma_v = 1
    u = np.random.normal(0, sigma_u ** 2)
    v = np.random.normal(0, sigma_v ** 2)
    s = u / np.power(abs(v), 1 / beta)
    if case == 0:
        step = multiplier * s * np.random.uniform()
    elif case == 1:
        step = multiplier * s * np.random.normal(0, 1)
    else:
        step = multiplier * s
    return step
