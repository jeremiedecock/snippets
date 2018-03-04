//usr/bin/env jshell --execution local "$0" "$@"; exit $?

// Init ///////////////////////////////////////////////////

List<String> list = new ArrayList<String>();

list.add("un");
list.add("deux");
list.add("trois");

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

// Shuffle ////////////////////////////////////////////////

java.util.Collections.shuffle(list);

for(String val : list) {
    System.out.println(val);
}

/exit
