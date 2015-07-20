/*
 * See: https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Collections_index%C3%A9es#M%C3%A9thodes_des_tableaux
 */

var tab1 = ["a", "b", "c", "c"];
var tab2 = [1, "two", 3.0];

print(tab1);
print(tab2);

print(tab1.length);

print(tab1[0]);

print(tab1.concat(tab2));

print(tab1.join('---'));

tab1.push("four");
print(tab1);

tab1.pop();
print(tab1);

tab1.shift("four");
print(tab1);

tab1.unshift("five");
print(tab1);

print(tab1.slice(1,3));

tab1.reverse();
print(tab1);

tab1.sort();
print(tab1);

print(tab1.indexOf("c"));

print(tab1.lastIndexOf("c"));


function func1(obj) {
    print(">", obj);
}

tab1.forEach(func1);


function func2(obj) {
    return obj.toUpperCase();
}

print(tab1.map(func2));


function func3(obj) {
    return typeof obj == 'number';
}

print(tab2.filter(func3));


print(tab2.every(func3));


print(tab2.some(func3));

