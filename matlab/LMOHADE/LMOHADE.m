classdef LMOHADE < ALGORITHM
    methods
        function main(Algorithm, Problem)
            [a, lg, L, c, capacity, staticGate, useRank] = Algorithm.ParameterSet(0.001, 10000, 0.08, 0.1, Problem.N, NaN, false);
            assert(Problem.maxFE >= Problem.N && Problem.N >= 2);
            assert(a >= 0 && lg >= 0 && L >= 0 && L <= 1 && c >= 0 && c <= 1 && capacity >= 1);
            assert(isnan(staticGate) || (staticGate >= 0 && staticGate <= 1));
            Population = Problem.Initialization();
            N = length(Population);
            Pbest = Population;
            Archive = Population([]);
            Report = trim_archive(Population, capacity);
            hunger = zeros(N, 1);
            muF = 0.5;
            muCR = 0.5;
            generation = 0;
            generations = max(1, ceil((Problem.maxFE - Problem.FE) / N));
            while Algorithm.NotTerminated(Report)
                generation = generation + 1;
                progress = generation / generations;
                n = min(N, Problem.maxFE - Problem.FE);
                x = Population.decs;
                y = Population.objs;
                if useRank
                    signal = ranking_feedback(y);
                else
                    score = mean(y, 2);
                    signal = (score - min(score)) / max(max(score) - min(score), eps);
                end
                tg = signal .* rand(N, 1) * mean(Problem.upper - Problem.lower);
                increment = tg;
                small = tg < lg;
                r6 = rand(N, 1);
                increment(small) = floor(lg * (1 + r6(small)));
                hunger = hunger + increment;
                hunger(signal == 0) = 0;
                F = muF + 0.1 * tan(pi * (rand(n, 1) - 0.5));
                while any(F <= 0)
                    bad = F <= 0;
                    F(bad) = muF + 0.1 * tan(pi * (rand(sum(bad), 1) - 0.5));
                end
                F = min(F, 1);
                CR = max(0, min(1, muCR + 0.1 * randn(n, 1)));
                leaders = trim_archive([Archive, Population], capacity);
                ly = leaders.objs;
                span = max(ly, [], 1) - min(ly, [], 1);
                satisfaction = (max(ly, [], 1) - ly) ./ max(span, eps);
                satisfaction(:, span == 0) = 1;
                [~, best] = max(sum(satisfaction, 2));
                gbest = repmat(leaders(best).dec, n, 1);
                pool = [Population, Archive];
                reference = pool(randi(length(pool), n, 1)).decs;
                total = sum(hunger);
                r4 = rand(n, 1);
                alpha = ones(n, 1);
                if total > 0
                    ids = r4 <= L;
                    alpha(ids) = hunger(ids) / total * N .* r4(ids);
                end
                beta = (1 - exp(-abs(hunger(1:n) - total))) .* (2 * rand(n, 1));
                R = (4 * rand(n, 1) - 2) * (1 - progress);
                if progress < 0.4
                    target = Pbest(1:n).decs;
                else
                    target = gbest;
                end
                mutant = alpha .* reference + R .* beta .* abs(target - x(1:n, :));
                probability = 0.55 - 0.3 * atan(15 * (progress - 0.8));
                if ~isnan(staticGate)
                    probability = staticGate;
                end
                exploratory = x(1:n, :) .* (1 + a * randn(n, Problem.D));
                modes = rand(n, 1) < probability;
                mutant(modes, :) = exploratory(modes, :);
                mask = rand(n, Problem.D) <= CR;
                forced = sub2ind([n, Problem.D], (1:n)', randi(Problem.D, n, 1));
                mask(forced) = true;
                trial = x(1:n, :);
                trial(mask) = mutant(mask);
                trial = max(Problem.lower, min(Problem.upper, trial));
                Offspring = Problem.Evaluation(trial);
                accepted = select_pairs(y(1:n, :), Offspring.objs);
                ids = find(accepted);
                Population(ids) = Offspring(ids);
                improved = select_pairs(Pbest.objs, Population.objs);
                Pbest(improved) = Population(improved);
                Archive = trim_archive([Archive, Population], capacity);
                Report = Archive;
                if any(accepted)
                    muF = (1 - c) * muF + c * sum(F(accepted).^2) / sum(F(accepted));
                    muCR = (1 - c) * muCR + c * mean(CR(accepted));
                end
            end
        end
    end
end

function keep = nondominated(y)
    keep = true(size(y, 1), 1);
    for i = 1:size(y, 1)
        keep(i) = ~any(all(y <= y(i, :), 2) & any(y < y(i, :), 2));
    end
end

function distance = crowding(y)
    [values, ~, inverse] = unique(y, 'rows');
    count = size(values, 1);
    d = zeros(count, 1);
    for j = 1:size(values, 2)
        [v, order] = sort(values(:, j));
        span = v(end) - v(1);
        if span > 0
            d(order([1, end])) = inf;
            d(order(2:end-1)) = d(order(2:end-1)) + (v(3:end) - v(1:end-2)) / span;
        end
    end
    if count <= 2
        d(:) = inf;
    end
    distance = d(inverse);
end

function accepted = select_pairs(parent, trial)
    better = all(trial <= parent, 2) & any(trial < parent, 2);
    worse = all(parent <= trial, 2) & any(parent < trial, 2);
    equal = all(parent == trial, 2);
    d = crowding([parent; trial]);
    n = size(parent, 1);
    accepted = better | (~worse & ~equal & d(n+1:end) > d(1:n));
end

function Population = trim_archive(Population, capacity)
    [~, ids] = unique(Population.objs, 'rows');
    Population = Population(ids);
    Population = Population(nondominated(Population.objs));
    while length(Population) > capacity
        [~, victim] = min(crowding(Population.objs));
        Population(victim) = [];
    end
end

function signal = ranking_feedback(y)
    remaining = (1:size(y, 1))';
    ranks = zeros(size(remaining));
    position = 0;
    while ~isempty(remaining)
        front = nondominated(y(remaining, :));
        ids = remaining(front);
        d = crowding(y(ids, :));
        [v, order] = sort(d, 'descend');
        k = 1;
        while k <= length(ids)
            last = k;
            while last < length(ids) && v(last+1) == v(k)
                last = last + 1;
            end
            ranks(ids(order(k:last))) = position + (k + last) / 2;
            k = last + 1;
        end
        position = position + length(ids);
        remaining = remaining(~front);
    end
    signal = (ranks - min(ranks)) / max(max(ranks) - min(ranks), eps);
end
