import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class WebWebViewWithJS extends Application {

    public static final String HTML = "<!DOCTYPE html>\n"
        + "<html>\n"
        + "<head>\n"
        + "    <meta charset=\"UTF-8\">\n"
        + "</head>\n"
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
