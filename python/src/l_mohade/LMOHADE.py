import numpy as np
from public import P_objective

def nondominated(y):
    y = np.asarray(y, dtype=float)
    return ~np.any(np.all(y[:, None] <= y[None, :], axis=2) & np.any(y[:, None] < y[None, :], axis=2), axis=0)

def crowding(y):
    values, inverse = np.unique(y, axis=0, return_inverse=True)
    distance = np.zeros(len(values))
    for j in range(values.shape[1]):
        order = np.argsort(values[:, j], kind='stable')
        span = np.ptp(values[:, j])
        if span > 0:
            distance[order[[0, -1]]] = np.inf
            distance[order[1:-1]] += (values[order[2:], j] - values[order[:-2], j]) / span
    if len(values) <= 2:
        distance[:] = np.inf
    return distance[inverse]

def ranking_feedback(y):
    remaining = np.arange(len(y))
    ranks = np.empty(len(y))
    position = 0
    while len(remaining):
        front = nondominated(y[remaining])
        ids = remaining[front]
        distance = crowding(y[ids])
        order = np.argsort(-distance, kind='stable')
        k = 0
        while k < len(ids):
            end = k + 1
            while end < len(ids) and distance[order[end]] == distance[order[k]]:
                end += 1
            ranks[ids[order[k:end]]] = position + (k + end - 1) / 2
            k = end
        position += len(ids)
        remaining = remaining[~front]
    span = np.ptp(ranks)
    return (ranks - ranks.min()) / span if span > 0 else np.zeros(len(y))

def select_pairs(parent, trial):
    better = np.all(trial <= parent, axis=1) & np.any(trial < parent, axis=1)
    worse = np.all(parent <= trial, axis=1) & np.any(parent < trial, axis=1)
    equal = np.all(parent == trial, axis=1)
    distance = crowding(np.vstack((parent, trial)))
    return better | ~worse & ~equal & (distance[len(parent):] > distance[:len(parent)])

def update_archive(ax, ay, x, y, capacity):
    x, y = (np.vstack((ax, x)), np.vstack((ay, y)))
    _, ids = np.unique(y, axis=0, return_index=True)
    ids = ids[nondominated(y[ids])]
    x, y = (x[ids], y[ids])
    while len(y) > capacity:
        victim = np.argmin(crowding(y))
        x, y = (np.delete(x, victim, axis=0), np.delete(y, victim, axis=0))
    return (x.copy(), y.copy())

def compromise(y):
    span = np.ptp(y, axis=0)
    satisfaction = np.divide(y.max(axis=0) - y, span, out=np.ones_like(y), where=span > 0)
    total = satisfaction.sum(axis=1)
    return int(np.argmax(total))

