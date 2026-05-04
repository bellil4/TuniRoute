package com.tuniroute.data.model;

import androidx.room.Entity;
import androidx.room.ForeignKey;
import androidx.room.Index;
import androidx.room.PrimaryKey;

/**
 * Junction table linking a TransportLine to its stops in order.
 * travelTimeFromPrev represents travel time (in minutes) from the
 * previous stop in the sequence (0 for the first stop).
 */
@Entity(
    tableName = "line_stops",
    foreignKeys = {
        @ForeignKey(
            entity = TransportLine.class,
            parentColumns = "id",
            childColumns = "lineId",
            onDelete = ForeignKey.CASCADE
        ),
        @ForeignKey(
            entity = Stop.class,
            parentColumns = "id",
            childColumns = "stopId",
            onDelete = ForeignKey.CASCADE
        )
    },
    indices = {
        @Index("lineId"),
        @Index("stopId")
    }
)
public class LineStop {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public int lineId;
    public int stopId;

    /** Position of this stop within the line (1-based) */
    public int sequenceOrder;

    /** Minutes to travel from the previous stop (0 for first stop) */
    public int travelTimeFromPrev;

    public LineStop(int lineId, int stopId, int sequenceOrder, int travelTimeFromPrev) {
        this.lineId = lineId;
        this.stopId = stopId;
        this.sequenceOrder = sequenceOrder;
        this.travelTimeFromPrev = travelTimeFromPrev;
    }
}
