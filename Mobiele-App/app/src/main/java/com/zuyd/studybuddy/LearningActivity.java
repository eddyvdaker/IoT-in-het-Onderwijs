package com.zuyd.studybuddy;

public class LearningActivity {
    /// class attributes
    private int id;
    private int duration;

    private String title;
    private String description;
    private String creationTimestamp;
    private String completionTimestamp;
    private String folderLocation;

    /// constructors
    public LearningActivity() {

    }

    public LearningActivity(int id, int duration, String title, String description, String creationTimestamp) {
        this.id = id;
        this.duration = duration;
        this.title = title;
        this.description = description;
        this.creationTimestamp = creationTimestamp;
        // todo: this.folderLocation = "<<location of activity datafolder on device>>" + title + "\'
    }

    /// class methods
    // getters
    public int getId() {
        return id;
    }

    public int getDuration() {
        return duration;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getCreationTimestamp() {
        return creationTimestamp;
    }

    public String getCompletionTimestamp() {
        return completionTimestamp;
    }

    public String getFolderLocation() {
        return folderLocation;
    }

    // setters
    public void setId(int id) {
        this.id = id;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public void setCreationTimestamp(String creationTimestamp) {
        this.creationTimestamp = creationTimestamp;
    }

    public void setCompletionTimestamp(String completionTimestamp) {
        this.completionTimestamp = completionTimestamp;
    }

    public void setFolderLocation(String folderLocation) {
        this.folderLocation = folderLocation;
    }
}
