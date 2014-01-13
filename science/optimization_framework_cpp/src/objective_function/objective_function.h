/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 *
 *  TODO: doit être un objet qui permet de connaître:
 *  - le dommaine de définition de x
 *    - continu / discret ?
 *    - contraint ou non
 *  - le nombre de dimensions de x
 *  - minimisation ou maximisation
 */

#ifndef OBJECTIVE_FUNCTION_H
#define OBJECTIVE_FUNCTION_H

#include <vector>

class ObjectiveFunction {

    protected:

        int ndim;
        std::vector<double> domainMin;
        std::vector<double> domainMax;

    public:

        double operator() (const std::vector<double> & x) const;

        std::vector<double> operator() (const std::vector<std::vector<double> > & x) const;

        int getDimension() const;

        std::vector<double> getDomainMin() const;

        std::vector<double> getDomainMax() const;


    protected:

        virtual double eval_one_sample(const std::vector<double> & x) const = 0;

        // This function can be redefined to speedup computations
        virtual std::vector<double> eval_multiple_samples(const std::vector<std::vector<double> > & x) const;

        virtual void plot(const std::vector<double> & xmin, const std::vector<double> & xmax) const;

};

#endif //OBJECTIVE_FUNCTION_H
