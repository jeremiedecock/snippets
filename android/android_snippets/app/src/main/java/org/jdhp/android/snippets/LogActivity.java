package org.jdhp.android.snippets;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

public class LogActivity extends AppCompatActivity {

    /*
     * This tag will be used for logging. It is best practice to use the class's name using
     * getSimpleName as that will greatly help to identify the location from which your logs are
     * being posted.
     */
    private static final String LOG_TAG = LogActivity.class.getSimpleName();

    /*
     * Log levels (from the most severe to the less severe)
     * ====================================================
     *
     * ERROR: to log obvious errors
     * WARN: to log things that don't make the application crash but remain in concern (e.g. not enough disk space)
     * INFO: to log purely information messages (e.g. beeing connected to the internet)
     * ---
     * DEBUG: e.g. to output the URL a function is using or responce for web services
     * VERBOSE: ...
     *
     * DEBUG and VERBOSE messages are not kept in apps release versions.
     *
     * Log.x(String tag, String message);
     * - tag is usually the class name from where the log message is thrown (to make easier the search on the log console)
     * - message is the message to display on the log console
     * - x is either:
     *     - "e" for ERROR log messages
     *     - "w" for WARN log messages
     *     - "i" for INFO log messages
     *     - "d" for DEBUG log messages
     *     - "v" for VERBOSE log messages
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log);
    }

    public void makeLogMessages(View view) {
        String message = "Hello from ";

        Log.e(LOG_TAG, message + "ERROR");
        Log.w(LOG_TAG, message + "WARN");
        Log.i(LOG_TAG, message + "INFO");
        Log.d(LOG_TAG, message + "DEBUG");
        Log.v(LOG_TAG, message + "VERBOSE");

        String toastMessage = "Watch the \"Android Monitor\"!";
        Toast.makeText(this, toastMessage, Toast.LENGTH_SHORT).show();
    }
}
