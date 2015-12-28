/*
 * compile: javac InitializedList.java
 * exec:    java InitializedList
 */

import java.util.ArrayList;
import java.util.Arrays;

public class InitializedList {

    public static void main(String[] args) {

        ArrayList<Integer> list = new ArrayList<Integer>(Arrays.asList(2, 3, 5));

        for(int val : list) {
            System.out.println(val);
        }
    }
}
