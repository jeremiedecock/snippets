/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Collections_index%C3%A9es#M%C3%A9thodes_des_tableaux
 */

// This script requires ECMAScript v7

var tab1 = [1, 2, 3, 4];
var tab2 = [i * 2 for (i of tab1)];

print(tab2);

