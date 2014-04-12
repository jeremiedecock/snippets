# USAGE: glpsol -m stocks.mod -o stocks.sol

/* *** DATA DECLARATION ************************* */

param c1;
param c2;
param c3;
param c4;
param c5;

/* *** DECISION VARIABLES *********************** */

var d1 >= -10, <= 10;
var d2 >= -10, <= 10;
var d3 >= -10, <= 10;
var d4 >= -10, <= 10;
var d5 >= -10, <= 10;

var s1 >= 0, <= 30;
var s2 >= 0, <= 30;
var s3 >= 0, <= 30;
var s4 >= 0, <= 30;
var s5 >= 0, <= 30;

/* *** OBJECTIVE FUNCTION *********************** */

maximize profit_total: c1 * -d1 + c2 * -d2 + c3 * -d3 + c4 * -d4 + c5 * -d5;

/* *** CONSTRAINTS ****************************** */

s.t. constraint_transition_1 : s1      - d1 = 0;
s.t. constraint_transition_2 : s2 - s1 - d2 = 0;
s.t. constraint_transition_3 : s3 - s2 - d3 = 0;
s.t. constraint_transition_4 : s4 - s3 - d4 = 0;
s.t. constraint_transition_5 : s5 - s4 - d5 = 0;

/* *** DATA SECTION ***************************** */

data;

param c1:=10;
param c2:=20;
param c3:=10;
param c4:=20;
param c5:=10;

end;
