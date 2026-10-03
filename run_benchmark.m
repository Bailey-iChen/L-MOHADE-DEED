function result = run_benchmark(platemoRoot, problemName, N, maxFE, seed, runs, outputDir)
    if nargin < 2, problemName = 'ZDT1'; end
    if nargin < 3, N = 100; end
    if nargin < 4, maxFE = []; end
    if nargin < 5, seed = 1; end
    if nargin < 6, runs = 1; end
    if nargin < 7, outputDir = fullfile(pwd, 'results'); end
    allowed = {'ZDT1', 'ZDT2', 'ZDT3', 'ZDT4', 'ZDT6', 'DTLZ1', 'DTLZ2', 'DTLZ3', 'DTLZ4', 'DTLZ5', 'DTLZ6', 'DTLZ7'};
    problemName = char(problemName);
    assert(ismember(problemName, allowed));
    validateattributes(N, {'numeric'}, {'scalar', 'integer', '>=', 2});
    validateattributes(seed, {'numeric'}, {'scalar', 'integer', 'nonnegative'});
    validateattributes(runs, {'numeric'}, {'scalar', 'integer', 'positive'});
    if startsWith(problemName, 'ZDT')
        M = 2;
        if isempty(maxFE), maxFE = 60000; end
    else
        M = 3;
        if isempty(maxFE), maxFE = 178500; end
    end
    validateattributes(maxFE, {'numeric'}, {'scalar', 'integer', '>=', N});
    assert(isfile(fullfile(platemoRoot, 'platemo.m')));
    oldPath = path;
    cleanup = onCleanup(@() path(oldPath));
    addpath(genpath(platemoRoot));
    addpath(fileparts(mfilename('fullpath')), '-begin');
    if ~isfolder(outputDir), mkdir(outputDir); end
    result = cell(runs, 1);
    for r = 1:runs
        runSeed = seed + r - 1;
        file = fullfile(outputDir, sprintf('%s_seed%d.mat', problemName, runSeed));
        assert(~isfile(file), 'Output already exists');
        rng(runSeed, 'twister');
        problem = feval(problemName, 'N', N, 'M', M, 'maxFE', maxFE);
        algorithm = LMOHADE('save', 1, 'outputFcn', @(~, ~) []);
        algorithm.Solve(problem);
        final = algorithm.result{end, 2};
        decisions = final.decs;
        objectives = final.objs;
        evaluations = problem.FE;
        igd = problem.CalMetric('IGD', final);
        save(file, 'decisions', 'objectives', 'evaluations', 'igd', 'runSeed');
        result{r} = struct('file', file, 'evaluations', evaluations, 'igd', igd);
    end
end
