// https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Fonctions/Fonctions_fl%C3%A9ch%C3%A9es

const l1 = [
      'Hydrogen',
      'Helium',
      'Lithium',
      'Beryllium'
];

l2 = l1.map(x => x.length);

console.log(l2);               // expected output: Array [8, 6, 7, 9]