class DEED:

    def __init__(self, maximum, minimum):
        deed = P_objective.deed
        self.units, self.hours = (deed.NO_OF_GENERATORS, deed.NO_OF_HOURS)
        names = {'pmin': 'GENERATORS_MIN_POWER', 'pmax': 'GENERATORS_MAX_POWER', 'up': 'GENERATORS_UP_RAMP', 'down': 'GENERATORS_DOWN_RAMP', 'cost_a': 'A_N', 'cost_b': 'B_N', 'cost_c': 'C_N', 'cost_d': 'D_N', 'cost_e': 'E_N', 'emission_a': 'ALPHA_N', 'emission_b': 'BETA_N', 'emission_c': 'GAMMA_N', 'emission_d': 'ETA_N', 'emission_e': 'DELTA_N'}
        self.c = {key: np.asarray(getattr(deed, name), dtype=float) for key, name in names.items()}
        self.demand = np.asarray(deed.POWER_DEMAND, dtype=float)
        self.b = np.asarray(deed.B_MATRIX, dtype=float)
        self.b0 = np.asarray(getattr(deed, 'B_LINEAR', np.zeros(self.units)), dtype=float)
        self.b00 = float(getattr(deed, 'B_CONSTANT', 0.0))
        self.initial = getattr(deed, 'INITIAL_OUTPUTS', None)
        self.zones = {int(k) - 1: np.asarray(v, dtype=float) for k, v in getattr(deed, 'PROHIBITED_ZONES', {}).items()}
        self.intervals = {u: np.column_stack((np.r_[self.c['pmin'][u], z[:, 1]], np.r_[z[:, 0], self.c['pmax'][u]])) for u, z in self.zones.items()}
        self.lower = np.tile(self.c['pmin'], self.hours)
        self.upper = np.tile(self.c['pmax'], self.hours)
        for values, expected in [(minimum, self.lower), (maximum, self.upper)]:
            values = np.asarray(values, dtype=float).ravel()
            if values.size == self.units:
                values = np.tile(values, self.hours)
            if values.shape != expected.shape or not np.array_equal(values, expected):
                raise ValueError('Bounds must match the selected DEED data')
        symmetric = self.b + self.b.T
        derivative = 1 - np.maximum(symmetric, 0) @ self.c['pmax'] - np.minimum(symmetric, 0) @ self.c['pmin'] - self.b0
        if np.any(derivative <= 0):
            raise ValueError('Net generation must increase within the bounds')
        if np.any(self.net(self.c['pmax'][None, :])[0] < self.demand):
            raise ValueError('Demand exceeds maximum net generation')

    def schedules(self, x):
        x = np.asarray(x, dtype=float)
        if x.size == 0 or x.size % len(self.lower) or (not np.isfinite(x).all()):
            raise ValueError('Expected finite nonempty schedules')
        return x.reshape(-1, self.hours, self.units)

    def net(self, p):
        return p.sum(axis=-1) - np.einsum('...i,ij,...j->...', p, self.b, p) - p @ self.b0 - self.b00

    def objectives(self, x):
        schedules = self.schedules(x).reshape(-1, len(self.lower))
        return P_objective.P_objective('value', 'DEED', 2, schedules)

    def validate(self, x):
        p, c = (self.schedules(x), self.c)
        capacity = np.maximum(0, np.maximum(c['pmin'] - p, p - c['pmax']).max(axis=(1, 2)))
        previous = p if self.initial is None else np.concatenate((np.broadcast_to(self.initial, (len(p), 1, self.units)), p), axis=1)
        delta = np.diff(previous, axis=1)
        ramp = np.maximum(0, np.maximum(delta - c['up'], -delta - c['down']).max(axis=(1, 2)))
        balance = np.abs(self.net(p) - self.demand).max(axis=1)
        zones = np.zeros(len(p))
        for unit, intervals in self.zones.items():
            for low, high in intervals:
                zones = np.maximum(zones, np.maximum(0, np.minimum(p[:, :, unit] - low, high - p[:, :, unit])).max(axis=1))
        return {'capacity': capacity, 'ramp': ramp, 'balance': balance, 'zones': zones, 'feasible': (capacity <= 1e-06) & (ramp <= 1e-06) & (balance <= 0.0001) & (zones <= 1e-06)}

    def project_hour(self, desired, lower, upper, demand):
        desired = np.clip(desired, lower, upper)
        low, high = (np.full(len(desired), -1.0), np.full(len(desired), 1.0))
        span = upper - lower
        for _ in range(42):
            mid = (low + high) / 2
            p = np.clip(desired + mid[:, None] * span, lower, upper)
            below = self.net(p) < demand
            low, high = (np.where(below, mid, low), np.where(below, high, mid))
        return p

    def repair(self, x):
        p, c = (self.schedules(x).copy(), self.c)
        valid = np.ones(len(p), dtype=bool)
        for hour, demand in enumerate(self.demand):
            lower = np.broadcast_to(c['pmin'], (len(p), self.units)).copy()
            upper = np.broadcast_to(c['pmax'], lower.shape).copy()
            previous = p[:, hour - 1] if hour else self.initial
            if previous is not None:
                lower = np.maximum(lower, previous - c['down'])
                upper = np.minimum(upper, previous + c['up'])
            desired = self.project_hour(p[:, hour], lower, upper, demand)
            for unit, intervals in self.intervals.items():
                low = np.maximum(lower[:, unit, None], intervals[None, :, 0])
                high = np.minimum(upper[:, unit, None], intervals[None, :, 1])
                possible = low <= high
                valid &= possible.any(axis=1)
                nearest = np.clip(desired[:, unit, None], low, high)
                distances = np.where(possible, np.abs(nearest - desired[:, unit, None]), np.inf)
                chosen, rows = (np.argmin(distances, axis=1), np.arange(len(p)))
                lower[:, unit], upper[:, unit] = (low[rows, chosen], high[rows, chosen])
            valid &= (lower <= upper).all(axis=1) & (self.net(lower) <= demand + 1e-08) & (self.net(upper) >= demand - 1e-08)
            p[:, hour] = self.project_hour(desired, lower, upper, demand) if self.zones else desired
        flat = p.reshape(len(p), -1)
        return (flat, valid & self.validate(flat)['feasible'])

