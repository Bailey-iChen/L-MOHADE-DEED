from l_mohade.LMOHADE import LMOHADE


class LMOHADE_l_007(LMOHADE):
    def __init__(self, particals, max_, min_, thresh, mesh_div=10, LH=10000, L=0.07, **kwargs):
        kwargs.setdefault('static_gate', L)
        super().__init__(particals, max_, min_, thresh, mesh_div, LH, L, **kwargs)
