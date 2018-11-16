
/*
 * Usage:
 * - compile: javac StaticInitializer.java
 * - execute: java  StaticInitializer
 */

import java.util.List;
import java.util.ArrayList;

public class StaticInitializer {

    public static List<String> LIST;

    //public StaticInitializer() {
    static {
        System.out.println("Init...");

        LIST = new ArrayList<String>();
        LIST.add("apple");
        LIST.add("banana");
        LIST.add("mango");
    }

    public static void main(String[] args) {
        //StaticInitializer foo1 = new StaticInitializer();
        //StaticInitializer foo2 = new StaticInitializer();

        for (String s : StaticInitializer.LIST)
            System.out.println(s);
    }
}
