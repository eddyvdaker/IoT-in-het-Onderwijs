package com.zuyd.studybuddy;

import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.AlertDialog;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;

import java.util.List;

public class LearningActivityAdapter extends RecyclerView.Adapter<LearningActivityAdapter.ViewHolder> {
    private List<LearningActivity> listLearningActivities;
    private Context context;
    private DbHandler dbHandler;
    private View view;

    // constructor
    public LearningActivityAdapter(List<LearningActivity> listLearningActivities, Context context, DbHandler dbHandler) {
        this.listLearningActivities = listLearningActivities;
        this.context = context;
        this.dbHandler = dbHandler;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.learning_activity_card, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, final int position) {
        final LearningActivity learningActivity = listLearningActivities.get(position);

        // get Title
        holder.textViewTitle.setText(learningActivity.getTitle());

        // event handlers
        holder.imageButtonDelete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                dbHandler.deleteLearningActivity(learningActivity.getId());

                // refresh view
                listLearningActivities.remove(listLearningActivities.get(position));
                notifyDataSetChanged();
            }
        });

        holder.imageButtonStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // code here
                // todo: get id -> http-request
                // todo: show stopwatch UI dialog
            }
        });

        holder.textViewTitle.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // todo: edit -> filled in data
                onCreateLearningActivityDialog(context, learningActivity);
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

        // constructor
        public ViewHolder(View itemView) {
            super(itemView);

            imageButtonDelete = (ImageButton) itemView.findViewById(R.id.imageButtonDelete);
            imageButtonStart = (ImageButton) itemView.findViewById(R.id.imageButtonStart);
            textViewTitle = (TextView) itemView.findViewById(R.id.textViewTitle);
        }
    }

    // todo: refactor to seperate class as it's a modified version of the onCreateLearningActivityDialog method in MainActivity
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
                        // todo: User cancelled: files unchanged & return to previous state
                        // do nothing
                    }
                });
        // get and show the AlertDialog from create()
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }
}
