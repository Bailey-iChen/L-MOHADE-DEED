#encoding: utf-8

from pathlib import Path
import numpy as np
from public import constants_5unit as deed
from public import init, update, P_objective
from l_mohade.LMOHADE import LMOHADE
import FindCompromisedSolution


def main():
    # The shared objective, initialization and repair routines use this case.
    if not all(module.deed is deed for module in (init, update, P_objective)):
        raise ValueError("DEED case mismatch: main, init, update and P_objective must use the same data module.")

    particals = 100  
    cycle_ = 10000  
    mesh_div = 100  
    
    thresh = 100  

    NumOfRuns = 5


    # Problem = "ZDT1"
    Problem = "DEED"
    # Problem = ZDT1()
    # Problem.reference_front = read_solutions(filename="public/ZDT1.pf")
    M = 2
    Population, Boundary, Coding = P_objective.P_objective("init", Problem, M, particals)
    max_ = Boundary[0]
    min_ = Boundary[1]

    # max_ = np.zeros((deed.NO_OF_HOURS, deed.NO_OF_GENERATORS))
    # min_ = np.zeros((deed.NO_OF_HOURS, deed.NO_OF_GENERATORS))
    # for h in range(deed.NO_OF_HOURS):
    #     for g in range(deed.NO_OF_GENERATORS):
    #         max_[h, g] = deed.GENERATORS_MAX_POWER[g]
    #         min_[h, g] = deed.GENERATORS_MIN_POWER[g]
    # max_ = max_.reshape((deed.NO_OF_GENERATORS * deed.NO_OF_HOURS))
    # min_ = min_.reshape((deed.NO_OF_GENERATORS * deed.NO_OF_HOURS))
    output_avg = True
    # results_directory = time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    
    results_directory = Path(__file__).resolve().parents[1] / "results" / "DEED_5unit_LMOHADE"

    Path(results_directory).mkdir(parents=True, exist_ok=True)

    # Additional tests
    fitness_hgs_10 = [0] * NumOfRuns
    position_hgs_10 = [0] * NumOfRuns
    fitness_hgs_1 = [0] * NumOfRuns
    position_hgs_1 = [0] * NumOfRuns
    fitness_hgs_01 = [0] * NumOfRuns
    position_hgs_01 = [0] * NumOfRuns
    fitness_hgs_001 = [0] * NumOfRuns
    position_hgs_001 = [0] * NumOfRuns
    fitness_hgs_0001 = [0] * NumOfRuns
    position_hgs_0001 = [0] * NumOfRuns
    fitness_hgs_00001 = [0] * NumOfRuns
    position_hgs_00001 = [0] * NumOfRuns

    fitness_hgs_l_01 = [0] * NumOfRuns
    position_hgs_l_01 = [0] * NumOfRuns
    fitness_hgs_l_006 = [0] * NumOfRuns
    position_hgs_l_006 = [0] * NumOfRuns
    fitness_hgs_l_007 = [0] * NumOfRuns
    position_hgs_l_007 = [0] * NumOfRuns
    fitness_hgs_l_008 = [0] * NumOfRuns
    position_hgs_l_008 = [0] * NumOfRuns
    fitness_hgs_l_009 = [0] * NumOfRuns
    position_hgs_l_009 = [0] * NumOfRuns
    fitness_hgs_l_tvl = [0] * NumOfRuns
    position_hgs_l_tvl = [0] * NumOfRuns


    fitness_lmohade_l_01 = [0] * NumOfRuns
    position_lmohade_l_01 = [0] * NumOfRuns
    fitness_lmohade_l_006 = [0] * NumOfRuns
    position_lmohade_l_006 = [0] * NumOfRuns
    fitness_lmohade_l_007 = [0] * NumOfRuns
    position_lmohade_l_007 = [0] * NumOfRuns
    fitness_lmohade_l_008 = [0] * NumOfRuns
    position_lmohade_l_008 = [0] * NumOfRuns
    fitness_lmohade_l_009 = [0] * NumOfRuns
    position_lmohade_l_009 = [0] * NumOfRuns

    fitness_lmohade_10 = [0] * NumOfRuns
    position_lmohade_10 = [0] * NumOfRuns
    fitness_lmohade_1 = [0] * NumOfRuns
    position_lmohade_1 = [0] * NumOfRuns
    fitness_lmohade_01 = [0] * NumOfRuns
    position_lmohade_01 = [0] * NumOfRuns
    fitness_lmohade_001 = [0] * NumOfRuns
    position_lmohade_001 = [0] * NumOfRuns
    fitness_lmohade_0001 = [0] * NumOfRuns
    position_lmohade_0001 = [0] * NumOfRuns
    fitness_lmohade_ms = [0] * NumOfRuns
    position_lmohade_ms = [0] * NumOfRuns
    fitness_lmohade_00001 = [0] * NumOfRuns
    position_lmohade_00001 = [0] * NumOfRuns

    fitness_lmohade_10 = [0] * NumOfRuns
    position_lmohade_10 = [0] * NumOfRuns
    fitness_lmohade_100 = [0] * NumOfRuns
    position_lmohade_100 = [0] * NumOfRuns
    fitness_lmohade_1000 = [0] * NumOfRuns
    position_lmohade_1000 = [0] * NumOfRuns
    fitness_lmohade_10000 = [0] * NumOfRuns
    position_lmohade_10000 = [0] * NumOfRuns





    # HGS
    fitness_hgs = [0] * NumOfRuns
    position_hgs = [0] * NumOfRuns
    fitness_ihgs = [0] * NumOfRuns
    position_ihgs = [0] * NumOfRuns
    fitness_lmohade = [0] * NumOfRuns
    position_lmohade = [0] * NumOfRuns

    fitness_mplmohade = [0] * NumOfRuns
    position_mplmohade = [0] * NumOfRuns

    fitness_phasordmphgs = [0] * NumOfRuns
    position_phasordmphgs = [0] * NumOfRuns
    fitness_pso = [0] * NumOfRuns
    position_pso = [0] * NumOfRuns
    fitness_ppso = [0] * NumOfRuns
    position_ppso = [0] * NumOfRuns

    fitness_woa = [0] * NumOfRuns
    position_woa = [0] * NumOfRuns

    fitness_hs = [0] * NumOfRuns
    position_hs = [0] * NumOfRuns

    fitness_de = [0] * NumOfRuns
    position_de = [0] * NumOfRuns
    fitness_imode = [0] * NumOfRuns
    position_imode = [0] * NumOfRuns
    fitness_hjde = [0] * NumOfRuns
    position_hjde = [0] * NumOfRuns

    fitness_sma = [0] * NumOfRuns
    position_sma = [0] * NumOfRuns
    for i in range(0, NumOfRuns):

        # Additional tests

        ###############       SMA
        
        
        # fitness_sma[i] = mosma_pareto_fitness
        # position_sma[i] = mosma_pareto_in
        # sma_indexes_cs = FindCompromisedSolution.comprosed_solution(mosma_pareto_fitness)
        # np.savetxt(str(results_directory) + "/" + "SMA_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "SMA_pareto_position" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOSMA_compromised_solution" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_l_01[i] = mohgs_al_pareto_al_fitness_l_01
        # position_lmohade_l_01[i] = mohgs_al_pareto_in_l_01
        # hgs_al_indexes_cs_l_01 = FindCompromisedSolution.comprosed_solution(mohgs_al_pareto_al_fitness_l_01)
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_fitness_l_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_position_l_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l01_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_l_006[i] = mohgs_al_pareto_al_fitness_l_006
        # position_lmohade_l_006[i] = mohgs_al_pareto_in_l_006
        # hgs_al_indexes_cs_l_006 = FindCompromisedSolution.comprosed_solution(mohgs_al_pareto_al_fitness_l_006)
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_fitness_l_006_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_position_l_006_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l006_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_l_007[i] = mohgs_al_pareto_al_fitness_l_007
        # position_lmohade_l_007[i] = mohgs_al_pareto_in_l_007
        # hgs_al_indexes_cs_l_007 = FindCompromisedSolution.comprosed_solution(mohgs_al_pareto_al_fitness_l_007)
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_fitness_l_007_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_position_l_007_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l007_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_l_008[i] = mohgs_al_pareto_al_fitness_l_008
        # position_lmohade_l_008[i] = mohgs_al_pareto_in_l_008
        # hgs_al_indexes_cs_l_008 = FindCompromisedSolution.comprosed_solution(mohgs_al_pareto_al_fitness_l_008)
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_fitness_l_008_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_position_l_008_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l008_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_l_009[i] = mohgs_al_pareto_al_fitness_l_009
        # position_lmohade_l_009[i] = mohgs_al_pareto_in_l_009
        # hgs_al_indexes_cs_l_009 = FindCompromisedSolution.comprosed_solution(mohgs_al_pareto_al_fitness_l_009)
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_fitness_l_007_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGSAL_pareto_position_l_009_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l009_" + str(i) + ".txt",
        

        
        
        # fitness_hgs_l_01[i] = mohgs_pareto_fitness_l_01
        # position_hgs_l_01[i] = mohgs_pareto_in_l_01
        # hgs_indexes_cs_l_01 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_l_01)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_l_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_l_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l01_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_l_006[i] = mohgs_pareto_fitness_l_006
        # position_hgs_l_006[i] = mohgs_pareto_in_l_006
        # hgs_indexes_cs_l_006 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_l_006)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_l_006_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_l_006_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l006_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_l_007[i] = mohgs_pareto_fitness_l_007
        # position_hgs_l_007[i] = mohgs_pareto_in_l_007
        # hgs_indexes_cs_l_007 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_l_007)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_l_007_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_l_007_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l007_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_l_008[i] = mohgs_pareto_fitness_l_008
        # position_hgs_l_008[i] = mohgs_pareto_in_l_008
        # hgs_indexes_cs_l_008 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_l_008)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_l_008_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_l_008_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l008_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_l_009[i] = mohgs_pareto_fitness_l_009
        # position_hgs_l_009[i] = mohgs_pareto_in_l_009
        # hgs_indexes_cs_l_009 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_l_009)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_l_009_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_l_009_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_l009_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_l_tvl[i] = mohgs_pareto_fitness_l_tvl
        # position_hgs_l_tvl[i] = mohgs_pareto_in_l_tvl
        # hgs_indexes_cs_l_tvl = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_l_tvl)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_l_tvl_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_l_tvl_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution_ltvl_" + str(i) + ".txt",
        

        
        
        # fitness_hgs_10[i] = mohgs_pareto_fitness_10
        # position_hgs_10[i] = mohgs_pareto_in_10
        # hgs_indexes_cs_10 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_10)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_10_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_10_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution10_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_1[i] = mohgs_pareto_fitness_1
        # position_hgs_1[i] = mohgs_pareto_in_1
        # hgs_indexes_cs_1 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_1)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_1_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_1_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution1_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_01[i] = mohgs_pareto_fitness_01
        # position_hgs_01[i] = mohgs_pareto_in_01
        # hgs_indexes_cs_01 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_01)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution01_" + str(i) + ".txt",
        

        
        
        # fitness_hgs_001[i] = mohgs_pareto_fitness_001
        # position_hgs_001[i] = mohgs_pareto_in_001
        # hgs_indexes_cs_001 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_001)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution001_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_0001[i] = mohgs_pareto_fitness_0001
        # position_hgs_0001[i] = mohgs_pareto_in_0001
        # hgs_indexes_cs_0001 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_0001)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_0001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_0001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution0001_" + str(i) + ".txt",
        
        #
        
        
        # fitness_hgs_00001[i] = mohgs_pareto_fitness_00001
        # position_hgs_00001[i] = mohgs_pareto_in_00001
        # hgs_indexes_cs_00001 = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness_00001)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_00001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position_00001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution00001_" + str(i) + ".txt",
        


        
        
        # fitness_lmohade_10[i] = lmohade_pareto_fitness_10
        # position_lmohade_10[i] = lmohade_pareto_in_10
        # indexes_cs_10 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_10)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_10_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_10_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_10_" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_1[i] = lmohade_pareto_fitness_1
        # position_lmohade_1[i] = lmohade_pareto_in_1
        # indexes_cs_1 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_1)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_1_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_1_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_1_" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_01[i] = lmohade_pareto_fitness_01
        # position_lmohade_01[i] = lmohade_pareto_in_01
        # indexes_cs_01 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_01)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_01_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_01_" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_001[i] = lmohade_pareto_fitness_001
        # position_lmohade_001[i] = lmohade_pareto_in_001
        # indexes_cs_001 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_001)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_001_" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_0001[i] = lmohade_pareto_fitness_0001
        # position_lmohade_0001[i] = lmohade_pareto_in_0001
        # indexes_cs_0001 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_0001)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_0001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_0001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_0001_" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_ms[i] = lmohade_pareto_fitness_ms
        # position_lmohade_ms[i] = lmohade_pareto_in_ms
        # indexes_cs_0001 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_ms)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_ms" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_ms" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_ms" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_00001[i] = lmohade_pareto_fitness_00001
        # position_lmohade_00001[i] = lmohade_pareto_in_00001
        # indexes_cs_00001 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_00001)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_00001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_00001_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_00001_" + str(i) + ".txt",
        

        
        
        # fitness_lmohade_10[i] = lmohade_pareto_fitness_10
        # position_lmohade_10[i] = lmohade_pareto_in_10
        # indexes_cs_10 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_10)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_10_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_10_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_10_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_100[i] = lmohade_pareto_fitness_100
        # position_lmohade_100[i] = lmohade_pareto_in_100
        # indexes_cs_100 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_100)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_100_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_100_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_100_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_1000[i] = lmohade_pareto_fitness_1000
        # position_lmohade_1000[i] = lmohade_pareto_in_1000
        # indexes_cs_1000 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_1000)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_1000_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_1000_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_1000_" + str(i) + ".txt",
        
        #
        
        
        # fitness_lmohade_10000[i] = lmohade_pareto_fitness_10000
        # position_lmohade_10000[i] = lmohade_pareto_in_10000
        # indexes_cs_10000 = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness_10000)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness_10000_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position_10000_" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution_10000_" + str(i) + ".txt",
        

        # ###############       HGS
        
        
        # fitness_hgs[i] = mohgs_pareto_fitness
        # position_hgs[i] = mohgs_pareto_in
        # hgs_indexes_cs = FindCompromisedSolution.comprosed_solution(mohgs_pareto_fitness)
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HGS_pareto_position" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGS_compromised_solution" + str(i) + ".txt",
        

        ###############       IHGS
        
        
        # fitness_ihgs[i] = moihgs_pareto_fitness
        # position_ihgs[i] = moihgs_pareto_in
        # np.savetxt(str(results_directory) + "/" + "improvedHGS_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "improvedHGS_pareto_position" + str(i) + ".txt",
        


        # MOHGS with Archive
        
        
        # fitness_lmohade[i] = lmohade_pareto_fitness
        # position_lmohade[i] = lmohade_pareto_in
        # indexes_cs = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution" + str(i) + ".txt",
        

        # Multi-population MOHGS with Archive
        
        
        # fitness_mplmohade[i] = mplmohade_pareto_fitness
        # position_mplmohade[i] = mplmohade_pareto_in
        # indexes_cs = FindCompromisedSolution.comprosed_solution(mplmohade_pareto_fitness)
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_position" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "MOHGSwithArchive_compromised_solution" + str(i) + ".txt",
        

        ###############       PhasorDMPHGS
        
        
        # fitness_phasordmphgs[i] = phasordmphgs_pareto_fitness
        # position_phasordmphgs[i] = phasordmphgs_pareto_in
        # np.savetxt(str(results_directory) + "/" + "PhasorDMPHGS_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "PhasorDMPHGS_pareto_position" + str(i) + ".txt",
        


        # ###############       PSO
        
        
        # fitness_pso[i] = mopso_pareto_fitness
        # position_pso[i] = mopso_pareto_in
        # np.savetxt(str(results_directory) + "/" + "PSO_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "PSO_pareto_position" + str(i) + ".txt",
        
        # indexes_cs_pso = FindCompromisedSolution.comprosed_solution(mopso_pareto_fitness)
        # np.savetxt(str(results_directory) + "/" + "MOPSO_compromised_solution_" + str(i) + ".txt",
        

        # #
        #############       PPSO
        
        
        # fitness_ppso[i] = moppso_pareto_fitness
        # position_ppso[i] = moppso_pareto_in
        # np.savetxt(str(results_directory) + "/" + "PPSO_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "PPSO_pareto_position" + str(i) + ".txt",
        
        #

        # Author-designated base L-MOHADE; other variants remain separate.
        lmohade = LMOHADE(particals, max_, min_, thresh, mesh_div)
        lmohade_pareto_in, lmohade_pareto_fitness = lmohade.done(cycle_)
        fitness_lmohade[i] = lmohade_pareto_fitness
        position_lmohade[i] = lmohade_pareto_in
        np.savetxt(results_directory / ("LMOHADE_fitness" + str(i) + ".txt"),
                   fitness_lmohade[i])
        np.savetxt(results_directory / ("LMOHADE_position" + str(i) + ".txt"),
                   position_lmohade[i])
        indexes_cs = FindCompromisedSolution.comprosed_solution(lmohade_pareto_fitness)
        np.savetxt(results_directory / ("LMOHADE_compromised_solution" + str(i) + ".txt"),
                   lmohade_pareto_fitness[indexes_cs])

        ###############       DE
        
        
        # fitness_de[i] = mode_pareto_fitness
        # position_de[i] = mode_pareto_in
        # np.savetxt(str(results_directory) + "/" + "DE_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "DE_pareto_position" + str(i) + ".txt",
        

        #############       iMoDE
        
        
        # fitness_imode[i] = moimode_pareto_fitness
        # position_imode[i] = moimode_pareto_in
        # np.savetxt(str(results_directory) + "/" + "iMoDE_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "iMoDE_pareto_position" + str(i) + ".txt",
        
        # indexes_cs_iMoDE = FindCompromisedSolution.comprosed_solution(moimode_pareto_fitness)
        # np.savetxt(str(results_directory) + "/" + "MOiMoDE_compromised_solution_" + str(i) + ".txt",
        


        ###############       HjDE
        
        
        # fitness_imode[i] = mohjde_pareto_fitness
        # position_imode[i] = mohjde_pareto_in
        # np.savetxt(str(results_directory) + "/" + "HjDE_pareto_fitness" + str(i) + ".txt",
        
        # np.savetxt(str(results_directory) + "/" + "HjDE_pareto_position" + str(i) + ".txt",
        


    # if output_avg == True:
    
    #     # np.savetxt(str(results_directory) + "/" + "HGS_pareto_fitness_Mean.txt", count_fitness_hgs)
    
    #     np.savetxt(str(results_directory) + "/" + "IHGS_pareto_fitness_Mean.txt", count_fitness_ihgs)
    
    #     # np.savetxt(str(results_directory) + "/" + "PSO_pareto_fitness_Mean.txt", count_fitness_pso)
    
    #     # np.savetxt(str(results_directory) + "/" + "PPSO_pareto_fitness_Mean.txt", count_fitness_ppso)
    
    #     # np.savetxt(str(results_directory) + "/" + "DE_pareto_fitness_Mean.txt", count_fitness_de)
    
    #     # np.savetxt(str(results_directory) + "/" + "iMoDE_pareto_fitness_Mean.txt", count_fitness_imode)

    # IHGS
    # count_fitness_ihgs = [0] * NumOfRuns
    # for i in range(NumOfRuns):
    
    
    #     count_fitness_ihgs[i] = moihgs_pareto_fitness
    


    # DEHGS
    # count_fitness_dehgs = [0] * NumOfRuns
    # for i in range(NumOfRuns):
    
    
    #     count_fitness_dehgs[i] = modehgs_pareto_fitness
    

    # PSO
    
    

    # DE
    
    

    # iMoDE
    
    


    # # PPSO
    # count_fitness_ppso = [0] * NumOfRuns
    # for i in range(NumOfRuns):
    
    
    #     count_fitness_ppso[i] = moppso_pareto_fitness
    


    # DECEHGS
    # count_fitness_decehgs = [0] * NumOfRuns
    # for i in range(NumOfRuns):
    
    
    #     count_fitness_decehgs[i] = modecehgs_pareto_fitness
    


    # fig = plt.figure()
    # ax3 = fig.add_subplot()#133
    # ax3.set_xlabel('Emission(lb)')
    # ax3.set_ylabel('Cost($)')
    # ax3.scatter(count_fitness_hgs[:, 1], count_fitness_hgs[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(count_fitness_ihgs[:, 1], count_fitness_ihgs[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(count_fitness_dehgs[:, 1], count_fitness_dehgs[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(mopso_pareto_fitness[:, 1], mopso_pareto_fitness[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(count_fitness_ppso[:, 1], count_fitness_ppso[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(mode_pareto_fitness[:, 1], mode_pareto_fitness[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(moimode_pareto_fitness[:, 1], moimode_pareto_fitness[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)
    # ax3.scatter(count_fitness_decehgs[:, 1], count_fitness_decehgs[:, 0], s=50, c='', edgecolors='#1c8c44', marker="*",
    #             alpha=1.0)

    # plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
    # plt.grid()
    # fig_name = "DEED_IHGS" + ".svg"
    # plt.savefig(fig_name, bbox_inches="tight", format='svg')
    # plt.clf()
    # plt.close()


 
if __name__ == "__main__":
    main()
