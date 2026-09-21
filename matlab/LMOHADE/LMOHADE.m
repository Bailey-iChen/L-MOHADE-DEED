classdef LMOHADE < ALGORITHM
% <multi> <real/integer>




    methods
        function main(Algorithm,Problem)
            %% Generate the weight vectors
            [W,Problem.N] = UniformPoint(Problem.N,Problem.M);
            W = W./repmat(sqrt(sum(W.^2,2)),1,size(W,2));
            %% Generate random population
            Population = Problem.Initialization();
            Fitness    = CalFitness(Population.objs);
            Z          = min(Population.objs,[],1);
            Population = Classification(Problem,Population,W,Z);
            Archive    = UpdateArchive(Population,Problem.N);

            hungry = zeros(Problem.N,1);
            sumHungry = 0;

            %% Optimization
            while Algorithm.NotTerminated(Archive)
                [Pbest,Gbest] = GetBest(Archive,W,Z);
                % MatingPool = TournamentSelection(2,Problem.N,Fitness);
                [Offspring, sumHungry, hungry] = OperatorLMOHADE(Problem,Population,Pbest,Gbest,sumHungry,hungry, Archive);
                [Population, Fitness] = EnvironmentalSelection_V2([Population,Offspring],Problem.N);
                
                Z             = min([Z;Population.objs],[],1);
                Archive       = UpdateArchive([Archive,Population],Problem.N);
                S             = OperatorGAhalf(Problem,Archive([1:length(Archive),randi(ceil(length(Archive)/2),1,length(Archive))]));
                Z             = min([Z;S.objs],[],1);
                Archive       = UpdateArchive([Archive,S],Problem.N);

            end
        end
    end
end