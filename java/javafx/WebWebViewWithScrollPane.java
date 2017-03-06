import javafx.application.Application;
import javafx.scene.control.ScrollPane;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;

public class WebWebViewWithScrollPane extends Application {

    private final String HTML = "<html>" +
        "<body>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "Hello!<br>" +
        "</body>" +
        "</html>";

    public void start(Stage stage) {
        final WebView browser = new WebView();
        final WebEngine webEngine = browser.getEngine();

        webEngine.loadContent(HTML);

        ScrollPane scrollPane = new ScrollPane();
        scrollPane.getStyleClass().add("noborder-scroll-pane");
        scrollPane.setStyle("-fx-background-color: white");
        scrollPane.setContent(browser);
        scrollPane.setFitToWidth(true);
        scrollPane.setPrefHeight(180);

        Scene scene = new Scene(scrollPane);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