def gate(progress):
    return 0.55 - 0.3 * np.arctan(15 * (progress - 0.8))

def sample_parameters(rng, n, mu_f, mu_cr):
    f = mu_f + 0.1 * rng.standard_cauchy(n)
    while np.any(f <= 0):
        bad = f <= 0
        f[bad] = mu_f + 0.1 * rng.standard_cauchy(bad.sum())
    return (np.minimum(f, 1), np.clip(rng.normal(mu_cr, 0.1, n), 0, 1))

def mutate(x, pbest, gbest, reference, hunger, progress, probability, rng, a, weight_gate):
    n = len(x)
    total = hunger.sum()
    r4 = rng.random(n)
    alpha = np.ones(n)
    if total > 0:
        alpha = np.where(r4 <= weight_gate, hunger[:n] / total * len(hunger) * r4, 1.0)
    beta = -np.expm1(-np.abs(hunger[:n] - total)) * rng.uniform(0, 2, n)
    r = rng.uniform(-2, 2, n) * (1 - progress)
    target = pbest if progress < 0.4 else gbest
    cooperative = alpha[:, None] * reference + (r * beta)[:, None] * np.abs(target - x)
    exploratory = x * (1 + rng.normal(0, a, x.shape))
    return np.where((rng.random(n) < probability)[:, None], exploratory, cooperative)

def crossover(x, mutant, cr, rng):
    mask = rng.random(x.shape) <= cr[:, None]
    mask[np.arange(len(x)), rng.integers(x.shape[1], size=len(x))] = True
    return np.where(mask, mutant, x)

