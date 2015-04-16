/* 
 * Bullet OSG Framework.
 * Common options parser module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef COMMON_OPTIONS_PARSER_H
#define COMMON_OPTIONS_PARSER_H

#include <boost/program_options.hpp>

#include <string>

namespace po = boost::program_options;

namespace simulator {

    class CommonOptionsParser {
        public:
            // Common options
            po::variables_map variableMap;

            bool useFullScreenMode;
            bool useHeadLessMode;

            double timeStepDurationSec;
            double tickDurationSec;
            int maxTicksPerTimeStep;

            double simulationDurationSec;

            std::string configFile;

            bool exit;
            int exitValue;

            bool verbose;

        public:
            CommonOptionsParser(int argc,
                                char * argv[],
                                const po::options_description & local_options_desc);
    };
}

#endif // COMMON_OPTIONS_PARSER_H
