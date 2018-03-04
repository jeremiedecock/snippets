//usr/bin/env jshell --execution local "$0" "$@"; exit $?

// Init ///////////////////////////////////////////////////

List<String> list = new ArrayList<String>();

list.add("un");
list.add("deux");
list.add("trois");

// Init (alt) /////////////////////////////////////////////

// String[] tab = {"un", "deux", "trois"};
// List<String> list = Arrays.asList(tab);

// Update /////////////////////////////////////////////////

list.add("quatre");      // Add at the end

list.add("zero");        // Add at the begining

int i = 0;
list.remove(i);          // Remove the ith element

// Iterate ////////////////////////////////////////////////

for(String val : list) {
    System.out.println(val);
}

// Size ///////////////////////////////////////////////////

System.out.println(list.size());

// To string //////////////////////////////////////////////

System.out.println(list.toString());

// Shuffle ////////////////////////////////////////////////

java.util.Collections.shuffle(list);
System.out.println(list.toString());

// Sort ///////////////////////////////////////////////////

list.sort(null);
System.out.println(list.toString());

// Is empty ? /////////////////////////////////////////////

System.out.println("Is empty ? " + list.isEmpty());

// Clear //////////////////////////////////////////////////

list.clear();
System.out.println(list.toString());

/exit
