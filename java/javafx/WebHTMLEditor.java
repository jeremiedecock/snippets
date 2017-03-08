import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.HTMLEditor;
import javafx.stage.Stage;

public class WebHTMLEditor extends Application {

    private final String HTML = "<html>" +
        "<body>" +
        "Hello!" +
        "</body>" +
        "</html>";

    public void start(Stage stage) {
        HTMLEditor browser = new HTMLEditor();
        browser.setHtmlText(HTML);

        Scene scene = new Scene(browser);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
