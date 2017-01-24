import org.eclipse.swt.SWT;
import org.eclipse.swt.SWTError;
import org.eclipse.swt.browser.Browser;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Shell;


public class BrowserHTMLWithJS {

    public static final String html = "<!DOCTYPE html>\n"
        + "<html>\n"
        + "<head>\n"
        + "    <meta charset=\"UTF-8\">\n"
        + "<head>\n"
        + "<body>\n"
        + "<div id=\"clock\"></div>\n"
        + "<script>\n"
        + "function display_clock() {\n"
        + "    var now = new Date();\n"
        + "    var elem = document.getElementById(\"clock\");\n"
        + "    if(elem) {\n"
        + "        elem.innerHTML = now.toLocaleTimeString();\n"
        + "    }\n"
        + "    setTimeout(display_clock, 1000);\n"
        + "}\n"
        + "window.onload = function() {\n"
        + "    display_clock();\n"
        + "}\n"
        + "</script>\n"
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
