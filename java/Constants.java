/*
 * Usage:
 * - compile: javac Constants.java
 * - execute: java  Constants
 */

public class Constants {
    public static void main(String [] args) {
        
        final int x;
        x = 3;
        //x = 4;   // Error: The final local variable x may already have been assigned

        System.out.println(x);
    }
}
