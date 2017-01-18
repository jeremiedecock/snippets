#!/usr/bin/env groovy

// Usage: groovy random.groovy
//    or: ./random.groovy

// Random /////////////////////////////////////////////////

Random rand = new Random();

n = 10;
x = rand.nextInt(n);     // integer between 0 and n
println x

x = rand.nextInt();      // integer between -2^31 and 2^31-1
println x

x = rand.nextLong();     // integer between -2^63 and 2^63-1
println x

x = rand.nextFloat();    // float  [0.0 ; 1.0]
println x

x = rand.nextDouble();   // double [0.0 ; 1.0]
println x

x = rand.nextGaussian(); // parameters: mu=0.0 and sigma=1.0
println x

x = rand.nextBoolean();  // true ou false
println x


// Custom seed (time) /////////////////////////////////////

Random custom_rand = new Random(0);  // Here 0 is used as custom seed

x = custom_rand.nextInt();
println x


// Shuffle lists //////////////////////////////////////////

l = [1, 2, 3, 4, 5];
println l;

java.util.Collections.shuffle(l);
println l;
