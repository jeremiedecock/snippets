/*
 * Usage:
 * - compile: javac Arrays.java
 * - execute: java  Arrays
 */

public class Arrays {
    public static void main(String[] args) {

		//int[] array = new int[3];   // OK
		//int array[] = new int[3];   // OK

        //int[] array = new int[3]{1, 2, 3};  // Error
        //int[] array = new int[]{1, 2, 3};   // OK
        //int array[] = new int[]{1, 2, 3};   // OK
        //int array[] = {1, 2, 3};   // OK
        int[] array = {1, 2, 3};   // OK
		
		for(int elem : array)
			System.out.println(elem);

    }
}
