import numpy as np
from public import constants_15unit as deed
import math
from public import zdt
from public import uf


def P_objective(Operation,Problem,M,Input):
    [Output, Boundary, Coding] = P_DEED(Operation, Problem, M, Input)
    if Boundary == []:
        return Output
    else:
        return Output, Boundary, Coding

def P_DTLZ(Operation,Problem,M,Input):
    Boundary = []
    Coding = ""
    k = 1
    K = [5, 10, 10, 10, 10, 10, 20]
    K_select = K[k - 1]
    if Operation == "init":
        D = M + K_select - 1
        MaxValue = np.ones((1, D))
        MinValue = np.zeros((1, D))
        Population = np.random.random((Input, D))
        Population = np.multiply(Population, np.tile(MaxValue, (Input, 1))) +\
            np.multiply((1-Population), np.tile(MinValue, (Input, 1)))
        Boundary = np.vstack((MaxValue, MinValue))
        Coding = "Real"
        return Population, Boundary, Coding
    elif Operation == "value":
        Population = Input
        FunctionValue = np.zeros((Population.shape[0], M))
        if Problem == "DTLZ1":
            # g = 100*(K_select+np.sum( (Population[:, M-1:] - 0.5)**2 - np.cos(20*np.pi*(Population[:, M-1:] - 0.5)), axis=1, keepdims = True))
            g = 100*(K_select+np.sum( (Population[:, M-1:] - 0.5)**2 - np.cos(20*np.pi*(Population[:, M-1:] - 0.5)), axis=1))
            for i in range(M):
                FunctionValue[:, i] = 0.5*np.multiply( np.prod(Population[:, :M-i-1], axis=1), (1+g))
                if i>0:
                    FunctionValue[:, i] = np.multiply(FunctionValue[:, i], 1-Population[:, M-i-1])
        elif Problem == "DTLZ2":
            g = np.sum( (Population[:, M-1:] - 0.5)**2,axis=1)
            for i in range(M):
                FunctionValue[:, i] = (1+g)*np.prod( np.cos( 0.5*np.pi*(Population[:, :M-i-1]) ),axis=1 )
                if i>0:
                    FunctionValue[:, i] = np.multiply(FunctionValue[:, i], np.sin( 0.5*np.pi* ( Population[:, M-i-1]) ) )
        # elif Problem == "ZDT3":
        #     g = 1 + 9 * np.sum(Population[:, M-1]) /


        return FunctionValue, Boundary, Coding

def P_ZDT(Operation,Problem,M,Input):
    Boundary = []
    Coding = ""
    if Operation == "init":
        D = 30
        MaxValue = np.ones((1, D))
        MinValue = np.zeros((1, D))
        Population = np.random.random((Input, D))
        Population = np.multiply(Population, np.tile(MaxValue, (Input, 1))) +\
            np.multiply((1-Population), np.tile(MinValue, (Input, 1)))
        Boundary = np.vstack((MaxValue, MinValue))
        Coding = "Real"
        return Population, Boundary, Coding
    elif Operation == "value":
        Population = Input
        FunctionValue = np.zeros((Population.shape[0], M))
        if Problem == "ZDT1":
            FunctionValue = zdt.cal_obj_func_zdt1(Input)
        elif Problem == "ZDT2":
            FunctionValue = zdt.cal_obj_func_zdt2(Input)
        elif Problem == "ZDT3":
            FunctionValue = zdt.cal_obj_func_zdt3(Input)
        elif Problem == "ZDT4":
            FunctionValue = zdt.cal_obj_func_zdt4(Input)

        return FunctionValue, Boundary, Coding



