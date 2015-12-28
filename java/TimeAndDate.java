/*
 * This snippet uses some useful Time and Date functions.
 *
 * Usage:
 * - compile: javac TimeAndDate.java
 * - execute: java TimeAndDate
 */

public class TimeAndDate {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		System.out.println( System.currentTimeMillis() ); // returns a long
		System.out.println( System.nanoTime() );          // returns a long

	}

}
