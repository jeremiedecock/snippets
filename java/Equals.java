/*
 * Usage:
 * - compile: javac Equals.java
 * - execute: java  Equals
 */

public class Equals {
    public static void main(String[] args) {
        String s1 = new String("Hello");
        String s2 = new String("Hello");
    
        if(s1 == s2) {
            System.out.println("Adresse equals");
        } else {
            System.out.println("Adresse not equals");
        }

        if(s1.equals(s2)) {
            System.out.println("Value equals");
        } else {
            System.out.println("Value not equals");
        }
    }
}
