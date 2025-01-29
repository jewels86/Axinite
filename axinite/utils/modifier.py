import axinite as ax

def modifier_from(functions: list[tuple['function', 'function']]) -> 'function':
    def modifier(body, f, bodies, t, delta, limit, n):
        for function in functions:
            if function[0](body, f, bodies, t, delta, limit, n):
                f = function[1](body, f, bodies, t, delta, limit, n)
        return f
    return modifier