const foo = ['A', 'B', 'C'];

foo.map((value, index) => console.log(index, value));

// Alternative method

console.log()

for(let [index, value] of foo.entries()) 
    console.log(index, value);

// Alternative method

console.log()

for (const [index, value] of foo.entries()) {
    console.log(index, value);
}
