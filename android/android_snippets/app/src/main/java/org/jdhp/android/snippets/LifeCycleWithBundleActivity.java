package org.jdhp.android.snippets;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

public class LifeCycleWithBundleActivity extends AppCompatActivity {

    // This tag will be used for logging
    private static final String TAG = MainActivity.class.getSimpleName();

    private static final String BUNDLE_INT_KEY = "data1";
    private static final String BUNDLE_STR_KEY = "data2";

    private int cptInt;
    private String cptStr;

    TextView tvData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_life_cycle_with_bundle);

        tvData = (TextView) findViewById(R.id.tv_life_cycle_with_bundle);

        Log.d(TAG, "Entering onCreate()");

        this.cptInt = 0;
        this.cptStr = "";

        // Restore or init data
        if(savedInstanceState != null) {
            if(savedInstanceState.containsKey(BUNDLE_INT_KEY)) {
                this.cptInt = savedInstanceState.getInt(BUNDLE_INT_KEY);
            }
            if(savedInstanceState.containsKey(BUNDLE_STR_KEY)) {
                this.cptStr = savedInstanceState.getString(BUNDLE_STR_KEY);
            }
        }

        displayData();
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        Log.d(TAG, "Entering onSaveInstanceState()");

        // Save data before the activity is stopped
        outState.putInt(BUNDLE_INT_KEY, this.cptInt);
        outState.putString(BUNDLE_STR_KEY, this.cptStr);
    }

    // MISC ////////////////////////////////////////////////////////////////////////////////////////

    public void incrementCpt(View view) {
        this.cptInt += 1;
        this.cptStr += ".";

        displayData();
    }

    public void displayData() {
        tvData.setText("cptInt=" + Integer.toString(this.cptInt) + "\ncptStr=" + this.cptStr);
    }

}
