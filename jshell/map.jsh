//usr/bin/env jshell --execution local "$0" "$@"; exit $?

Map<Integer, String> map = new HashMap<>();

map.put(1, "one");
map.put(2, "two");
map.put(3, "three");
map.put(4, "four");
map.put(5, "five");

// Iterate over keys
for(Integer key : map.keySet()) {
    System.out.println(key);
}

// Iterate over values
for(String value : map.values()) {
    System.out.println(value);
}

// Iterate over entries (keys and values)
for(Map.Entry<Integer, String> entry : map.entrySet()) {
    Integer key = entry.getKey();
    String value = entry.getValue();
    System.out.println(key + " " + value);
}

/exit
