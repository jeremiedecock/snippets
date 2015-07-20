/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Types_et_grammaire
 */

function print_var(input) {
    if(input === undefined) {        // Check if the variable is defined
        print("Undefined variable");
    } else {
        print(input);
    }
}

var v1;
var v2 = 5;

print_var(v1);
print_var(v2);

