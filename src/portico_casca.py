from math import degrees, inf
from .common import calc_angle, MAX_OPENING_ANGLE, MAX_MERGE_ANGLE, BeamNode, ShellNode


def calc_lig_full_rig(n0: BeamNode, n1: ShellNode):
    def cond_1():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"h": n1.h}}
        label_f = "h"
        f = d["n1"][label_f]
        for label_e, e in d["n0"].items():
            if degrees(calc_angle(f, e)) > MAX_MERGE_ANGLE:
                continue
            d["n1"][label_f] = e
            d |= {"merged": [("n1" + label_f, label_e)]}
            return (True, d)
        return (False, None)

    def cond_2():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"h": n1.h}}
        label_f = "h"
        f = d["n1"][label_f]
        ang = inf
        for label, e in d["n0"].items():
            a = degrees(calc_angle(f, e))
            if a < ang:
                ang = a
                label_e = label
        if ang > MAX_OPENING_ANGLE:
            return (False, None)
        d |= {"bar1": ["n1" + label_f, label_e]}
        return (True, d)

    for cond in [cond_1, cond_2]:
        b, d = cond()
        if b:
            return d
