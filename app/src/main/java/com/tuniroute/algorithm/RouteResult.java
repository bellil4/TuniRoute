package com.tuniroute.algorithm;

import java.util.List;

/**
 * A complete journey from the origin to the destination,
 * composed of one or more RouteSteps.
 */
public class RouteResult {

    public final List<RouteStep> steps;
    public final int totalMinutes;
    public final int transferCount;

    public RouteResult(List<RouteStep> steps) {
        this.steps = steps;
        int total = 0;
        for (RouteStep step : steps) {
            total += step.totalMinutes();
        }
        this.totalMinutes = total;
        // transfers = number of line changes = steps.size() - 1
        this.transferCount = Math.max(0, steps.size() - 1);
    }

    /** Human-readable summary, e.g. "Métro Ligne 1 → Bus Ligne 50" */
    public String getSummary() {
        if (steps.isEmpty()) return "";
        if (steps.size() == 1) return steps.get(0).lineName;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < steps.size(); i++) {
            if (i > 0) sb.append(" → ");
            sb.append(steps.get(i).lineName);
        }
        return sb.toString();
    }
}
