package com.zuyd.studybuddy;

import android.content.Context;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    private FloatingActionButton fab;
    private boolean[] fabEnabled;

    private RecyclerView recyclerView;
    public RecyclerView.Adapter adapter;

    private List<StudyActivity> listStudyActivities;

    // list url central server
    Map<String, String> urlCentralServer = new HashMap<String, String>();

    // connection
    private ConnectivityManager connectivityManager;
    private NetworkInfo activeNetwork;
    private boolean isConnected;

    // REST-handler
    String stringJsonStudyActivities;

    private int studentId;

    // RequestQueue
    private RequestQueue mRequestQueue;
    private StringRequest stringRequest;
    private static final String TAG = MainActivity.class.getName();
    private static final String REQUESTTAG = "string request first";

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // Floating Action button
        fab = (FloatingActionButton) findViewById(R.id.fab);
        this.fabEnabled = new boolean[1];
        this.fabEnabled[0] = true;

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (fabEnabled[0]) {
                    onCreateStudyActivityDialog();
                } else {
                    Snackbar snackbar = Snackbar.make(view, "Stop de leeractiviteit voordat je een ander wil toevoegen", Snackbar.LENGTH_LONG);
                    snackbar.show();
                }
            }
        });

        /// recyclerview
        recyclerView = (RecyclerView) findViewById(R.id.recyclerView);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // studentid
        studentId = 1; // todo: get studentid from local file

        // set URL central server
        urlCentralServer.put("GETAllStudyActivities", "http://ts.guydols.nl:5000/events?id=");
        urlCentralServer.put("POSTNewStudyActivity", "http://ts.guydols.nl:5000/event");

        // get connection status info
        connectivityManager = (ConnectivityManager) this.getSystemService(this.CONNECTIVITY_SERVICE);
        connectivityManager.getActiveNetworkInfo();
        activeNetwork = connectivityManager.getActiveNetworkInfo();
        isConnected = activeNetwork != null && activeNetwork.isConnectedOrConnecting();

        // request queue
        mRequestQueue = Volley.newRequestQueue(this);

        if (isConnected) {
            getStudyActivities(urlCentralServer.get("GETAllStudyActivities"), this);
        } else {
            Toast.makeText(MainActivity.this, "Er is geen internetverbinding. Herstart de app.", Toast.LENGTH_LONG).show();
        }
    }

    // Overrides
    @Override
    protected void onStop() {
        super.onStop();
        if (mRequestQueue != null) {
            mRequestQueue.cancelAll(REQUESTTAG);
        }
    }

    /// Dialogs
    // create study activity dialog
    public void onCreateStudyActivityDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);

        // get the layout inflater
        LayoutInflater inflater = MainActivity.this.getLayoutInflater();

        // inflate and set the layout for the dialog
        // pass null as the parent view because it's going in the dialog layout
        builder.setView(inflater.inflate(R.layout.study_activity_dialog, null))
                .setTitle("Leeractiviteit aanmaken")
                .setPositiveButton("Aanmaken", null)
                .setNegativeButton("Annuleren", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // do nothing: exit alertdialog and return to the main window
                    }
                });

        // create the dialog
        final AlertDialog alertDialog = builder.create();

        // create custom PositiveButton with fields correction
        alertDialog.setOnShowListener(new DialogInterface.OnShowListener() {
            @Override
            public void onShow(DialogInterface dialogInterface) {

                Button button = ((AlertDialog) alertDialog).getButton(AlertDialog.BUTTON_POSITIVE);
                button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        // EditTexts of dialog
                        EditText editText_dialog_name = (EditText) ((AlertDialog) alertDialog).findViewById(R.id.editText_dialog_name);
                        EditText editText_dialog_description = (EditText) ((AlertDialog) alertDialog).findViewById(R.id.editText_dialog_description);
                        EditText editText_dialog_duration = (EditText) ((AlertDialog) alertDialog).findViewById(R.id.editText_dialog_duration);
                        EditText editText_dialog_moduleid = (EditText) ((AlertDialog) alertDialog).findViewById(R.id.editText_dialog_moduleid);
                        EditText editText_dialog_teacherid = (EditText) ((AlertDialog) alertDialog).findViewById(R.id.editText_dialog_teacherid);

                        // error checking
                        boolean filledDialog = true;
                        if (editText_dialog_name.getText().toString().length() == 0) {
                            filledDialog = false;
                            editText_dialog_name.setError("Dit veld is niet ingevuld");
                        }
                        if(editText_dialog_description.getText().toString().length() == 0) {
                            filledDialog = false;
                            editText_dialog_description.setError("Dit veld is niet ingevuld");
                        }
                        if(editText_dialog_duration.getText().toString().length() == 0) {
                            filledDialog = false;
                            editText_dialog_duration.setError("Dit veld is niet ingevuld");
                        }
                        if (editText_dialog_moduleid.getText().toString().length() == 0) {
                            filledDialog = false;
                            editText_dialog_moduleid.setError("Dit veld is niet ingevuld");
                        }
                        if(editText_dialog_teacherid.getText().toString().length() == 0) {
                            filledDialog = false;
                            editText_dialog_teacherid.setError("Dit veld is niet ingevuld");
                        }

                        // create StudyActivity-object
                        if (filledDialog) {
                            StudyActivity studyActivity = new StudyActivity();

                            // essential attributes
                            studyActivity.setStudentid(studentId);
                            studyActivity.setModuleid(editText_dialog_moduleid.getText().toString());
                            studyActivity.setTitle(editText_dialog_name.getText().toString());

                            String teacherid = editText_dialog_teacherid.getText().toString();

                            // optional attributes
                            studyActivity.setDescription(editText_dialog_description.getText().toString());
                            studyActivity.setTime_est(editText_dialog_duration.getText().toString());

                            // save StudyActivity-object in external database
                            createStudyActivity(urlCentralServer.get("POSTNewStudyActivity"), studyActivity, teacherid);

                            // dismiss dialog
                            alertDialog.dismiss();
                        }
                    }
                });
            }
        });

        // show the AlertDialog
        alertDialog.show();
    }

    /// HTTP-Requests
    // get study activities
    public void getStudyActivities(String url, final Context context) {
        final Context contextAdapter = context;
        String finalUrl = url + studentId;

        listStudyActivities = new LinkedList<StudyActivity>();
        stringRequest = new StringRequest
                (Request.Method.GET, finalUrl,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                Log.i(TAG, response);
                                stringJsonStudyActivities = response;

                                // create list study Activities
                                try {
                                    JSONObject jsonObject = new JSONObject(response);
                                    JSONArray jsonArray = jsonObject.getJSONArray("events");
                                    int jsonArrayLength = jsonArray.length();

                                    // morph json-object into workable StudyActivity object
                                    for (int i = 0; i < jsonArrayLength; i++) {
                                        // create, init, and add studyActivity object to studyActivities List
                                        Gson gson = new Gson();
                                        StudyActivity studyActivity = gson.fromJson(jsonArray.get(i).toString(), StudyActivity.class);

                                        if (!(studyActivity.getActivity_status()).equals("completed")) {
                                            listStudyActivities.add(studyActivity);
                                        }
                                    }

                                    // geen openstaande leeractiviteiten
                                    if (listStudyActivities.isEmpty()) {
                                        Toast.makeText(MainActivity.this, "Momenteel zijn er geen openstaande leeractiviteiten", Toast.LENGTH_SHORT).show();
                                    }
                                } catch (JSONException e) {
                                    Log.i(TAG, "JSONException has been catched");

                                    // error toast
                                    Toast.makeText(MainActivity.this, "Er is iets mis gegaan, neem contact op met de docent (MA-GS-JE)", Toast.LENGTH_LONG).show();
                                }

                                adapter = new StudyActivityAdapter(listStudyActivities, contextAdapter, fabEnabled);
                                recyclerView.setAdapter(adapter);
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.i(TAG, "VolleyError " + error.toString());

                        // error toast
                        Toast.makeText(MainActivity.this, "Er is iets mis gegaan, neem contact op met de docent (MA-GS-ER)", Toast.LENGTH_LONG).show();
                    }
                });

        stringRequest.setTag(REQUESTTAG);

        mRequestQueue.add(stringRequest);
    }

    // create study activity
    private void createStudyActivity(String url, StudyActivity studyActivity, String teacherid) {
        // form study Activity to json string
        Gson gson = new Gson();
        final String jsonStudyActivity = gson.toJson(studyActivity)
                .replaceAll("\"teacherid\":-1", "\"teacherid\":\"" + teacherid + "\"") // set teacherid with a string variable
                .replaceAll("\"id\":-1,", "") // delete id
                .replaceAll("\"activity_status\":\"\",", "") // delete activity_status
                .replaceAll(":-1", "\"\""); // replace all -1 values with a ""-value

        StringRequest stringRequest = new StringRequest
                (Request.Method.POST, url, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response", response);
                        // confirmation toast
                        Toast.makeText(MainActivity.this, "De leeractiviteit is met succes aangemaakt", Toast.LENGTH_SHORT).show();

                        // refresh view
                        getStudyActivities(urlCentralServer.get("GETAllStudyActivities"), MainActivity.this);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.i(TAG, error.toString());
                        // error toast
                        Toast.makeText(MainActivity.this, "Er is iets mis gegaan, neem contact op met de docent (MA-CS-ER)", Toast.LENGTH_LONG).show();
                    }
                }) {
            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";
            }

            @Override
            public byte[] getBody() {
                try {
                    return jsonStudyActivity == null ? null : jsonStudyActivity.getBytes("utf-8");
                } catch (UnsupportedEncodingException uee) {
                    Log.i(TAG, "Unsupported Encoding while trying to get the bytes of " + jsonStudyActivity + " using utf-8");

                    // error toast
                    Toast.makeText(MainActivity.this, "Er is iets mis gegaan, neem contact op met de docent (MA-CS-UE)", Toast.LENGTH_LONG).show();
                    return null;
                }
            }
        };

        // POST-request to server using volley
        stringRequest.setTag(REQUESTTAG);
        mRequestQueue.add(stringRequest);
    }
}
