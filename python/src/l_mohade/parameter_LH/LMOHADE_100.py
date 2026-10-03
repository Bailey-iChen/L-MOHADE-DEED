from l_mohade.LMOHADE import LMOHADE


class LMOHADE_100(LMOHADE):
    def __init__(self, particals, max_, min_, thresh, mesh_div=10, LH=100, L=0.08, **kwargs):
        super().__init__(particals, max_, min_, thresh, mesh_div, LH, L, **kwargs)
