package com.zuyd.studybuddy;

import android.content.DialogInterface;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;

import java.util.List;

public class MainActivity extends AppCompatActivity {
    private FloatingActionButton fab;
    private boolean[] fabEnabled; // todo: dirty fix

    private RecyclerView recyclerView;
    private RecyclerView.Adapter adapter;

    private List<LearningActivity> listLearningActivities;
    private DbHandler dbHandler;

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
                    onCreateLearningActivityDialog();
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

        // create dbHandler-object
        dbHandler = new DbHandler(this, null, null, 1);

        // get all learning activities
        listLearningActivities = dbHandler.getAllLearningActivities();

        // adapter
        adapter = new LearningActivityAdapter(listLearningActivities, this, dbHandler, fabEnabled);
        recyclerView.setAdapter(adapter);
    }

    public void onCreateLearningActivityDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);

        // get the layout inflater
        LayoutInflater inflater = MainActivity.this.getLayoutInflater();

        // inflate and set the layout for the dialog
        // pass null as the parent view because it's going in the dialog layout
        builder.setView(inflater.inflate(R.layout.learning_activity_dialog, null))
                // Add action buttons
                .setTitle("Leeractiviteit aanmaken")
                .setPositiveButton("Opslaan", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        // EditTexts of dialog
                        EditText editText_dialog_name = (EditText) ((AlertDialog) dialog).findViewById(R.id.editText_dialog_name);
                        EditText editText_dialog_description = (EditText) ((AlertDialog) dialog).findViewById(R.id.editText_dialog_description);
                        EditText editText_dialog_duration = (EditText) ((AlertDialog) dialog).findViewById(R.id.editText_dialog_duration);

                        // create LearningActivity-object
                        LearningActivity learningActivity = new LearningActivity();
                        learningActivity.setTitle(editText_dialog_name.getText().toString());
                        learningActivity.setDescription(editText_dialog_description.getText().toString());
                        learningActivity.setDuration(Integer.parseInt(editText_dialog_duration.getText().toString()));

                        // save LearningActivity-object in sql database
                        dbHandler.addLearningActivity(learningActivity);

                        // refresh view
                        listLearningActivities = dbHandler.getAllLearningActivities();

                        // todo: dirty-fix: recreate all cards
                        adapter = new LearningActivityAdapter(listLearningActivities, MainActivity.this, dbHandler, fabEnabled);
                        recyclerView.setAdapter(adapter);
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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
