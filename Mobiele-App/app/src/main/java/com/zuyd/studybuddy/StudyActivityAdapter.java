package com.zuyd.studybuddy;

import android.content.Context;
import android.content.DialogInterface;
import android.os.SystemClock;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AlertDialog;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Chronometer;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class StudyActivityAdapter extends RecyclerView.Adapter<StudyActivityAdapter.ViewHolder> {
    private List<StudyActivity> listStudyActivities;
    private Context context;
    private boolean[] fabEnabled;

    public void setHolder(ViewHolder holder) {
        this.holder = holder;
    }

    public ViewHolder getHolder() {
        return this.holder;
    }

    // study activity
    StudyActivity studyActivity;

    public void setStudyActivity(StudyActivity studyActivity) {
        this.studyActivity = studyActivity;
    }

    public StudyActivity getStudyActivity() {
        return this.studyActivity;
    }

    // stopwatch
    private ViewHolder holder;
    public static boolean timerRunning; // todo: why public?

    // list url central server
    Map<String, String> urlCentralServer = new HashMap<String, String>();

    // HTTP
    String stringJsonStudysession;
    private StringRequest stringRequest;
    private RequestQueue mRequestQueue;
    private static final String TAG = MainActivity.class.getName();
    private static final String REQUESTTAG = "string request first";

    // constructor
    public StudyActivityAdapter(List<StudyActivity> listStudyActivities, Context context, boolean[] fabEnabled) {
        this.listStudyActivities = listStudyActivities;
        this.context = context;
        this.fabEnabled = fabEnabled;

        // request queue
        mRequestQueue = Volley.newRequestQueue(context);

        urlCentralServer.put("GETAllStudyActivities", "http://ts.guydols.nl:5000/events?id=");
        urlCentralServer.put("GETToggleSession", "http://ts.guydols.nl:5000/toggle_session?id=");
        urlCentralServer.put("GETStopStudyActivity", "http://ts.guydols.nl:5000/stop_activity?id=");
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        timerRunning = false;
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.study_activity_card, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, final int position) {
        final StudyActivity studyActivity = listStudyActivities.get(position);

        // set textview attribute text-values
        holder.textViewStudyActivityTitle.setText(studyActivity.getTitle());
        holder.textViewStudyActivityModuleid.setText(studyActivity.getModuleid());
        holder.textViewStudyActivityDescription.setText(studyActivity.getDescription());
        holder.textViewStudyActivityDuration.setText("het zal " + studyActivity.getTime_est() + " minuten duren ");

        // start start button
        if ((studyActivity.getActivity_status()).equals("started")) {
            holder.buttonStopwatchToggle.setText("Pauze");
            holder.buttonStopwatchToggle.setBackgroundColor(0xff33b5e5);
            holder.chronometerSessionTime.setBase(SystemClock.elapsedRealtime() + holder.timeWhenStopped);
            holder.chronometerSessionTime.start();
        }

        // event handlers
        holder.buttonStopwatchToggle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /// Pause stopwatch
                if (!timerRunning) {
                    // start (new) session
                    toggleTimer(holder, studyActivity);
                } else if (timerRunning && holder == getHolder()) {
                    // pause running session
                    toggleTimer(holder, studyActivity);
                } else {
                    // show error
                    Snackbar snackbar = Snackbar.make(view, "Momenteel is er al een leeractiviteit actief", Snackbar.LENGTH_LONG);
                    snackbar.show();
                }
            }
        });

        holder.buttonStopwatchStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (studyActivity == getStudyActivity() && timerRunning) {
                    /// stop Stopwatch
                    holder.timeWhenStopped = holder.chronometerSessionTime.getBase() - SystemClock.elapsedRealtime();
                    stopTimerDialog(holder, studyActivity);

                    // reset holder value
                    setHolder(null);

                    // reset studyActivity
                    setStudyActivity(null);

                    // enable floating action bar
                    fabEnabled[0] = true;

                    // timerRunning
                    timerRunning = false;
                } else {
                    // show error
                    Snackbar snackbar = Snackbar.make(view, "Start dit leeractiviteit voordat je het wil stoppen", Snackbar.LENGTH_LONG);
                    snackbar.show();
                }
            }
        });
    }

    @Override
    public int getItemCount() {
        return listStudyActivities.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        // Study activity attributes
        public TextView textViewStudyActivityTitle;
        public TextView textViewStudyActivityModuleid;
        public TextView textViewStudyActivityDescription;
        public TextView textViewStudyActivityDuration;

        // Stopwatch UI
        public LinearLayout linearLayoutStopwatch;
        public Button buttonStopwatchToggle;
        public Button buttonStopwatchStop;

        // chronometer
        private Chronometer chronometerSessionTime;
        private long timeWhenStopped = 0;

        // constructor of Viewholder class
        public ViewHolder(View itemView) {
            super(itemView);

            // Study activity attributes:
            textViewStudyActivityTitle = (TextView) itemView.findViewById(R.id.textViewStudyActivityTitle);
            textViewStudyActivityModuleid = (TextView) itemView.findViewById(R.id.textViewStudyActivityModuleid);
            textViewStudyActivityDescription = (TextView) itemView.findViewById(R.id.textViewStudyActivityDescription);
            textViewStudyActivityDuration = (TextView) itemView.findViewById(R.id.textViewStudyActivityDuration);

            // Stopwatch UI
            linearLayoutStopwatch = (LinearLayout) itemView.findViewById(R.id.lineairLayoutStopwatch);
            chronometerSessionTime = (Chronometer) itemView.findViewById(R.id.chronometerSessionTime);
            buttonStopwatchToggle = (Button) itemView.findViewById(R.id.buttonStopwatchToggle);
            buttonStopwatchStop = (Button) itemView.findViewById(R.id.buttonStopwatchStop);
        }
    }

    //// chronometer logic
    /// toggle: start-pause
    private void toggleTimer(final ViewHolder holder, final StudyActivity studyActivity) {
        if ((holder.buttonStopwatchToggle.getText()).equals("Start") && !(holder.chronometerSessionTime.getText()).equals("00:00")) {
            startTimer(holder, studyActivity);
        } else if ((holder.buttonStopwatchToggle.getText()).equals("Start")) {
            startTimerDialog(holder, studyActivity);
        } else {
            pauseTimer(holder, studyActivity);
        }
    }

    /// dialogs
    // start timer dialog
    private void startTimerDialog(final ViewHolder holder, final StudyActivity studyActivity) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);

        // set builder attributes
        builder.setTitle("Leeractiviteit starten")
                .setMessage("Bij het starten van een leeractiviteit wordt het volgende opgenomen: \n* omgevingsgeluid, \n* kamertemperatuur, \n* luchtvochtigheid, \n* beeldmateriaal. ")
                .setPositiveButton("Starten", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        startTimer(holder, studyActivity);
                    }
                })
                .setNegativeButton("Annuleren", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // do nothing: exit alertdialog and return to the main window
                    }
                });

        // get and show the AlertDialog from create()
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }

    // stop timer dialog
    private void stopTimerDialog(final ViewHolder holder, final StudyActivity studyActivity) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);

        // set builder attributes
        builder.setTitle("Leeractiviteit stoppen")
                .setMessage("Weet je zeker dat je deze leeractiviteit wil stoppen?")
                .setPositiveButton("Ja", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        stopTimer(holder, studyActivity);
                    }
                })
                .setNegativeButton("Nee", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // do nothing: exit alertdialog and return to the main window; recording continues.
                    }
                });

        // get and show the AlertDialog from create()
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }

    /// timer logic
    // start timer
    private void startTimer(ViewHolder holder, StudyActivity studyActivity) {
        // disable create study activity button
        fabEnabled[0] = false;

        // set holder
        setHolder(holder);

        // timerRunning
        timerRunning = true;

        // study activity
        setStudyActivity(studyActivity);

        // GET-request: toggle session // todo: refactor -> first execute the GET-request, then on success run the timer
        httpRequest(urlCentralServer.get("GETToggleSession"), studyActivity);

        // start
        holder.buttonStopwatchToggle.setText("Pauze");
        holder.buttonStopwatchToggle.setBackgroundColor(0xff33b5e5);
        holder.chronometerSessionTime.setBase(SystemClock.elapsedRealtime() + holder.timeWhenStopped);
        holder.chronometerSessionTime.start();
    }

    // pause timer
    private void pauseTimer(final ViewHolder holder, StudyActivity studyActivity) {
        // timerRunning
        timerRunning = false;

        // GET-request: toggle session // todo: refactor -> first execute the GET-request, then on success run the timer
        httpRequest(urlCentralServer.get("GETToggleSession"), studyActivity);

        // stop
        holder.buttonStopwatchToggle.setText("Start");
        holder.buttonStopwatchToggle.setBackgroundColor(0xff40ff81);
        holder.timeWhenStopped = holder.chronometerSessionTime.getBase() - SystemClock.elapsedRealtime();
        holder.chronometerSessionTime.stop();
    }

    // stop timer
    private void stopTimer(ViewHolder holder, StudyActivity studyActivity) {
        // todo: refactor -> first execute the GET-request, then on success run the timer
        httpRequest(urlCentralServer.get("GETStopStudyActivity"), studyActivity);

        // timerRunning
        timerRunning = false;

        // reset chronometer
        holder.chronometerSessionTime.setBase(SystemClock.elapsedRealtime());
        holder.chronometerSessionTime.stop();
        holder.timeWhenStopped = 0;

        // reset view
        holder.buttonStopwatchToggle.setText("Start");
    }

    /// HTTP-Requests
    // uniformal http-request for start-pause-stop
    private void httpRequest(String url, StudyActivity studyActivity) {
        final String finalUrl = url + studyActivity.getId();

        stringRequest = new StringRequest
                (Request.Method.GET, finalUrl,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                Log.i(TAG, response); // todo: for testing purpose only
                                stringJsonStudysession = response;

                                // confirmation toasts
                                if (response.contains("completed")) {
                                    Toast.makeText((MainActivity) context, "De leeractiviteit is met succes afgerond", Toast.LENGTH_SHORT).show();

                                    /// refresh View when the stop button has been pressed
                                    ((MainActivity) context).getStudyActivities(urlCentralServer.get("GETAllStudyActivities"), context);
                                } else if(response.contains("started")) {
                                    Toast.makeText((MainActivity) context, "De leeractiviteit is gestart", Toast.LENGTH_SHORT).show();
                                } else if(response.contains("paused")) {
                                    Toast.makeText((MainActivity) context, "De leeractiviteit is gepauzeerd", Toast.LENGTH_SHORT).show();
                                }
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO Auto-generated method stub
                        Log.i(TAG, error.toString());

                        // error toast
                        Toast.makeText((MainActivity) context, "Er is iets mis gegaan, neem contact op met de docent (SA-HR-ER)", Toast.LENGTH_SHORT).show();
                    }
                });

        stringRequest.setTag(REQUESTTAG);
        mRequestQueue.add(stringRequest);
    }
}
