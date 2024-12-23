import axinite as ax
from axinite._load import _load
from axinite._load_jit import _load_jit
import numpy as np

def load(delta, limit, *bodies, t=0, modifiers=[], action=lambda *args, **kwargs: None, jit=True):
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
            

    else:
        return _load(delta, limit, action, *bodies, t=0, modifiers=modifiers)