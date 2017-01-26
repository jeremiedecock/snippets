/*
 * Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)
 */

import org.eclipse.swt.SWT;
import org.eclipse.swt.SWTError;
import org.eclipse.swt.browser.Browser;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Shell;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.FileNotFoundException;


public class BrowserHTMLWithMathJaxFromFile {

    final public static String HTML = BrowserHTMLWithMathJaxFromFile.loadHtmlFile("mathjax_demo.html");

    private static String loadHtmlFile(String source) {
        StringBuffer html = new StringBuffer();
        
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(BrowserHTMLWithMathJaxFromFile.class.getResourceAsStream(source)));
            
            String line;
            do {
                line = reader.readLine();
                if(line != null) {
                    html.append(line);
                }
            } while(line != null);
        } catch(FileNotFoundException e) {
            System.out.println(e);
        } catch(IOException e) {
            System.out.println(e);
        }
        
        return html.toString();
    }


    public static void main(String [] args) {

        // SWT
        Display display = new Display();

        // Make the window
        Shell shell = new Shell(display);
        shell.setLayout(new GridLayout(1, false));

        // Add a widget
        Browser browser;
        try {
            //browser = new Browser(shell, SWT.NONE);       // default
            //browser = new Browser(shell, SWT.MOZILLA);  // force mozilla
            browser = new Browser(shell, SWT.WEBKIT);   // force webkit
        } catch (SWTError e) {
            System.out.println("Could not instantiate Browser: " + e.getMessage());
            display.dispose();
            return;
        }
        browser.setLayoutData(new GridData(GridData.FILL_BOTH));
        browser.setText(HTML);

        // Render the window
        shell.open();

        while(!shell.isDisposed()) {
            if(!display.readAndDispatch()) {
                display.sleep();
            }
        }

        display.dispose();
    }
}
