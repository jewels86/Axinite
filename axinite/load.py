import axinite as ax
from axinite._load_legacy import _load_legacy
from axinite._load_jit import _load_jit
import numpy as np
import astropy.units as u
from astropy.coordinates import CartesianRepresentation

def load(delta, limit, *bodies, t=0 * u.s, modifiers=[], action=lambda *args, **kwargs: None, jit=True):
    if jit:
        body_dtype = np.dtype([
            ("m", np.float64),
            ("r", np.float64, (limit.value/delta.value, 3)),
            ("v", np.float64, (limit.value/delta.value, 3))
        ])
        _bodies = np.array(dtype=body_dtype)
        for body in bodies:
            r = body.r.values()
            v = body.v.values()
            for i, _r in enumerate(r): r[i] = _r.value
            for i, _v in enumerate(v): v[i] = _v.value
            _bodies = np.append(_bodies, np.array([
                (body.mass.value, r, v)
            ]))
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
        return _load_legacy(delta, limit, *bodies, t=t, modifiers=modifiers, action=action)