NO_OF_HOURS = 24
NO_OF_GENERATORS = deed.NO_OF_GENERATORS
SLACK_GENERATOR_INDEX = deed.SLACK_GENERATOR_INDEX
EMISSION_SCALING_FACTOR = 10
def P_DEED(Operation,Problem,M,Input):
    Boundary = []
    Coding = ""

    if Operation == "value":
        Population = Input
        FunctionValue = np.zeros((Population.shape[0], M))
        if Problem == "DEED":
            for i in range(Population.shape[0]):
                generators_power = np.copy(Input[i])
                costs = compute_cost_function(generators_power)
                emissions = compute_emission_function(generators_power)
                violations = compute_violation_function(generators_power)
                FunctionValue[i, 0] = costs
                FunctionValue[i, 1] = emissions
        return FunctionValue, Boundary, Coding

    elif Operation == "init":
        D = NO_OF_HOURS * NO_OF_GENERATORS
        # MaxValue = 600 * np.ones([1, D])
        # MinValue = 100 * np.ones([1, D])
        MaxValue = deed.GENERATORS_MAX_POWER
        MinValue = deed.GENERATORS_MIN_POWER
        # Population = np.random.uniform(100, 600, (Input, D))
        # Population = np.multiply(Population, np.tile(MaxValue, (Input, 1))) + \
        #              np.multiply((1 - Population), np.tile(MinValue, (Input, 1)))
        Population = np.zeros((Input, D))
        for i in range(Input):
            X_i_reshape = np.reshape(Population[i, :], (24, deed.NO_OF_GENERATORS))
            for h_i in range(24):
                for g_i in range(deed.NO_OF_GENERATORS):
                    X_i_reshape[h_i, g_i] = MinValue[g_i] + (MaxValue[g_i] - MinValue[g_i]) * np.random.rand()
            X_i_reshape = np.reshape(X_i_reshape, 24 * deed.NO_OF_GENERATORS)
            Population[i, :] = X_i_reshape.copy()
        Boundary = np.vstack((MaxValue, MinValue))
        Coding = "Real"

        return Population, Boundary, Coding



def compute_cost_function(generators_power):
    cost = 0
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))
    for h_i in range(NO_OF_HOURS):
        for g_i in range(NO_OF_GENERATORS):
            generator_power = generators_power_reshaped[h_i][g_i]
            sin = math.sin( deed.E_N[g_i] * (deed.GENERATORS_MIN_POWER[g_i] - generator_power) )
            cost += deed.A_N[g_i] +\
                    deed.B_N[g_i] * generator_power +\
                    deed.C_N[g_i] * np.power(generator_power, 2) +\
                    np.absolute(deed.D_N[g_i] * sin)
    return cost

def compute_emission_function(generators_power):
    emission = 0
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))
    for h_i in range(NO_OF_HOURS):
        for g_i in range(NO_OF_GENERATORS):
            generator_power = generators_power_reshaped[h_i][g_i]
            emission += deed.ALPHA_N[g_i] +\
                        deed.BETA_N[g_i] * generator_power +\
                        deed.GAMMA_N[g_i] * np.power(generator_power, 2) +\
                        deed.ETA_N[g_i] * np.exp(deed.DELTA_N[g_i] * generator_power)
    return emission


def compute_violation_function(generators_power):
    operation_violations = compute_operation_violations(generators_power)
    ramp_violations = compute_ramp_violations(generators_power)

    return ramp_violations + operation_violations

def compute_operation_violations(generators_power):
    violation = 0
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))
    for h_i in range(NO_OF_HOURS):
        slack_power = generators_power_reshaped[h_i][SLACK_GENERATOR_INDEX]
        if (slack_power > deed.GENERATORS_MAX_POWER[SLACK_GENERATOR_INDEX]):
            violation += np.absolute(slack_power - deed.GENERATORS_MAX_POWER[SLACK_GENERATOR_INDEX] + 1)
        elif (slack_power < deed.GENERATORS_MIN_POWER[SLACK_GENERATOR_INDEX]):
            violation += np.absolute(deed.GENERATORS_MIN_POWER[SLACK_GENERATOR_INDEX] - slack_power + 1)
    return violation

def compute_ramp_violations(generators_power):
    violation = 0
    generators_power_reshaped = np.reshape(generators_power, (NO_OF_HOURS, NO_OF_GENERATORS))
    for h_i in range(1, NO_OF_HOURS):
        for g_i in range(NO_OF_GENERATORS):
            current_power = generators_power_reshaped[h_i][g_i]
            previous_power = generators_power_reshaped[h_i-1][g_i]
            diff_power = current_power - previous_power
            if (diff_power > deed.GENERATORS_UP_RAMP[g_i]):
                violation += np.absolute(diff_power - deed.GENERATORS_UP_RAMP[g_i] + 1)
            elif (diff_power < (-1 * deed.GENERATORS_DOWN_RAMP[g_i])):
                violation += np.absolute(diff_power + deed.GENERATORS_DOWN_RAMP[g_i] + 1)
    return violation








