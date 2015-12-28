/*
 * This snippet show how shuffle a list
 *
 * compile: javac RandomShuffleList.java
 * exec:    java RandomShuffleList
 */

import java.util.ArrayList;
import java.util.Arrays;

public class RandomShuffleList {

    public static void main(String[] args) {

        // Build the initial list
        ArrayList<Integer> list = new ArrayList<Integer>(Arrays.asList(1, 2, 3, 4, 5));

        // Shuffle the list
        java.util.Collections.shuffle(list);

        // Show the list
        for(int val : list) {
            System.out.println(val);
        }

    }
}
