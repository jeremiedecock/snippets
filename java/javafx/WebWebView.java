import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class WebWebView extends Application {

    private final String HTML = "<html>" +
        "<body>" +
        "Hello!" +
        "</body>" +
        "</html>";

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
