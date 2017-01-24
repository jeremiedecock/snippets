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


public class BrowserHTMLWithMathJax {

    public static final String html = "<!DOCTYPE html>\n"
        + "<html>\n"
        + "<head>\n"
        + "    <meta charset=\"UTF-8\">\n"
        + "    <script type=\"text/x-mathjax-config\">\n"
        + "        MathJax.Hub.Config({\n"
        + "            tex2jax: {inlineMath: [[\"$\",\"$\"],[\"\\\\(\",\"\\\\)\"]]}\n"
        + "        });\n"
        + "    </script>\n"
        + "    <!-- Install MathJax on Debian: \"aptitude install libjs-mathjax\" -->\n"
        + "    <script type=\"text/javascript\" src='/usr/share/javascript/mathjax/MathJax.js?config=TeX-AMS_HTML-full'></script>\n"
        + "</head>\n"
        + "<body>\n"
        + "    <p>\n"
        + "        When $a \\ne 0$, there are two solutions to \\(ax^2 + bx + c = 0\\) and they are\n"
        + "        $$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.$$\n"
        + "    </p>\n"
        + "</body>\n"
        + "</html>";

    public static void main(String [] args) {
        // Display the HTML code
        System.out.println(html);

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
