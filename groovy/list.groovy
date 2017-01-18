#!/usr/bin/env groovy

// Usage: groovy list.groovy
//    or: ./list.groovy

// Init ///////////////////////////////////////////////////

l = [];
println l;

l = [1, 2, 3, 4, 5];
println l;


// Update /////////////////////////////////////////////////

l.add(6)      // Add at the end
println l;

l.add(0, -1)  // Add at the begining
println l;

i = 0;
l.remove(i);  // Remove the ith element

l2 = l.clone()
l2.clear()
println l2


// Size ///////////////////////////////////////////////////

println l.size()


// Get / Set //////////////////////////////////////////////

l[3] = 40;      // Set

println l[3];   // Get


// Visit //////////////////////////////////////////////////

// For loop
for(elem in l) {
    println "- $elem";
}


// Shuffle ////////////////////////////////////////////////

java.util.Collections.shuffle(l);
println l;
