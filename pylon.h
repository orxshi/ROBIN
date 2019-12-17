#include <cassert>

extern double U(double c[8], double xl);
extern double r(double H, double W, double N, double phi);

struct Pylon
{
    static double H(double xl);
    static double W(double xl);
    static double N(double xl);
    static double Z(double xl);
    static double yl(double xl, double phi);
    static double zl(double xl, double phi);
};

double Pylon::yl(double xl, double phi)
{
    return r(H(xl), W(xl), N(xl), phi) * std::sin(phi);
}

double Pylon::zl(double xl, double phi)
{
    return r(H(xl), W(xl), N(xl), phi) * std::cos(phi) + Z(xl);
}

double Pylon::H(double xl)
{
    double c[8];

    assert(xl >= 0.4);

    if (xl < 0.8)
    {
        c[0] = 1.0;
        c[1] = -1.0;
        c[2] = -0.8;
        c[3] = 0.4;
        c[4] = 3.0;
        c[5] = 0.0;
        c[6] = 0.145;
        c[7] = 3.0;
    }
    else if (xl < 1.018)
    {
        c[0] = 1.0;
        c[1] = -1.0;
        c[2] = -0.8;
        c[3] = 0.218;
        c[4] = 2.0;
        c[5] = 0.0;
        c[6] = 0.145;
        c[7] = 2.0;
    }
    
    return U(c, xl);
}

double Pylon::W(double xl)
{
    double c[8];

    assert(xl >= 0.4);

    if (xl < 0.8)
    {
        c[0] = 1.0;
        c[1] = -1.0;
        c[2] = -0.8;
        c[3] = 0.4;
        c[4] = 3.0;
        c[5] = 0.0;
        c[6] = 0.166;
        c[7] = 3.0;
    }
    else if (xl < 1.018)
    {
        c[0] = 1.0;
        c[1] = -1.0;
        c[2] = -0.8;
        c[3] = 0.218;
        c[4] = 2.0;
        c[5] = 0.0;
        c[6] = 0.166;
        c[7] = 2.0;
    }

    if (U(c, xl) == 0.)
    {
        std::cout << "xl: " << xl << std::endl;
        std::cout << "c[0]: " << c[0] << std::endl;
        std::cout << "c[1]: " << c[1] << std::endl;
        std::cout << "c[2]: " << c[2] << std::endl;
        std::cout << "c[3]: " << c[3] << std::endl;
        std::cout << "c[4]: " << c[4] << std::endl;
        std::cout << "c[5]: " << c[5] << std::endl;
        std::cout << "c[6]: " << c[6] << std::endl;
        std::cout << "c[7]: " << c[7] << std::endl;
    }

    return U(c, xl);
}

double Pylon::Z(double xl)
{
    double c[8];

    assert(xl >= 0.4);

    if (xl < 0.8)
    {
        c[0] = 0.0;
        c[1] = 0.0;
        c[2] = 0.0;
        c[3] = 0.0;
        c[4] = 0.0;
        c[5] = 0.125;
        c[6] = 0.0;
        c[7] = 0.0;
    }
    else if (xl < 1.018)
    {
        c[0] = 1.0;
        c[1] = -1.0;
        c[2] = -0.8;
        c[3] = 1.1;
        c[4] = 1.5;
        c[5] = 0.065;
        c[6] = 0.06;
        c[7] = 0.6;
    }

    return U(c, xl);
}

double Pylon::N(double xl)
{
    double c[8];

    assert(xl >= 0.4);

    if (xl < 0.8)
    {
        c[0] = 0.0;
        c[1] = 0.0;
        c[2] = 0.0;
        c[3] = 0.0;
        c[4] = 0.0;
        c[5] = 5.0;
        c[6] = 0.0;
        c[7] = 0.0;
    }
    else if (xl < 1.018)
    {
        c[0] = 0.0;
        c[1] = 0.0;
        c[2] = 0.0;
        c[3] = 0.0;
        c[4] = 0.0;
        c[5] = 5.0;
        c[6] = 0.0;
        c[7] = 0.0;
    }

    return U(c, xl);
}
