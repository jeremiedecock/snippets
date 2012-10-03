#include <algorithm>
#include <functional>
#include <numeric>

#include <cmath>
#include <cstdio>

#include "tools.h"

/**
 * Return the mean value for a vector of double.
 */
double tools::average_value(const std::vector<double> & v)
{
    return std::accumulate(v.begin(), v.end(), 0.0) / v.size();
}

/**
 * Return the standard deviation for a vector of double.
 */
double tools::standard_deviation(const std::vector<double> & v)
{
    double avg_value = average_value(v);

    std::vector<double> diff(v.size());
    std::transform(v.begin(), v.end(), diff.begin(), std::bind2nd(std::minus<double>(), avg_value));

    double sq_sum = std::inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);

    return std::sqrt(sq_sum / v.size());
}
