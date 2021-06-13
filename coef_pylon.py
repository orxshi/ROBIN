from coef_common import U

class Pylon:

    def H(xl):

        if xl < 0.8:
            c = [1.0, -1.0, -0.8, 0.4, 3.0, 0.0, 0.145, 3.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 0.218, 2.0, 0.0, 0.145, 2.0]
        else:
            print("error Hpylon")

        return U(c, xl);


    def W(xl):

        if xl < 0.8:
            c = [1.0, -1.0, -0.8, 0.4, 3.0, 0.0, 0.166, 3.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 0.218, 2.0, 0.0, 0.166, 2.0]
        else:
            print("error Wpylon")

        return U(c, xl);


    def Z(xl):

        if xl < 0.4:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.125, 0.0, 0.0]
        elif xl < 1.018:
            c = [1.0, -1.0, -0.8, 1.1, 1.5, 0.065, 0.06, 0.6]
        else:
            print("error Zpylon")

        return U(c, xl);


    def N(xl):

        if xl < 0.4:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        elif xl < 1.018:
            c = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0]
        else:
            print("error Npylon")

        return U(c, xl);
