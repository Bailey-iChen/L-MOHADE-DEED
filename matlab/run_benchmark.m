function run_benchmark(platemoRoot,problemName,N,maxFE,seed)
% Run one explicitly selected benchmark with the author-designated method.
% No default experimental parameters; this function was not executed during packaging.
    narginchk(5,5);
    validateattributes(N,{'numeric'},{'scalar','integer','positive'});
    validateattributes(maxFE,{'numeric'},{'scalar','integer','positive'});
    validateattributes(seed,{'numeric'},{'scalar','integer','nonnegative','<=',2^32-1});
    allowed = {'ZDT1','ZDT2','ZDT3','ZDT4','ZDT6','DTLZ1','DTLZ2','DTLZ3','DTLZ4','DTLZ5','DTLZ6','DTLZ7'};
    problemName = char(problemName);
    assert(ismember(problemName,allowed),'Choose one of the twelve manuscript benchmarks.');
    assert(isfolder(platemoRoot),'PlatEMO directory does not exist.');
    oldPath = path; oldDir = pwd;
    clean = onCleanup(@() restore_session(oldPath,oldDir)); %#ok<NASGU>
    cd(platemoRoot); platemoRoot = pwd;
    assert(isfile(fullfile(platemoRoot,'platemo.m')),'platemo.m not found.');
    addpath(genpath(platemoRoot));
    methodDir = fullfile(fileparts(mfilename('fullpath')),'LMOHADE');
    addpath(methodDir,'-begin');
    rng(seed,'twister');
    platemo('algorithm',@LMOHADE,'problem',str2func(problemName), ...
            'N',N,'maxFE',maxFE,'save',1);
end

function restore_session(oldPath,oldDir)
    path(oldPath);
    cd(oldDir);
end
