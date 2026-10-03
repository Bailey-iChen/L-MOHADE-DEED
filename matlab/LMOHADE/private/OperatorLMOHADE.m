function [Offspring,sumHungry,hungry] = OperatorLMOHADE(Problem,Particle,Pbest,Gbest,sumHungry,hungry,Archive)
    %% Parameter setting
    ParticleDec = Particle.decs;
    PbestDec    = Pbest.decs;
    GbestDec    = Gbest.decs;
    [N,D]       = size(ParticleDec);
    Lower  = repmat(Problem.lower,N,1);
    Upper  = repmat(Problem.upper,N,1);
    
    %% Calculate HGS Parameter
    Worstest_fitness = max(Particle.objs);
    for i = 1:N
         l = Gbest(i).objs;
         m = Particle(i).objs;
         nnn = (exp(sum(Particle(i).objs-Gbest(i).objs)) + exp(sum(Gbest(i).objs-Particle(i).objs)));
         %calculate the variation control of all positions
         E(i) = 2/(exp(sum(Particle(i).objs-Gbest(i).objs)) + exp(sum(Gbest(i).objs-Particle(i).objs)));
         %calculate the hungry of each position
        if Gbest(i).objs == Particle(i).objs
            hungry(i) = 0;
        else
            temprand = rand();
            c = (Particle(i).objs-Gbest(i).objs)/(Worstest_fitness-Gbest(i).objs)*temprand*2*(Upper-Lower);
            if c<100
                b=100*(1+temprand);
            else
                b=c;
            end   
            hungry(i) = hungry(i)+ max(b); 
            sumHungry = sumHungry + hungry(i);
        end
    end 
    %% Multi Objective Hunger Games Search Algorithm
    OffDec = ParticleDec;
    for i = 1:N
        shrink=2*(1-Problem.FE/Problem.maxFE);
        R = 2*rand()*shrink-shrink;
        L = 1 - (0.55 + 1 / pi * atan((1 - Problem.FE/Problem.maxFE - 0.8) / 0.3));
        if rand() < L % 0.03
            W1 = hungry(i)*N/sumHungry*rand;
        else
            W1 = 1;
        end
        W2 = (1-exp(-abs(hungry(i)-sumHungry)))*rand()*2;
        if rand() > L
            OffDec(i,:) = ParticleDec(i) * (1+randn(1));
        else
%             if Problem.FE < 0.4*Problem.maxFE
            if rand() > 0.7
%                 OffDec(i,:) = W1*Archive(randi(length(Archive))).decs + R*W2*abs(PbestDec(i,:)-OffDec(i,:));
                OffDec(i,:) = W1*PbestDec(i,:) + R*W2*abs(Archive(randi(length(Archive))).decs-OffDec(i,:));
            else
                OffDec(i,:) = W1*GbestDec(i,:) + R*W2*abs(GbestDec(i,:)-OffDec(i,:));
            end
        end
    end
        %% Deterministic back
    Lower  = repmat(Problem.lower,N,1);
    Upper  = repmat(Problem.upper,N,1);
    OffDec = max(min(OffDec,Upper),Lower);
    
        %% Polynomial mutation
    if Problem.FE <= Problem.maxFE*0.5
        disM = 20;
        Site = rand(N,D) < 1/D;
        mu   = rand(N,D);
        temp = Site & mu<=0.5;
        OffDec(temp) = OffDec(temp)+(Upper(temp)-Lower(temp)).*((2.*mu(temp)+(1-2.*mu(temp)).*...
                       (1-(OffDec(temp)-Lower(temp))./(Upper(temp)-Lower(temp))).^(disM+1)).^(1/(disM+1))-1);
        temp  = Site & mu>0.5; 
        OffDec(temp) = OffDec(temp)+(Upper(temp)-Lower(temp)).*(1-(2.*(1-mu(temp))+2.*(mu(temp)-0.5).*...
                       (1-(Upper(temp)-OffDec(temp))./(Upper(temp)-Lower(temp))).^(disM+1)).^(1/(disM+1)));
    end
    Offspring = Problem.Evaluation(OffDec);
end

