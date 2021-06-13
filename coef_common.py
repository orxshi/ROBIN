from constant import ZERO

def U(c, xl):

    u = c[5]

    if c[6] != 0:

        if c[1] != 0:
            t = c[0] + c[1] * abs((xl + c[2]) / c[3]) ** c[4]
        else:
            t = c[0]

        if abs(t) <= ZERO:
            t = 0

        assert c[7] > 0
        u += c[6] * t ** (1./c[7])

    return u;
