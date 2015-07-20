/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Collections_avec_cl%C3%A9s#Le_type_Map
 */

// This script requires ECMAScript 6 or above.

var dict = new Map();

dict.set("one", 1);
dict.set("two", 2);
dict.set("three", 3);
dict.set("four", 4);

print(dict);

print(dict.size);

print(dict.has("one"));
print(dict.get("one"));

dict.delete("one");

for(var [key, val] of dict) {
    print(key, ":", val);
}
