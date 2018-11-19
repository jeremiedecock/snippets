/*
 * Usage:
 * - compile: javac Arrays.java
 * - execute: java  Arrays
 */

public class Arrays {
    public static void main(String[] args) {

        //int[] t = new int[3];   // OK
        //int t[] = new int[3];   // OK

        //int[] t = new int[3]{1, 2, 3};  // Error
        //int[] t = new int[]{1, 2, 3};   // OK
        //int t[] = new int[]{1, 2, 3};   // OK
        //int t[] = {1, 2, 3};            // OK
        int[] t = {1, 2, 3};              // OK

        System.out.println(t.length);
        System.out.println();

        for(int elem : t)
            System.out.println(elem);

        /*
        int t[][] = {{1, 2, 3}, {4, 5, 6}};                       // OK
        //int[][] t = {{1, 2, 3}, {4, 5, 6}};                     // OK
        //int t[][] = new int[][]{{1, 2, 3}, {4, 5, 6}};          // OK
        //int[][] t = new int[][]{{1, 2, 3}, {4, 5, 6}};          // OK

        for(int[] row : t)
            for(int elem : row)
                System.out.println(elem);
        */
    }
}
