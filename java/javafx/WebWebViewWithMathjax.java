import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class WebWebViewWithMathjax extends Application {

    // OFFLINE VERSION
    // Install MathJax on Debian: "aptitude install libjs-mathjax"
    //public static final String MATHJAX_URL = "/usr/share/javascript/mathjax/MathJax.js?config=TeX-AMS_HTML-full";
    
    // ONLINE VERSION
    public static final String MATHJAX_URL = "https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML-full";

    public static final String HTML = "<!DOCTYPE html>\n"
        + "<html>\n"
        + "<head>\n"
        + "    <meta charset=\"UTF-8\">\n"
        + "    <script type=\"text/x-mathjax-config\">\n"
        + "        MathJax.Hub.Config({\n"
        + "            tex2jax: {inlineMath: [[\"$\",\"$\"],[\"\\\\(\",\"\\\\)\"]]}\n"
        + "        });\n"
        + "    </script>\n"
        + "    <script type=\"text/javascript\" src='" + MATHJAX_URL  + "'></script>\n"
        + "</head>\n"
        + "<body>\n"
        + "    <p>\n"
        + "        When $a \\ne 0$, there are two solutions to \\(ax^2 + bx + c = 0\\) and they are\n"
        + "        $$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.$$\n"
        + "    </p>\n"
        + "</body>\n"
        + "</html>";

    public void start(Stage stage) {
        final WebView browser = new WebView();
        final WebEngine webEngine = browser.getEngine();

        webEngine.loadContent(HTML);

        Scene scene = new Scene(browser);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
