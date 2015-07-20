/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Fonctions
 */

function print_var(input) {
    print(input);
}

var v1 = "Hello";

print_var(v1);

///////////////////////////////////////////////////////////////////////////////

function factorial(n){
    if ((n == 0) || (n == 1))
        return 1;
    else
        return (n * factorial(n - 1));
}

print(factorial(4));
