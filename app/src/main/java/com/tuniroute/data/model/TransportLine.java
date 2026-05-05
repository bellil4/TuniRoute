package com.tuniroute.data.model;

import androidx.room.Entity;
import androidx.room.PrimaryKey;
import androidx.annotation.NonNull;

/**
 * Represents a public transport line (bus, metro, or train).
 */
@Entity(tableName = "transport_lines")
public class TransportLine {

    @PrimaryKey
    public int id;

    /** Internal name, e.g. "metro_l1" */
    @NonNull
    public String name;

    /** Display name shown to the user, e.g. "Métro Ligne 1" */
    @NonNull
    public String displayName;

    /** The type of transport (BUS, METRO, TRAIN) */
    @NonNull
    public TransportType type;

    /** Color code for UI display (hex string, e.g. "#4CAF50") */
    @NonNull
    public String colorHex;

    public TransportLine(int id, @NonNull String name, @NonNull String displayName,
                         @NonNull TransportType type, @NonNull String colorHex) {
        this.id = id;
        this.name = name;
        this.displayName = displayName;
        this.type = type;
        this.colorHex = colorHex;
    }
}
