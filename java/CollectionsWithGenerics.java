/*
 *
 * Usage:
 * - compile: javac CollectionsSnippets.java
 * - execute: java CollectionsSnippets
 */

import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

public class CollectionsWithGenerics {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		// Without generics /////////////////////

		List l1 = new ArrayList();

		l1.add(1);
        l1.add(2);
        l1.add(3);
		
		//for(int elem : l1) System.out.println(elem);        // Error: Type mismatch: cannot convert from element type Object to int
		//for(Integer elem : l1) System.out.println(elem);    // Error: Type mismatch: cannot convert from element type Object to int
		for(Object elem : l1) System.out.println(elem);       // Ok : l1 contains instances of the "Object" class => elements have to be casted to be used as Integers...

		System.out.println();

		// With generics ////////////////////////

		//List<Integer> l2 = new ArrayList<Integer>();   // OK : don't use the "diamond operator" to automatically retrieve the generic type
		List<Integer> l2 = new ArrayList<>();            // OK : use the "diamond operator" to automatically retrieve the generic type

		l2.add(1);
        l2.add(2);
        l2.add(3);
		
		for(int elem : l2) System.out.println(elem);          // l2 contains instances of the "Integer" class (instead of "Object")

		System.out.println();

	}

}
