import src.portico_portico as pp
import src.portico_casca as pc
import src.casca_casca as cc
from src.common import uvec, BeamNode, ShellNode
import numpy as np

np.set_printoptions(precision=3)


def portico_portico_test():
    n0 = BeamNode(uvec(np.array([1, 0, 0])), uvec(np.array([0, 1, 0])))
    n1 = BeamNode(uvec(np.array([-1, 0, 0])), uvec(np.array([0, 1, 0])))
    d = pp.calc_lig_rig_parcial(n0, n1, n1.g2)
    print(d)

    n0 = BeamNode(uvec(np.array([1, 0, 0])), uvec(np.array([0, 1, 0])))
    n1 = BeamNode(uvec(np.array([1, 0.1, 0])), uvec(np.array([0, 1, 0])))
    d = pp.calc_lig_rig_total(n0, n1)
    print(d)


def portico_casca_test():
    n0 = BeamNode(uvec(np.array([1, 0, 0])), uvec(np.array([0, 1, 0])))
    n1 = ShellNode(uvec(np.array([0.159, 1, 0])))
    d = pc.calc_lig_rig_total(n0, n1)
    print(d)


def casca_casca_test():
    n0 = ShellNode(uvec(np.array([0, 1, 0])))
    n1 = ShellNode(uvec(np.array([0, 1, 0.1])))
    d = cc.calc_lig_rig_total(n0, n1)
    print(d)


portico_portico_test()
portico_casca_test()
casca_casca_test()
