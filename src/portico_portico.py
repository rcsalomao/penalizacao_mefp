import numpy as np
from math import degrees
from itertools import combinations
from .common import (
    calc_angle,
    calc_perpend_projected_vec,
    MAX_MERGE_ANGLE,
    MAX_OPENING_ANGLE,
    MAX_PROJECTED_ANGLE,
    MIN_PROJECTED_ANGLE,
    BeamNode,
)
from numpy.typing import NDArray


def calc_lig_rig_parcial(n0: BeamNode, n1: BeamNode, n1_free_g: NDArray):
    def cond_1():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for label_f, f in d["n1"].items():
            if id(f) == id(n1_free_g):
                continue
            for label_e, e in d["n0"].items():
                if degrees(calc_angle(f, e)) > MAX_MERGE_ANGLE:
                    continue
                d["n1"][label_f] = e
                d |= {"merged": [(label_f, label_e)]}
                return (True, d)
        return (False, None)

    def cond_2():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for label_f, f in d["n1"].items():
            if id(f) == id(n1_free_g):
                continue
            label_e = "n0g1"
            e = d["n0"][label_e]
            if degrees(calc_angle(e, f)) > MAX_OPENING_ANGLE:
                continue
            label_m = "n0g2"
            m = d["n0"][label_m]
            if degrees(calc_angle(m, f)) > MAX_OPENING_ANGLE:
                continue
            v1 = calc_perpend_projected_vec(f, e)
            v2 = calc_perpend_projected_vec(f, m)
            ang = degrees(calc_angle(v1, v2))
            if MIN_PROJECTED_ANGLE < ang < MAX_PROJECTED_ANGLE:
                d |= {"bar1": [label_f, label_e], "bar2": [label_f, label_m]}
                return (True, d)
        return (False, None)

    def cond_3():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for label_f, f in d["n1"].items():
            if id(f) == id(n1_free_g):
                continue
            new_point = np.cross(*(d["n0"].values()))
            for combi in combinations(
                [("np", new_point), *(d["n0"].items())],
                2,
            ):
                label_e, e = combi[0]
                if degrees(calc_angle(e, f)) > MAX_OPENING_ANGLE:
                    continue
                label_m, m = combi[1]
                if degrees(calc_angle(m, f)) > MAX_OPENING_ANGLE:
                    continue
                v1 = calc_perpend_projected_vec(f, e)
                v2 = calc_perpend_projected_vec(f, m)
                ang = degrees(calc_angle(v1, v2))
                if MIN_PROJECTED_ANGLE < ang < MAX_PROJECTED_ANGLE:
                    d |= {
                        "bar1": ["np", "n0g1"],
                        "bar2": ["np", "n0g2"],
                        "bar3": ["np", "n0"],
                    }
                    d |= {"bar4": [label_f, label_e], "bar5": [label_f, label_m]}
                    d |= {"np": new_point}
                    return (True, d)
        return (False, None)

    for cond in [cond_1, cond_2, cond_3]:
        b, d = cond()
        if b:
            return d


