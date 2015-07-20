/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Collections_avec_cl%C3%A9s#Les_ensembles
 */

// This script requires ECMAScript 6 or above.

var set = new Set();

set.add("one");
set.add(2);
set.add("three");
set.add(4);

print(set);

print(set.size);

print(set.has("one"));

set.delete("one");

for(var item of set) {
    print(item);
}
