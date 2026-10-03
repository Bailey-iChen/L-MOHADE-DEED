from l_mohade.LMOHADE import LMOHADE


class LMOHADE_10(LMOHADE):
    def __init__(self, particals, max_, min_, thresh, mesh_div=10, LH=10, L=0.08, **kwargs):
        super().__init__(particals, max_, min_, thresh, mesh_div, LH, L, **kwargs)
