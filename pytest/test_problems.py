#!/usr/bin/env python
# coding: utf-8

from itertools import product

import pytest

import numpy as np

from capytaine.problems import *
from capytaine.reference_bodies import DummyBody

dummy = DummyBody()

def test_depth():
    assert PotentialFlowProblem(dummy, free_surface=np.infty, sea_bottom=-np.infty).depth == np.infty
    assert PotentialFlowProblem(dummy, free_surface=0.0, sea_bottom=-np.infty).depth == np.infty
    assert PotentialFlowProblem(dummy, free_surface=0.0, sea_bottom=-1.0).depth == 1.0

    with pytest.raises(Exception):
        PotentialFlowProblem(dummy, free_surface=0.0, sea_bottom=1.0)

def test_Airy():
    """Compare finite depth Airy wave expression with results from analytical
    expression"""
    try:
        import sympy as sp
        from sympy.abc import t
        from sympy.physics.vector import ReferenceFrame
        from sympy.physics.vector import gradient, divergence

        R = ReferenceFrame('R')
        x, y, z = R[0], R[1], R[2]
        Phi, k, h, g, rho = sp.symbols("Phi, k, h, g, rho")

        omega = sp.sqrt(g*k*sp.tanh(k*h))
        Phi = g/omega * sp.cosh(k*(z+h))/sp.cosh(k*h) * sp.sin(k*x - omega*t)
        u = gradient(Phi, R)
        p = -rho*Phi.diff(t)

        for depth in np.linspace(100.0, 10.0, 2):
            for omega in np.linspace(0.5, 4.0, 2):

                dp = DiffractionProblem(dummy, free_surface=0.0, sea_bottom=-depth, omega=omega)

                for t_val, x_val, y_val, z_val in product(np.linspace(0.0, 1.0, 2),
                                                          np.linspace(-10, 10, 3),
                                                          np.linspace(-10, 10, 3),
                                                          np.linspace(-10, 0, 3)):

                    parameters = {t:t_val, x:x_val, y:y_val, z:z_val,
                                  omega:dp.omega, k:dp.wavenumber,
                                  h:dp.depth, g:dp.g, rho:dp.rho}
                    u_num = dp.Airy_wave(np.array((x_val, y_val, z_val)))

                    assert np.isclose(float(u.dot(R.x).subs(parameters)),
                                      np.real(u_num[0]*np.exp(-1j * dp.omega * t_val)),
                                      rtol=1e-3
                                      )
                    assert np.isclose(float(u.dot(R.y).subs(parameters)),
                                      np.real(u_num[1]*np.exp(-1j * dp.omega * t_val)),
                                      rtol=1e-3
                                      )
                    assert np.isclose(float(u.dot(R.z).subs(parameters)),
                                      np.real(u_num[2]*np.exp(-1j * dp.omega * t_val)),
                                      rtol=1e-3
                                      )
                    # assert np.isclose(float(p.subs(parameters)),
                    #                   np.real(p_num*np.exp(-1j * dp.omega * t_val)),
                    #                   rtol=1e-3
                    #                   )
    except ImportError:
        pass
