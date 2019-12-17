#include <vector>
#include <cassert>
#include <fstream>
#include <iostream>
#include <cmath>
#include "mainbody.h"
#include "pylon.h"

double PI = 3.14159265359;
double ZERO = 1e-10;

double U(double c[8], double xl)
{
    double u = c[5];
    if (c[6] != 0.)
    {
        double t1 = (xl + c[2]) / c[3];
        //if (std::abs(t1) <= ZERO)
        //{
            //t1 = 0.;
        //}
        double t2 = c[0] + c[1] * std::pow(std::abs(t1), c[4]);
        if (std::abs(t2) <= ZERO)
        {
            t2 = 0.;
        }
        u += c[6] * std::pow(t2, (1./c[7]));
    }
    if (std::isnan(u))
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
        std::cout << "t1: " << std::pow((xl + c[2]) / c[3], c[4]) << std::endl;
        std::cout << "t2: " << c[0] + c[1] * std::pow((xl + c[2]) / c[3], c[4]) << std::endl;
        
        
    }
    assert(!std::isnan(u));
    return u;
    //return c[5] + c[6] * std::pow(c[0] + c[1] * std::pow((xl + c[2]) / c[3], c[4]), (1./c[7]));
}

double r(double H, double W, double N, double phi)
{
    assert(!std::isnan(H));
    assert(!std::isnan(W));
    assert(!std::isnan(N));
    assert(!std::isnan(phi));
    assert(N != 0.);
    double res = std::pow((std::pow(0.25 * H * W, N) / (std::pow(std::abs(0.5 * H * std::sin(phi)), N) + std::pow(std::abs(0.5 * W * std::cos(phi)), N))), 1./N);
    if (std::isnan(res))
    {
        std::cout << "H: " << H << std::endl;
        std::cout << "W: " << W << std::endl;
        std::cout << "N: " << N << std::endl;
        std::cout << "phi: " << phi << std::endl;
        std::cout << "cos: " << std::cos(phi) << std::endl;
        std::cout << "sin: " << std::sin(phi) << std::endl;
        //std::cout << "t1: " << std::pow(0.25 * H * W, N) << std::endl;
        std::cout << "t2: " << (std::pow(0.5 * H * std::sin(phi), N) + std::pow(0.5 * W * std::cos(phi), N)) << std::endl;
    }
    assert(!std::isnan(res));
    return res;
    //return std::pow((std::pow(0.25 * H * W, N) / (std::pow(0.5 * H * std::sin(phi), N) + std::pow(0.5 * W * std::cos(phi), N))), 1./N);
}

void generate(double begin, double end, double inc, std::vector<double>& v)
{
    for (double d=begin; d<end; d=d+inc)
    {
        v.push_back(d);
    }
}

int main()
{
    std::vector<double> xmainbody, xpylon, p;

    generate(0.00001, 2.0, 0.1, xmainbody);
    generate(0.400001, 1.018, 0.1, xpylon);
    generate(0.0, 2*PI, 0.01, p);

    std::ofstream out;
    out.open("robin.dat");

    for (double d: xmainbody)
    {
        for (double r: p)
        {
            out << d << " " << MainBody::yl(d, r) << " " << MainBody::zl(d, r) << std::endl;
        }
    }

    for (double d: xpylon)
    {
        for (double r: p)
        {
            out << d << " " << Pylon::yl(d, r) << " " << Pylon::zl(d, r) << std::endl;
        }
    }

    out.close();

    return 0;
}
