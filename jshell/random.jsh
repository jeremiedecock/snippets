//usr/bin/env jshell --execution local "$0" "$@"; exit $?

// Random /////////////////////////////////////////////////

Random rand = new Random();

int n = 10;
int x = rand.nextInt(n);         // integer between 0 and n
System.out.println(x);

int x = rand.nextInt();          // integer between -2^31 and 2^31-1
System.out.println(x);

long x = rand.nextLong();        // integer between -2^63 and 2^63-1
System.out.println(x);

float x = rand.nextFloat();      // float  [0.0 ; 1.0]
System.out.println(x);

double x = rand.nextDouble();    // double [0.0 ; 1.0]
System.out.println(x);

double x = rand.nextGaussian();  // parameters: mu=0.0 and sigma=1.0
System.out.println(x);

boolean x = rand.nextBoolean();  // true ou false
System.out.println(x);


// Custom seed (time) /////////////////////////////////////

Random custom_rand = new Random(0);  // Here 0 is used as custom seed

int x = custom_rand.nextInt();
System.out.println(x);


// Shuffle lists //////////////////////////////////////////

List<Integer> list = new ArrayList<Integer>();
list.add(1);
list.add(2);
list.add(3);
list.add(4);
for(Integer val : list) {
    System.out.println(val);
}

java.util.Collections.shuffle(list);
for(Integer val : list) {
    System.out.println(val);
}

/exit
