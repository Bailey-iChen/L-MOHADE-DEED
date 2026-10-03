from l_mohade.LMOHADE import LMOHADE


class LMOHADE_0001(LMOHADE):
    def __init__(self, particals, max_, min_, thresh, mesh_div=10, LH=10000, L=0.08, **kwargs):
        kwargs.setdefault('a', 0.001)
        super().__init__(particals, max_, min_, thresh, mesh_div, LH, L, **kwargs)
