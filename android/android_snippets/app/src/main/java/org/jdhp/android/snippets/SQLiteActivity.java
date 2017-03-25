package org.jdhp.android.snippets;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.util.Date;

/*
 * To drop the database, see:
 * - http://stackoverflow.com/questions/4406067/how-to-delete-sqlite-database-from-android-programmatically
 * - http://stackoverflow.com/questions/5326918/how-to-drop-database-in-sqlite
 * - http://stackoverflow.com/questions/3598452/database-delete-android
 *   When your in MainActivity
 *        this.deleteDatabase("mydata.db");
 *   or when you have a context handle elsewhere
 *        context.deleteDatabase("mydata.db");
 *   or
 *        adb shell
 *        su
 *        cd /data/data
 *        cd <your.application.java.package>
 *        cd databases
 *        rm <your db name>.db
 *
 * On MacOSX: adb is in /Users/${USER}/Library/Android/sdk/platform-tools/adb
 *
 * To access the db with sqlite client:
 *        adb shell
 *        su
 *        cd /data/data
 *        cd <your.application.java.package>
 *        cd databases
 *        sqlite3 <your db name>.db
 *
 *        Main commands are:
 *        - .help
 *        - .databases
 *        - .tables
 *        - .schema
 *        - .fullschema
 *        - .show
 *        - .dbinfo
 *
 */

public class SQLiteActivity extends AppCompatActivity {

    // This tag will be used for logging
    private static final String LOG_TAG = SQLiteActivity.class.getSimpleName();

    TextView tvData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sqlite);

        tvData = (TextView) findViewById(R.id.tv_persistant_data);

        updateTextView();
    }

    private void updateTextView() {
        tvData.setText("");

        DBHelper dbHelper = new DBHelper(this);
        SQLiteDatabase db = dbHelper.getWritableDatabase();

        Cursor cursor = db.query("TABLE1",
                new String[] {"COL1"},
                null, null, null, null, null);

        if(cursor.moveToFirst()) {
            do {
                String col1 = cursor.getString(0);
                tvData.append(col1 + "\n");
            } while (cursor.moveToNext());
        }

        db.close();
    }

    public void addNameInSQLite(View view) {
        Date now = new Date();
        Log.d(LOG_TAG, "Add " + now.toString());

        ContentValues cv = new ContentValues();
        cv.put("COL1", now.toString());

        DBHelper dbHelper = new DBHelper(this);
        SQLiteDatabase db = dbHelper.getWritableDatabase();

        db.insert("TABLE1", null, cv);
        //db.execSQL("insert into TABLE1 values (\"" + now.toString() + "\");");

        db.close();

        updateTextView();
    }

    public void clearNamesInSQLite(View view) {
        Log.d(LOG_TAG, "Clear the DB");

        DBHelper dbHelper = new DBHelper(this);
        SQLiteDatabase db = dbHelper.getWritableDatabase();

        db.execSQL("delete from TABLE1;");                                     // Remove all entries

        db.close();

        updateTextView();
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////

class DBHelper extends SQLiteOpenHelper {

    // This tag will be used for logging
    private static final String LOG_TAG = DBHelper.class.getSimpleName();

    private static final String DATABASE_NAME = "db1.db";
    private static final int DATABASE_VERSION = 1;

    public DBHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        Log.d(LOG_TAG, "Create the DB");

        db.execSQL("CREATE TABLE TABLE1 (COL1 TEXT PRIMARY KEY);");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int i, int i1) {
        Log.d(LOG_TAG, "Update the DB");

        db.execSQL("DROP TABLE IF EXISTS TABLE1;");
        onCreate(db);
    }
}