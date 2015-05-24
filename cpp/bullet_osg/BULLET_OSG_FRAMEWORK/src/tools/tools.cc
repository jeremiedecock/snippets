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
#include <fstream>       // for std::ifstream
#include <string>
#include <vector>

std::vector<double> simulator::text_file_to_std_vector(const std::string & file_name) {
    std::vector<double> std_vector;

    std::ifstream ifs(file_name);
    // TODO : check file_name ?

    double num;
    while(ifs >> num) {
        std_vector.push_back(num);
    }

    ifs.close();

    return std_vector;
}

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


Eigen::Vector2d simulator::string_to_eigen_vector2(const std::string & string_vector) {
    std::vector<double> std_vector = simulator::string_to_std_vector<double>(string_vector);
    if(std_vector.size() != 2) throw std::invalid_argument("Requires a vector with 2 elements.");
    return Eigen::Vector2d(std_vector[0], std_vector[1]); //TODO
}


Eigen::Vector3d simulator::string_to_eigen_vector3(const std::string & string_vector) {
    std::vector<double> std_vector = simulator::string_to_std_vector<double>(string_vector);
    if(std_vector.size() != 3) throw std::invalid_argument("Requires a vector with 3 elements.");
    return Eigen::Vector3d(std_vector[0], std_vector[1], std_vector[2]); //TODO
}


Eigen::Vector4d simulator::string_to_eigen_vector4(const std::string & string_vector) {
    std::vector<double> std_vector = simulator::string_to_std_vector<double>(string_vector);
    if(std_vector.size() != 4) throw std::invalid_argument("Requires a vector with 4 elements.");
    return Eigen::Vector4d(std_vector[0], std_vector[1], std_vector[2], std_vector[3]); //TODO
}


bool simulator::file_exists(const char * filename) {
    if(FILE * file = fopen(filename, "r")) {
        fclose(file);
        return true;
    }
    return false;
}

