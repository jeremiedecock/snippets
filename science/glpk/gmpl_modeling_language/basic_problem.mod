# USAGE: glpsol -m basic_problem.mod -o basic_problem.sol
#
# A basic 2 variables problem:
#
# max z = x_1 + 2 x_2
# s.t.    x_1 + x_2 <= 6
#               x_2 <= 3
#          x_1, x_2 >= 0
#
# See: http://www.ibm.com/developerworks/linux/library/l-glpk1/
#      http://www.ibm.com/developerworks/linux/library/l-glpk2/
#      http://www.ibm.com/developerworks/linux/library/l-glpk3/

/* Decision variables */
var x1 >=0;
var x2 >=0;

/* Objective function */
maximize z: x1 + 2*x2;

/* Constraints */
s.t. constraint1 : x1 + x2 <= 6;
s.t. constraint2 : x2 <= 3;

end;
