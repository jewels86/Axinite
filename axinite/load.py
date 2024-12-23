import axinite as ax
from axinite._load_legacy import _load_legacy
from axinite._load_jit import _load_jit
import numpy as np
import astropy.units as u
from astropy.coordinates import CartesianRepresentation
from numba import njit

def load(delta, limit, *bodies, t=0 * u.s, modifiers=[], action=None, jit=True):
    if jit:
        @njit
        def jit_action(*args, **kwargs): return None
        if not action: action = jit_action
        body_dtype = np.dtype([
            ("m", np.float64),
            ("r", np.float64, (int(limit.value/delta.value), 3)),
            ("v", np.float64, (int(limit.value/delta.value), 3))
        ])
        _bodies = np.array([], dtype=body_dtype)
        for body in bodies:
            _r = body.r.values()
            _v = body.v.values()
            r = np.zeros((int(limit.value/delta.value), 3))
            v = np.zeros((int(limit.value/delta.value), 3))
            for i, __r in enumerate(_r): 
                r[i][0] = __r.x.value
                r[i][1] = __r.y.value
                r[i][2] = __r.z.value
            for i, __v in enumerate(_v):
                v[i][0] = __v.x.value
                v[i][1] = __v.y.value
                v[i][2] = __v.z.value
            np.append(_bodies, np.array([
                (body.mass.value, r, v)
            ], dtype=body_dtype))
        _bodies = _load_jit(delta.value, limit.value, _bodies)
        __bodies = ()
        for body in _bodies: 
            _body = ax.Body(body["m"] * u.kg, CartesianRepresentation(body["r"][0], u.m), CartesianRepresentation(body["v"][0], u.m/u.s))
            for i, r in enumerate(body["r"]):
                _body.r[i] = CartesianRepresentation(r, u.m)
            for i, v in enumerate(body["v"]):
                _body.v[i] = CartesianRepresentation(v, u.m/u.s)
            __bodies += (_body,)
        return __bodies

    else:
        if not action: action = lambda *args, **kwargs: None
        return _load_legacy(delta, limit, *bodies, t=t)