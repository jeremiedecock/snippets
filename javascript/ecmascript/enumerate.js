const foo = ['A', 'B', 'C'];

foo.map((element, index) => console.log(index, element));

// Alternative method

console.log()

for (const [index, element] of foo.entries()) {
    console.log(index, element);
}
