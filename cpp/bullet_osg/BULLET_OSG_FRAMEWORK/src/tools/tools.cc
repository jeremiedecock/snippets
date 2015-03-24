/* 
 * Bullet OSG Framework.
 * Tools module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "tools.h"

#include <cstdio>

std::string simulator::eigen_vector_to_string(const Eigen::VectorXd &eigen_vector, std::string separator) {
    std::ostringstream oss;

    for(unsigned int i=0 ; i < eigen_vector.size() ; i++) {
        oss << eigen_vector[i];
        if((i + 1) < eigen_vector.size()) {
            oss << separator;
        }
    }

    return oss.str();
}


bool simulator::file_exists(const char * filename) {
    if(FILE * file = fopen(filename, "r")) {
        fclose(file);
        return true;
    }
    return false;
}