def optimize(model, seed=1, population=100, evaluations=100100, capacity=100, a=0.001, lg=10000.0, weight=0.5, scale=1.0, feedback='weighted', static_gate=None, weight_gate=0.08, adaptation=0.1, no_hunger=False, no_archive=False, no_adaptation=False, checkpoint=10000):
    if population < 2 or capacity < 1 or evaluations < population or (checkpoint < 1):
        raise ValueError('Invalid population, capacity, evaluation budget or checkpoint interval')
    if not 0 <= weight <= 1 or scale <= 0 or a < 0 or (lg < 0):
        raise ValueError('Invalid feedback or hunger parameters')
    if not 0 <= weight_gate <= 1 or not 0 <= adaptation <= 1:
        raise ValueError('Invalid weight gate or adaptation rate')
    if static_gate is not None and (not 0 <= static_gate <= 1):
        raise ValueError('Static gate must be in [0, 1]')
    rng = np.random.default_rng(seed)
    x = rng.uniform(model.lower, model.upper, (population, len(model.lower)))
    x, valid = model.repair(x)
    attempts = 0
    while not valid.all() and attempts < 100:
        ids = np.flatnonzero(~valid)
        x[ids], valid[ids] = model.repair(rng.uniform(model.lower, model.upper, (len(ids), x.shape[1])))
        attempts += 1
    if not valid.all():
        raise RuntimeError('Could not initialize a feasible population')
    y = model.objectives(x)
    pbest, pbest_y = (x.copy(), y.copy())
    ax, ay = (np.empty((0, x.shape[1])), np.empty((0, y.shape[1])))
    hunger = np.zeros(population)
    mu_f, mu_cr = (0.5, 0.5)
    fes, generation, rejected = (population, 0, 0)
    generations = max(1, int(np.ceil((evaluations - population) / population)))
    trace = []
    checkpoints = {}
    next_checkpoint = fes
    while True:
        if fes >= next_checkpoint or fes == evaluations:
            sx, sy = update_archive(ax, ay, x, y, capacity)
            checkpoints[f'archive_x_{fes}'] = sx
            checkpoints[f'archive_y_{fes}'] = sy
            trace.append([fes, generation, gate(generation / generations) if static_gate is None else static_gate, mu_f, mu_cr, len(sy), rejected])
            next_checkpoint = (fes // checkpoint + 1) * checkpoint
        if fes == evaluations:
            break
        generation += 1
        progress = generation / generations
        n = min(population, evaluations - fes)
        score = weight * y[:, 0] + scale * (1 - weight) * y[:, 1]
        span = np.ptp(score)
        signal = ranking_feedback(y) if feedback == 'rank' else (score - score.min()) / span if span > 0 else np.zeros(population)
        tg = signal * rng.random(population) * np.mean(model.upper - model.lower)
        increment = np.where(tg < lg, np.floor(lg * (1 + rng.random(population))), tg)
        hunger = np.where(signal == 0, 0.0, hunger + increment)
        f, cr = sample_parameters(rng, n, mu_f, mu_cr) if not no_adaptation else (np.full(n, 0.5), np.full(n, 0.5))
        leader_x, leader_y = update_archive(ax, ay, x, y, capacity)
        gbest = np.broadcast_to(leader_x[compromise(leader_y)], (n, x.shape[1]))
        pool = x if no_archive else np.vstack((x, ax))
        reference = pool[rng.integers(len(pool), size=n)]
        probability = gate(progress) if static_gate is None else static_gate
        if no_hunger:
            cooperative = reference + rng.uniform(-2, 2, n)[:, None] * (1 - progress) * np.abs((pbest[:n] if progress < 0.4 else gbest) - x[:n])
            exploratory = x[:n] * (1 + rng.normal(0, a, x[:n].shape))
            mutant = np.where((rng.random(n) < probability)[:, None], exploratory, cooperative)
        else:
            mutant = mutate(x[:n], pbest[:n], gbest, reference, hunger, progress, probability, rng, a, weight_gate)
        trial = crossover(x[:n], mutant, cr, rng)
        trial, valid = model.repair(np.clip(trial, model.lower, model.upper))
        rejected += int((~valid).sum())
        trial[~valid] = x[:n][~valid]
        ty = model.objectives(trial)
        fes += n
        accepted = select_pairs(y[:n], ty) & valid
        indices = np.flatnonzero(accepted)
        x[indices], y[indices] = (trial[indices], ty[indices])
        improved = select_pairs(pbest_y, y)
        pbest[improved], pbest_y[improved] = (x[improved], y[improved])
        if not no_archive:
            ax, ay = update_archive(ax, ay, x, y, capacity)
        if len(indices) and (not no_adaptation):
            mu_f = (1 - adaptation) * mu_f + adaptation * np.sum(f[indices] ** 2) / np.sum(f[indices])
            mu_cr = (1 - adaptation) * mu_cr + adaptation * cr[indices].mean()
    ax, ay = update_archive(ax, ay, x, y, capacity)
    chosen = compromise(ay)
    return dict(decisions=ax, objectives=ay, population=x, population_objectives=y, compromise=ax[chosen].reshape(model.hours, model.units), compromise_objectives=ay[chosen], evaluations=np.array(fes), rejected=np.array(rejected), trace=np.asarray(trace), **checkpoints)

class LMOHADE:

    def __init__(self, particals, max_, min_, thresh, mesh_div=10, LH=10000, L=0.08, a=0.001, weight=0.5, scale=1.0, feedback='weighted', static_gate=None, seed=None, adaptation=0.1, no_hunger=False, no_archive=False, no_adaptation=False):
        self.particals = particals
        self.max_, self.min_ = (max_, min_)
        self.thresh, self.mesh_div = (thresh, mesh_div)
        self.LH, self.L = (LH, L)
        self.a, self.weight, self.scale = (a, weight, scale)
        self.feedback, self.static_gate = (feedback, static_gate)
        self.seed, self.adaptation = (seed, adaptation)
        self.no_hunger, self.no_archive, self.no_adaptation = (no_hunger, no_archive, no_adaptation)

    def done(self, cycle_):
        if not isinstance(cycle_, (int, np.integer)) or cycle_ < 0:
            raise ValueError('cycle_ must be a nonnegative integer')
        model = DEED(self.max_, self.min_)
        seed = self.seed if self.seed is not None else int(np.random.randint(0, 2 ** 32))
        self.result = optimize(model, seed=seed, population=self.particals, evaluations=self.particals * (cycle_ + 1), capacity=self.thresh, a=self.a, lg=self.LH, weight=self.weight, scale=self.scale, feedback=self.feedback, static_gate=self.static_gate, weight_gate=self.L, adaptation=self.adaptation, no_hunger=self.no_hunger, no_archive=self.no_archive, no_adaptation=self.no_adaptation)
        self.archive_in = self.result['decisions']
        self.archive_fitness = self.result['objectives']
        self.in_, self.fitness_ = (self.result['population'], self.result['population_objectives'])
        self.evaluations = int(self.result['evaluations'])
        return (self.archive_in.copy(), self.archive_fitness.copy())
