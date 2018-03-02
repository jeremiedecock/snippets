package org.jdhp.snippets;

import org.apache.commons.math3.complex.Complex;

/*
 * This snippet tests complex numbers with the Apache Commons math3 library.
 *
 * Usage:
 * - compile: gradle build
 * - execute: gradle run
 */

public class ComplexNumbers {

    public static void main(String args[]) {
        Complex c = new Complex(2.0, 5.0);
         
        Complex c2 = c.pow(2);

        System.out.format("(%f + %fi)² = %f + %fi", c.getReal(), c.getImaginary(), c2.getReal(), c2.getImaginary());
    }
}
