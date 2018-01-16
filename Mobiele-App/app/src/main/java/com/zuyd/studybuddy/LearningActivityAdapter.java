package com.zuyd.studybuddy;

import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.CountDownTimer;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AlertDialog;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.List;
import java.util.Locale;

public class LearningActivityAdapter extends RecyclerView.Adapter<LearningActivityAdapter.ViewHolder> {
    private List<LearningActivity> listLearningActivities;
    private Context context;
    private DbHandler dbHandler;
    private boolean[] fabEnabled;

    public void setHolder(ViewHolder holder) {
        this.holder = holder;
    }

    // stopwatch
    private ViewHolder holder;
    private long timeLeftInMillis;

    public boolean isTimerRunning() {
        return timerRunning;
    }

    public static boolean timerRunning;
    private TextView textViewStopwatchCountDown;
    private CountDownTimer countDownTimer;

    // constructor
    public LearningActivityAdapter(List<LearningActivity> listLearningActivities, Context context, DbHandler dbHandler, boolean[] fabEnabled) {
        this.listLearningActivities = listLearningActivities;
        this.context = context;
        this.dbHandler = dbHandler;
        this.fabEnabled = fabEnabled;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        timerRunning = false;
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.learning_activity_card, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, final int position) {
        final LearningActivity learningActivity = listLearningActivities.get(position);

        // get Title
        holder.textViewTitle.setText(learningActivity.getTitle());

        // event handlers
        holder.imageButtonDelete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (!timerRunning) {
                    dbHandler.deleteLearningActivity(learningActivity.getId());

                    // refresh view
                    listLearningActivities.remove(listLearningActivities.get(position));
                    notifyDataSetChanged();
                } else {
                    Snackbar snackbar = Snackbar.make(view, "Stop de leeractiviteit voordat je een wijziging wil aanbrengen", Snackbar.LENGTH_LONG);
                    snackbar.show();
                }
            }
        });

        holder.imageButtonStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // 1. Wait for connection with server --> HTTP-request: send POST; send id&Title -> when respond 202 'OK': save status in sqlite db: runningLearningActivities.
                // 2. Show linearLayoutStopwatch, get duration of appropriate learningActivity-object & textViewStopwatchTime.setText()

                if (!timerRunning) {
                    setHolder(holder);
                    holder.linearLayoutStopwatch.setVisibility(View.VISIBLE);
                    holder.textViewStopwatchTime.setText((Integer.toString(learningActivity.getDuration())) + ":00");

                    //
                    fabEnabled[0] = false;

                    // 3. Countdown
                    timeLeftInMillis = learningActivity.getDuration() * 60000;
                    startTimer(timeLeftInMillis, holder.textViewStopwatchTime);

                    // 4. todo: disable the holders until the endtime has elapsed.

                    // code here
                    // todo: get id -> http-request
                    // todo: show stopwatch UI dialog
                } else {
                    Snackbar snackbar = Snackbar.make(view, "Momenteel is er al een leeractiviteit actief", Snackbar.LENGTH_LONG);
                    snackbar.show();
                }
            }
        });

        holder.buttonStopwatchPause.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Pause stopwatch
                pauseTimer();
            }
        });

        holder.buttonStopwatchStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // stop Stopwatch
                stopTimer();

                // enable floating action bar
                fabEnabled[0] = true;
            }
        });

        holder.textViewTitle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!timerRunning) {
                    onCreateLearningActivityDialog(context, learningActivity);
                } else {
                    Snackbar snackbar = Snackbar.make(view, "Stop de leeractiviteit voordat je een wijziging wil aanbrengen", Snackbar.LENGTH_LONG);
                    snackbar.show();
                }
            }
        });

        holder.buttonStopwatchExtend.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                // Extend stopwatch time by 5 minutes
                timeLeftInMillis += 5 * 60000;
                countDownTimer.cancel();
                startTimer(timeLeftInMillis, holder.textViewStopwatchTime);
            }
        });
    }

    @Override
    public int getItemCount() {
        return listLearningActivities.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public ImageButton imageButtonDelete;
        public ImageButton imageButtonStart;
        public TextView textViewTitle;

        // Stopwatch UI
        public LinearLayout linearLayoutStopwatch;
        public TextView textViewStopwatchTime;
        public Button buttonStopwatchPause;
        public Button buttonStopwatchExtend;
        public Button buttonStopwatchStop;

        // constructor
        public ViewHolder(View itemView) {
            super(itemView);

            imageButtonDelete = (ImageButton) itemView.findViewById(R.id.imageButtonDelete);
            imageButtonStart = (ImageButton) itemView.findViewById(R.id.imageButtonStart);
            textViewTitle = (TextView) itemView.findViewById(R.id.textViewTitle);

            // Stopwatch UI
            linearLayoutStopwatch = (LinearLayout) itemView.findViewById(R.id.lineairLayoutStopwatch);
            textViewStopwatchTime = (TextView) itemView.findViewById(R.id.textViewStopwatchTime);
            buttonStopwatchPause = (Button) itemView.findViewById(R.id.buttonStopwatchPause);
            buttonStopwatchExtend = (Button) itemView.findViewById(R.id.buttonStopwatchExtend);
            buttonStopwatchStop = (Button) itemView.findViewById(R.id.buttonStopwatchStop);
        }
    }

    // Stopwatch
    public void startTimer(long timeLeftInMillis, TextView textViewStopwatchTime) {
        this.setTextViewStopwatchCountDown(textViewStopwatchTime);
        timerRunning = true;

        countDownTimer = new CountDownTimer(timeLeftInMillis, 1000) {
            @Override
            public void onTick(long millisUntilFinished) {
                setTimeLeftInMillis(millisUntilFinished);
                updateCountDownText(millisUntilFinished);
            }

            @Override
            public void onFinish() {
                // todo: notify: push,vibrate, ??
                stopTimer();
            }
        }.start();
    }

    private void pauseTimer( ) {
        if ((holder.buttonStopwatchPause.getText()).equals("Pauze")) {
            // save timer state

            holder.buttonStopwatchPause.setText("Hervat");
            countDownTimer.cancel();
        } else {
            // start
            holder.buttonStopwatchPause.setText("Pauze");
            countDownTimer.cancel();
            startTimer(timeLeftInMillis, holder.textViewStopwatchTime);
        }
    }

    private void stopTimer() {
        countDownTimer.cancel();
        timerRunning = false;

        holder.buttonStopwatchPause.setText("Pauze");
        holder.linearLayoutStopwatch.setVisibility(View.GONE);
        // todo: then gather data & show message what to do next.

        /// todo: gather data
        // todo: http-request
    }

    public void setTimeLeftInMillis(long timeLeftInMillis) {
        this.timeLeftInMillis = timeLeftInMillis;
    }

    public void setTextViewStopwatchCountDown(TextView textViewStopwatchCountDown) {
        this.textViewStopwatchCountDown = textViewStopwatchCountDown;
    }

    private void updateCountDownText(double timeLeftInMillis) {
        int minutes = (int) (timeLeftInMillis / 1000) / 60;
        int seconds = (int) (timeLeftInMillis / 1000) % 60;

        String timeLeftFormatted = String.format(Locale.getDefault(), "%02d:%02d", minutes, seconds);
        textViewStopwatchCountDown.setText(timeLeftFormatted);
    }

    // Edit learning activity
    public void onCreateLearningActivityDialog(Context context, final LearningActivity learningActivity) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);

        // get the layout inflater
        LayoutInflater inflater = LayoutInflater.from(context);

        // inflate and set the layout for the dialog
        // pass null as the parent view because it's going in the dialog layout
        View viewLearningActivityDialog = inflater.inflate(R.layout.learning_activity_dialog, null);

        // EditTexts of dialog
        EditText editText_dialog_name = (EditText) ((View) viewLearningActivityDialog).findViewById(R.id.editText_dialog_name);
        EditText editText_dialog_description = (EditText) ((View) viewLearningActivityDialog).findViewById(R.id.editText_dialog_description);
        EditText editText_dialog_duration = (EditText) ((View) viewLearningActivityDialog).findViewById(R.id.editText_dialog_duration);

        // fill view elements
        editText_dialog_name.setText(learningActivity.getTitle());
        editText_dialog_description.setText(learningActivity.getDescription());
        editText_dialog_duration.setText(Integer.toString(learningActivity.getDuration()));

        builder.setView(viewLearningActivityDialog);
        builder.setTitle("Leeractiviteit bewerken")
                // Add action buttons
                .setPositiveButton("Opslaan", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // EditTexts of dialog
                        EditText editText_dialog_name = (EditText) ((AlertDialog) dialog).findViewById(R.id.editText_dialog_name);
                        EditText editText_dialog_description = (EditText) ((AlertDialog) dialog).findViewById(R.id.editText_dialog_description);
                        EditText editText_dialog_duration = (EditText) ((AlertDialog) dialog).findViewById(R.id.editText_dialog_duration);

                        // create LearningActivity-object
                        learningActivity.setTitle(editText_dialog_name.getText().toString());
                        learningActivity.setDescription(editText_dialog_description.getText().toString());
                        learningActivity.setDuration(Integer.parseInt(editText_dialog_duration.getText().toString()));

                        // save LearningActivity-object in sql database
                        dbHandler.updateLearningActivity(learningActivity);

                        // refresh view
                        listLearningActivities = dbHandler.getAllLearningActivities();

                        // recreate all cards
                        notifyDataSetChanged();
                    }
                })
                .setNegativeButton("Annuleren", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // do nothing
                    }
                });
        // get and show the AlertDialog from create()
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }
}
