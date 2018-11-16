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

public class CollectionsSnippets {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		// List ///////////////////////////////////////////////////////////////
		
		// Make an empty list

		List<Integer> l3 = new ArrayList<Integer>();      // Ok -> without the "diamond operator"
		//List<Integer> l3 = new ArrayList<>();           // Ok -> with    the "diamond operator"
		//List<> l3 = new ArrayList<Integer>();           // Error: Incorrect number of arguments for type List<E>; it cannot be parameterized with arguments <>

		// Make and initialize a list (JDK9)

		//List<String> l4 = List.of("one", "two", "three");                   // WARNING: this makes an immutable list !
		List<String> l4 = new ArrayList<>(List.of("one", "two", "three"));    // Mutable list

		// Add elements in the list

        l4.add("four");
		
		for(String elem : l4) {
			System.out.println(elem);
		}
		System.out.println();

        System.out.println("Size: " +  l4.size());
		System.out.println("Empty: " + l4.isEmpty());
		System.out.println();
		
		// Map ////////////////////////////////////////////////////////////////
		
        Map<String, Integer> m = new HashMap<String, Integer>();

        m.put("One", 1);
        m.put("Two", 2);
        m.put("Three", 3);
		
		//for (int elem : m) {
		//	System.out.println(elem);
		//}

        System.out.println("Size: " + m.size());
        System.out.println("Empty: " + m.isEmpty());
	}

}
