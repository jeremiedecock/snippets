import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class WebWebViewWithCSS extends Application {

    public static final String HTML = "<!DOCTYPE html>"
        + "<html>"
        + "<head>"
        + "    <meta charset=\"UTF-8\">"
        + "    <style type=\"text/css\">"
        + "* {color: #0f0;}"
        + "body {background-color: #f00;}"
        + "    </style>"
        + "</head>"
        + "<body>Hello !</body>"
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
