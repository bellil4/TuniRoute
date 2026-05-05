package com.tuniroute.algorithm;

import com.tuniroute.data.model.TransportType;

/**
 * Represents one segment of a journey: board a specific line at one stop
 * and ride to another stop.
 */
public class RouteStep {

    public final String fromStopName;
    public final String toStopName;
    public final String lineName;
    public final TransportType transportType;

    /** Minutes spent travelling on this segment (excludes waiting/transfer) */
    public final int travelMinutes;

    /** Minutes waited before boarding (initial wait or transfer wait) */
    public final int waitMinutes;

    public RouteStep(String fromStopName, String toStopName,
                     String lineName, TransportType transportType,
                     int travelMinutes, int waitMinutes) {
        this.fromStopName  = fromStopName;
        this.toStopName    = toStopName;
        this.lineName      = lineName;
        this.transportType = transportType;
        this.travelMinutes = travelMinutes;
        this.waitMinutes   = waitMinutes;
    }

    public int totalMinutes() {
        return waitMinutes + travelMinutes;
    }
}
