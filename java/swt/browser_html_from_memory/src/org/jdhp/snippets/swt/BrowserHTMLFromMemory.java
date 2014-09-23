package org.jdhp.snippets.swt;

import org.eclipse.swt.SWT;
import org.eclipse.swt.SWTError;
import org.eclipse.swt.browser.Browser;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Shell;


public class BrowserHTMLFromMemory {

    public static final String html = "<html><body>Hello !</body></html>";

    public static void main(String [] args) {
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
        browser.setText(html);

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
