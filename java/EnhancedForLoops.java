/*
 * This snippet shows how to use enhanced for loops.
 *
 * For more information, read the following page
 * https://blogs.oracle.com/CoreJavaTechTips/entry/using_enhanced_for_loops_with
 *
 * Usage:
 * - compile: javac EnhancedForLoops.java
 * - execute: java EnhancedForLoops
 */

public class EnhancedForLoops {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		// 1D demo ////////////////////////////////////////////////////////////
		
		String[] table = new String[]{"one", "two", "three"};
		
		// for ( Type variable : Iterable ) {
		for (String elem : table) {
			System.out.println(elem);
		}
		
		// 2D demo ////////////////////////////////////////////////////////////
		
		int[][] tab = {{1, 2, 3}, {4, 5, 6}};

		for(int[] row : tab) {
			for(int elem : row) {
				System.out.println(elem);
			}
		}

	}

}
