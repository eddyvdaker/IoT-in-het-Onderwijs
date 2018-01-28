package com.zuyd.studybuddy;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.LinkedList;
import java.util.List;

public class TodoTabFragment extends Fragment{
    private static final String TAG = TodoTabFragment.class.getName();

    private RecyclerView mRecyclerView;
    private RecyclerView.LayoutManager mLayoutmanager;
    private RecyclerAdapter mAdapter;

    private LinkedList<StudyActivity> listStudyActivities;
    private boolean[] fabEnabled;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Bundle bundle = this.getArguments();

        // get listStudyActivities
        try  {
            listStudyActivities = (LinkedList<StudyActivity>) bundle.getSerializable("listStudyActivities");
        } catch (NullPointerException e) {
            Log.d(TAG, "NullpointerException listStudyActivities");
            listStudyActivities = new LinkedList<StudyActivity>();
        }

        // get fabEnabled
        try {
            fabEnabled = bundle.getBooleanArray("fabEnabled");
        } catch (NullPointerException e) {
            Log.d(TAG, "NullpointerException fabEnabled");
        }
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.todotab_fragment, container, false);

        // recyclerview
        mRecyclerView = (RecyclerView) view.findViewById(R.id.recyclerView);
        mLayoutmanager = new LinearLayoutManager(this.getActivity());
        mRecyclerView.setLayoutManager(mLayoutmanager);

        // Recycler adapter
        mAdapter = new RecyclerAdapter(listStudyActivities, this.getContext(), fabEnabled);
        mRecyclerView.setAdapter(mAdapter);

        return view;
    }
}
