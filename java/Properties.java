import java.util.Enumeration;

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

        // Set the timezone property
        System.setProperty("timezone", "EsternStandardTime");
        
        // Get the timezone property
        String timezone = System.getProperty("timezone");
        System.out.println(timezone);
        
        // Get all properties
        java.util.Properties properties = System.getProperties();
        Enumeration propertyNames = properties.propertyNames();

        String key;

        while(propertyNames.hasMoreElements()) {
            key = (String) propertyNames.nextElement();
            System.out.println(key + " = " + properties.getProperty(key));
        }

    }
}
