from math import degrees
from .common import calc_angle, MAX_OPENING_ANGLE, MAX_MERGE_ANGLE, ShellNode


def calc_lig_rig_total(n0: ShellNode, n1: ShellNode):
    def cond_1():
        d = {"n0": {"h": n0.h}, "n1": {"h": n1.h}}
        label_e = "h"
        e = d["n0"][label_e]
        label_f = "h"
        f = d["n1"][label_f]
        if degrees(calc_angle(f, e)) > MAX_MERGE_ANGLE:
            return (False, None)
        d["n1"][label_f] = e
        d |= {"merged": [("n1" + label_f, "n0" + label_e)]}
        return (True, d)

    def cond_2():
        d = {"n0": {"h": n0.h}, "n1": {"h": n1.h}}
        label_e = "h"
        e = d["n0"][label_e]
        label_f = "h"
        f = d["n1"][label_f]
        if degrees(calc_angle(f, e)) > MAX_OPENING_ANGLE:
            return (False, None)
        d |= {"bar1": ["n1" + label_f, "n0" + label_e]}
        return (True, d)

    def cond_3():
        d = {"n0": {"h": n0.h}, "n1": {"h": n1.h}}
        label_e = "h"
        e = d["n0"][label_e]
        label_f = "h"
        f = d["n1"][label_f]
        if degrees(calc_angle(f, -e)) < 0.5:
            return (False, None)
        if degrees(calc_angle(f, -e)) > MAX_OPENING_ANGLE:
            return (False, None)
        d |= {"bar1": ["n1" + label_f, "n0" + label_e]}
        d |= {"inverted": ["n0" + label_e]}
        return (True, d)

    for cond in [cond_1, cond_2, cond_3]:
        b, d = cond()
        if b:
            return d
