from l_mohade.LMOHADE import LMOHADE


class LMOHADE_10(LMOHADE):
    def __init__(self, particals, max_, min_, thresh, mesh_div=10, LH=10000, L=0.08, **kwargs):
        kwargs.setdefault('a', 10.0)
        super().__init__(particals, max_, min_, thresh, mesh_div, LH, L, **kwargs)
