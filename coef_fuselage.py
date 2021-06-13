from coef_common import U

class Fuselage:

    def H(xl):

        if xl < 0.4:
            c = [1.0, -1.0, -0.4, 0.4, 1.8, 0.0, 0.25, 1.8]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0]
        elif xl < 1.9:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.05, 0.2, 0.6]
        elif xl < 2.0:
            c = [1.0, -1.0, -1.9, 0.1, 2.0, 0.0, 0.05, 2.0]
        else:
            print("error H")

        return U(c, xl);


    def W(xl):

        if xl < 0.4:
            c = [1.0, -1.0, -0.4, 0.4, 2.0, 0.0, 0.25, 2.0]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0]
        elif xl < 1.9:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.05, 0.2, 0.6]
        elif xl < 2.0:
            c = [1.0, -1.0, -1.9, 0.1, 2.0, 0.0, 0.05, 2.0]
        else:
            print("error W")

        return U(c, xl);


    def Z(xl):

        if xl < 0.4:
            c = [1.0, -1.0, -0.4, 0.4, 1.8, -0.08, 0.08, 1.8]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif xl < 1.9:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.04, -0.04, 0.6]
        elif xl < 2.0:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.04, 0.0, 0.0]

        return U(c, xl);


    def N(xl):

        if xl < 0.4:
            c = [2.0, 3.0, 0.0, 0.4, 1.0, 0.0, 1.0, 1.0]
        elif xl < 0.8:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        elif xl < 1.9:
            c = [5.0, -3.0, -0.8, 1.1, 1.0, 0.0, 1.0, 1.0]
        elif xl < 2.0:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 1.0]
        else:
            print("error N")

        return U(c, xl);