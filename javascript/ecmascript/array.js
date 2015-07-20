/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Collections_index%C3%A9es#M%C3%A9thodes_des_tableaux
 */

var tab1 = ["one", "two", "three"];
var tab2 = [1, "two", 3.0];

print(tab1);
print(tab2);

print(tab1.length);

print(tab1[0]);

print(tab1.concat(tab2))

print(tab1.join('---'))

tab1.push("four")
print(tab1);

tab1.pop()
print(tab1);

tab1.shift("four")
print(tab1);

tab1.unshift("five")
print(tab1);

print(tab1.slice(1,3));

tab1.reverse()
print(tab1);

tab1.sort()
print(tab1);
