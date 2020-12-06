const foo = ['A', 'B', 'C'];

for(const [index, value] of foo.entries()) 
    console.log(index, value);




// Alternative method

console.log()

foo.map((value, index) => console.log(index, value));




bar = foo.map((value, index) => index + ":" + value);
