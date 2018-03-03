//usr/bin/env jshell --execution local "$0" "$@"; exit $?

List<String> list = new ArrayList<String>();

list.add("un");
list.add("deux");
list.add("trois");

for(String val : list) {
    System.out.println(val);
}

/exit