def calc_lig_rig_total(n0: BeamNode, n1: BeamNode):
    def cond_1():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for couple1, couple2 in [
            (("n1g1", "n0g1"), ("n1g2", "n0g2")),
            (("n1g2", "n0g1"), ("n1g1", "n0g2")),
        ]:
            f = d["n1"][couple1[0]]
            e = d["n0"][couple1[1]]
            if degrees(calc_angle(f, e)) > MAX_MERGE_ANGLE:
                continue
            n = d["n1"][couple2[0]]
            m = d["n0"][couple2[1]]
            if degrees(calc_angle(n, m)) > MAX_MERGE_ANGLE:
                continue
            d["n1"][couple1[0]] = e
            d["n1"][couple2[0]] = m
            d |= {"merged": [couple1, couple2]}
            return (True, d)
        return (False, None)

    def cond_2():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for couple, pair in [
            (("n1g1", "n0g1"), ("n1g2", "n0g2")),
            (("n1g2", "n0g1"), ("n1g1", "n0g2")),
            (("n1g1", "n0g2"), ("n1g2", "n0g1")),
            (("n1g2", "n0g2"), ("n1g1", "n0g1")),
        ]:
            f = d["n1"][couple[0]]
            e = d["n0"][couple[1]]
            if degrees(calc_angle(f, e)) > MAX_MERGE_ANGLE:
                continue
            n = d["n1"][pair[0]]
            m = d["n0"][pair[1]]
            if degrees(calc_angle(n, m)) > MAX_OPENING_ANGLE:
                continue
            d["n1"][couple[0]] = e
            d |= {"bar": [*pair]}
            d |= {"merged": [couple]}
            return (True, d)
        return (False, None)

    def cond_3():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for couple, pair in [
            (("n1g1", "n0g1"), ("n1g2", "n0g2")),
            (("n1g2", "n0g1"), ("n1g1", "n0g2")),
            (("n1g1", "n0g2"), ("n1g2", "n0g1")),
            (("n1g2", "n0g2"), ("n1g1", "n0g1")),
        ]:
            f = d["n1"][couple[0]]
            e = d["n0"][couple[1]]
            if degrees(calc_angle(f, e)) > MAX_MERGE_ANGLE:
                continue
            n = d["n1"][pair[0]]
            m = d["n0"][pair[1]]
            new_point = np.cross(e, m)
            if degrees(calc_angle(new_point, n)) > MAX_OPENING_ANGLE:
                continue
            d["n1"][couple[0]] = e
            d |= {
                "bar1": ["np", couple[1]],
                "bar2": ["np", pair[1]],
                "bar3": ["np", "n0"],
            }
            d |= {"bar4": [pair[0], "np"]}
            d |= {"np": new_point}
            return (True, d)
        return (False, None)

    def cond_4():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        for label_f, f in d["n1"].items():
            e = d["n0"]["n0g1"]
            if degrees(calc_angle(e, f)) > MAX_OPENING_ANGLE:
                continue
            m = d["n0"]["n0g2"]
            if degrees(calc_angle(m, f)) > MAX_OPENING_ANGLE:
                continue
            v1 = calc_perpend_projected_vec(f, e)
            v2 = calc_perpend_projected_vec(f, m)
            ang = degrees(calc_angle(v1, v2))
            if not (MIN_PROJECTED_ANGLE < ang < MAX_PROJECTED_ANGLE):
                continue
            for label_n, n in d["n1"].items():
                if label_f == label_n:
                    continue
                for label_o, o in d["n0"].items():
                    if degrees(calc_angle(o, n)) > MAX_OPENING_ANGLE:
                        continue
                    v3 = calc_perpend_projected_vec(n, o)
                    ang = degrees(calc_angle(f, v3))
                    if MIN_PROJECTED_ANGLE < ang < MAX_PROJECTED_ANGLE:
                        d |= {
                            "bar1": [label_f, "n0g1"],
                            "bar2": [label_f, "n0g2"],
                            "bar3": [label_n, label_o],
                        }
                        return (True, d)
        return (False, None)

    def cond_5():
        d = {"n0": {"n0g1": n0.g1, "n0g2": n0.g2}, "n1": {"n1g1": n1.g1, "n1g2": n1.g2}}
        new_point = np.cross(*(d["n0"].values()))
        for label_f, f in d["n1"].items():
            for combi in combinations([("np", new_point), *(d["n0"].items())], 2):
                label_e, e = combi[0]
                if degrees(calc_angle(e, f)) > MAX_OPENING_ANGLE:
                    continue
                label_m, m = combi[1]
                if degrees(calc_angle(m, f)) > MAX_OPENING_ANGLE:
                    continue
                v1 = calc_perpend_projected_vec(f, e)
                v2 = calc_perpend_projected_vec(f, m)
                ang = degrees(calc_angle(v1, v2))
                if not (MIN_PROJECTED_ANGLE < ang < MAX_PROJECTED_ANGLE):
                    continue
                for label_n, n in d["n1"].items():
                    if label_f == label_n:
                        continue
                    for label_o, o in [("np", new_point), *(d["n0"].items())]:
                        if degrees(calc_angle(o, n)) > MAX_OPENING_ANGLE:
                            continue
                        v3 = calc_perpend_projected_vec(n, o)
                        ang = degrees(calc_angle(f, v3))
                        if MIN_PROJECTED_ANGLE < ang < MAX_PROJECTED_ANGLE:
                            d |= {
                                "bar1": ["np", "n0g1"],
                                "bar2": ["np", "n0g2"],
                                "bar3": ["np", "n0"],
                            }
                            d |= {
                                "bar4": [label_f, label_e],
                                "bar5": [label_f, label_m],
                                "bar6": [label_n, label_o],
                            }
                            d |= {"np": new_point}
                            return (True, d)
        return (False, None)

    for cond in [cond_1, cond_2, cond_3, cond_4, cond_5]:
        b, d = cond()
        if b:
            return d
