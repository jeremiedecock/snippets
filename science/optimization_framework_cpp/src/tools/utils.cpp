/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#include <algorithm>
#include <functional>
#include <numeric>

#include <cmath>
#include "tools/utils.h"

double average_value(const std::vector<double> & v)
{
    return std::accumulate(v.begin(), v.end(), 0.0) / v.size();
}

double standard_deviation(const std::vector<double> & v)
{
    double avg_value = average_value(v);

    std::vector<double> diff(v.size());
    std::transform(v.begin(), v.end(), diff.begin(), std::bind2nd(std::minus<double>(), avg_value));

    double sq_sum = std::inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);

    return std::sqrt(sq_sum / v.size());
}

double expressed_in_percent(const double & value_to_express, const double & reference_value)
{
    return 100.0 * abs(value_to_express) / abs(reference_value);
}

