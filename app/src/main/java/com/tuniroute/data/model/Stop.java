package com.tuniroute.data.model;

import androidx.room.Entity;
import androidx.room.PrimaryKey;
import androidx.annotation.NonNull;

/**
 * Represents a physical stop or station in the transport network.
 * A stop can be shared by multiple transport lines (e.g., "République"
 * is served by Metro lines 1, 2, and 3).
 */
@Entity(tableName = "stops")
public class Stop {

    @PrimaryKey
    public int id;

    @NonNull
    public String name;

    public Stop(int id, @NonNull String name) {
        this.id = id;
        this.name = name;
    }
}
