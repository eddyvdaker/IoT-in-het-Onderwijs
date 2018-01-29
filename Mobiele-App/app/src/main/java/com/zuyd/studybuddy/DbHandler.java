//package com.zuyd.studybuddy;
//
//import android.database.sqlite.SQLiteDatabase;
//import android.database.sqlite.SQLiteOpenHelper;
//import android.database.Cursor;
//import android.content.Context;
//import android.content.ContentValues;
//
//import java.util.LinkedList;
//import java.util.List;
//
//public class DbHandler extends SQLiteOpenHelper {
//    private static final int DATABASE_VERSION = 1;
//    private static final String DATABASE_NAME = "studybuddy.db";
//    public static final String TABLE_LEARNINGACTIVITIES = "learningactivities";
//
//    // TABLE columns
//    public static final String COLUMN_ID = "id";
//    public static final String COLUMN_TITLE = "title";
//    public static final String COLUMN_DESCRIPTION = "description";
//    public static final String COLUMN_CREATIONTIMESTAMP = "creationTimestamp";
//    public static final String COLUMN_COMPLETIONTIMESTAMP = "completionTimestamp";
//    public static final String COLUMN_DURATION = "duration";
//    public static final String COLUMN_FOLDERLOCATION = "folderLocation";
//
//    // constructor
//    public DbHandler(Context context, String name, SQLiteDatabase.CursorFactory factory, int version) {
//        super(context, DATABASE_NAME, factory, DATABASE_VERSION);
//    }
//
//    /// db-methods
//    // creation of db
//    @Override
//    public void onCreate(SQLiteDatabase db) {
//        String query = "CREATE TABLE " + TABLE_LEARNINGACTIVITIES + "(" +
//                COLUMN_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
//                COLUMN_TITLE + " TEXT, " +
//                COLUMN_DESCRIPTION + " TEXT, " +
//                COLUMN_CREATIONTIMESTAMP + " TEXT, " +
//                COLUMN_COMPLETIONTIMESTAMP + " TEXT, " +
//                COLUMN_DURATION + " INTEGER, " +
//                COLUMN_FOLDERLOCATION + " TEXT" +
//                ");";
//        db.execSQL(query);
//    }
//
//    // Is only called when db exists but the stored version number is lower than requested in constructor.
//    @Override
//    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
//        // Increment the database version so that onUpgrade() is invoked. This method is used as data loss is not an issue, yet.
//        db.execSQL("DROP TABLE IF EXISTS " + TABLE_LEARNINGACTIVITIES);
//        onCreate(db);
//    }
//
//    /// CRUD
//    // CREATE: add new record to db
//    public void addLearningActivity(StudyActivity studyActivity) {
//        // init record values
//        ContentValues values = new ContentValues();
//
//        values.put(COLUMN_TITLE, studyActivity.getTitle());
//        values.put(COLUMN_DESCRIPTION, studyActivity.getDescription());
//        values.put(COLUMN_DURATION, studyActivity.getDuration());
//        values.put(COLUMN_CREATIONTIMESTAMP, studyActivity.getCreationTimestamp());
//        values.put(COLUMN_FOLDERLOCATION, studyActivity.getFolderLocation());
//
//        // get reference to writable DB
//        SQLiteDatabase db = getWritableDatabase();
//
//        // query
//        db.insert(TABLE_LEARNINGACTIVITIES, null, values);
//
//        // write to db
//        db.close();
//    }
//
//    // CREATE: add new multiple records to db
//    public void addLearningActivities(List<StudyActivity> learningActivities) {
//        // get reference to writable DB
//        SQLiteDatabase db = getWritableDatabase();
//
//        // init record values
//        for(int i=0; i < learningActivities.size(); i++) {
//            ContentValues values = new ContentValues();
//
//            values.put(COLUMN_TITLE, learningActivities.get(i).getTitle());
//            values.put(COLUMN_DESCRIPTION, learningActivities.get(i).getDescription());
//            values.put(COLUMN_DURATION, learningActivities.get(i).getDuration());
//            values.put(COLUMN_CREATIONTIMESTAMP, learningActivities.get(i).getCreationTimestamp());
//            values.put(COLUMN_FOLDERLOCATION, learningActivities.get(i).getFolderLocation());
//
//            // query
//            db.insert(TABLE_LEARNINGACTIVITIES, null, values);
//        }
//
//        // write to db
//        db.close();
//    }
//
//    // READ: read all uncompleted records from db
//    public List<StudyActivity> getAllLearningActivities() {
//        List<StudyActivity> learningActivities = new LinkedList<StudyActivity>();
//
//        // query
//        String query = "SELECT * FROM " + TABLE_LEARNINGACTIVITIES + " WHERE " + COLUMN_COMPLETIONTIMESTAMP + " IS NULL";
//
//        // get reference to writable DB
//        SQLiteDatabase db = getWritableDatabase();
//        Cursor cursor = db.rawQuery(query, null);
//
//        // todo: sort by creationTime?
//
//        // go over each row, build learning activity and add it to list
//        StudyActivity studyActivity = null;
//        if (cursor.moveToFirst()) {
//            do {
//                studyActivity = new StudyActivity();
//
//                // set object variables //todo: refactor
//                studyActivity.setId(cursor.getInt(0));
//                studyActivity.setTitle(cursor.getString(1));
//                studyActivity.setDescription(cursor.getString(2));
//                studyActivity.setCreationTimestamp(cursor.getString(3));
//                studyActivity.setCompletionTimestamp(cursor.getString(4));
//                studyActivity.setDuration(cursor.getInt(5));
//                studyActivity.setFolderLocation(cursor.getString(6));
//
//                // add studyActivity to learningActivities
//                learningActivities.add(studyActivity);
//            } while (cursor.moveToNext());
//        }
//
//        return learningActivities;
//    }
//
//    // todo: READ: read one specific uncompleted record from db
//    public StudyActivity getLearningActivity(int id) {
//        // get reference to writable DB
//        SQLiteDatabase db = getReadableDatabase();
//
//        // query
//        String query = "SELECT * FROM " + TABLE_LEARNINGACTIVITIES + " WHERE " + COLUMN_ID + " IS " + id;
//        Cursor cursor = db.rawQuery(query, null);
//
//        // if we got results, get the first one
//        if (cursor != null) {
//            cursor.moveToFirst();
//        }
//
//        // build StudyActivity-object //todo: refactor
//        StudyActivity studyActivity = new StudyActivity();
//        studyActivity.setId(cursor.getInt(0));
//        studyActivity.setTitle(cursor.getString(1));
//        studyActivity.setDescription(cursor.getString(2));
//        studyActivity.setCreationTimestamp(cursor.getString(3));
//        studyActivity.setCompletionTimestamp(cursor.getString(4));
//        studyActivity.setDuration(cursor.getInt(5));
//        studyActivity.setFolderLocation(cursor.getString(6));
//
//        return studyActivity;
//    }
//
//    // UPDATE: update a record from db
//    public void updateLearningActivity(StudyActivity studyActivity) {
//        // get reference to writable db
//        SQLiteDatabase db = this.getWritableDatabase();
//
//        // create ContentValues to add key "column"/value
//        ContentValues values = new ContentValues();
//        values.put(COLUMN_TITLE, studyActivity.getTitle());
//        values.put(COLUMN_DESCRIPTION, studyActivity.getDescription());
//        values.put(COLUMN_DURATION, studyActivity.getDuration());
//        values.put(COLUMN_CREATIONTIMESTAMP, studyActivity.getCreationTimestamp());
//        values.put(COLUMN_FOLDERLOCATION, studyActivity.getFolderLocation());
//
//        // update record
//        int i = db.update(
//                TABLE_LEARNINGACTIVITIES,
//                values,
//                COLUMN_ID + " = ?",
//                new String[] {String.valueOf(studyActivity.getId())}
//        );
//
//        //  write to db
//        db.close();
//    }
//
//    // todo: UPDATE: update record from db -> COLUMN_COMPLETIONTIMESTAMP
//
//    // DELETE: delete new record from db
//    public void deleteLearningActivity(int id) {
//        SQLiteDatabase db = getWritableDatabase();
//        db.delete(TABLE_LEARNINGACTIVITIES, COLUMN_ID + "=" + id, null);
//
//        // write to db
//        db.close();
//    }
//}
