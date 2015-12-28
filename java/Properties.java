/*
 * This snippet show how to set and get properties.
 *
 * For more information, read "Le guide de survie Java" (chap. 2)
 * (by Timothy Fisher, ed. CampusPress)
 *
 * Usage:
 * - compile: javac Properties.java
 * - execute: java Properties
 */

public class Properties {
    public static void main(String [] args) {

        String timezone;
        
        // Get the timezone property
        timezone = System.getProperty("timezone");
        System.out.println(timezone);

        // Set the timezone property
        System.setProperty("timezone", "EsternStandardTime");
        
        // Get the timezone property
        timezone = System.getProperty("timezone");
        System.out.println(timezone);
    }
}
