package com.tuniroute.algorithm;

import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;
import com.tuniroute.data.model.TransportType;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

/**
 * Finds optimal routes through the Tunis public transport network.
 *
 * Algorithm: Dijkstra on a state-space graph where each state is
 * (stopId, currentLineId).  A "transfer" penalty is added whenever
 * the passenger switches lines at the same stop.
 *
 * Wait times (minutes, approximate averages):
 *   Metro : 5 min
 *   Train  : 10 min
 *   Bus    : 8 min
 *
 * Transfer walking penalty: 3 min
 */
public class RouteFinder {

    // ─── Tuning constants ───────────────────────────────────────────────────────
    private static final int WAIT_METRO    = 5;
    private static final int WAIT_TRAIN    = 10;
    private static final int WAIT_BUS      = 8;
    private static final int TRANSFER_WALK = 3;  // minutes to walk between platforms

    /** Maximum number of route options to return */
    private static final int MAX_RESULTS = 3;

    // ─── Graph data ─────────────────────────────────────────────────────────────

    /** adjacency list: stopId → list of outgoing edges */
    private final Map<Integer, List<Edge>> graph = new HashMap<>();

    /** stopId → stop name */
    private final Map<Integer, String> stopNames = new HashMap<>();

    /** lineId → TransportLine */
    private final Map<Integer, TransportLine> lineMap = new HashMap<>();

    // ─── Inner classes ──────────────────────────────────────────────────────────

    private static class Edge {
        final int toStopId;
        final int lineId;
        final int travelMinutes;

        Edge(int toStopId, int lineId, int travelMinutes) {
            this.toStopId      = toStopId;
            this.lineId        = lineId;
            this.travelMinutes = travelMinutes;
        }
    }

    /** Dijkstra node (state = stop + active line) */
    private static class State implements Comparable<State> {
        final int stopId;
        final int lineId;   // -1 = not yet boarded any line
        final int totalTime;
        final int transfers;
        final List<RouteStep> path;

        State(int stopId, int lineId, int totalTime, int transfers, List<RouteStep> path) {
            this.stopId    = stopId;
            this.lineId    = lineId;
            this.totalTime = totalTime;
            this.transfers = transfers;
            this.path      = path;
        }

        @Override
        public int compareTo(State other) {
            // Primary: minimise total time.  Secondary: minimise transfers.
            if (this.totalTime != other.totalTime) return Integer.compare(this.totalTime, other.totalTime);
            return Integer.compare(this.transfers, other.transfers);
        }
    }

    // ─── Public API ─────────────────────────────────────────────────────────────

    /**
     * Build the graph from database data.
     * Must be called before {@link #findRoutes}.
     */
    public void buildGraph(List<Stop> stops, List<TransportLine> lines, List<LineStop> lineStops) {
        graph.clear();
        stopNames.clear();
        lineMap.clear();

        for (Stop s : stops) {
            stopNames.put(s.id, s.name);
            graph.put(s.id, new ArrayList<>());
        }

        for (TransportLine l : lines) {
            lineMap.put(l.id, l);
        }

        // Group line-stops by line
        Map<Integer, List<LineStop>> byLine = new HashMap<>();
        for (LineStop ls : lineStops) {
            byLine.computeIfAbsent(ls.lineId, k -> new ArrayList<>()).add(ls);
        }

        // For each line, sort stops by sequenceOrder and add bidirectional edges
        for (Map.Entry<Integer, List<LineStop>> entry : byLine.entrySet()) {
            int lineId = entry.getKey();
            List<LineStop> ordered = entry.getValue();
            Collections.sort(ordered, (a, b) -> Integer.compare(a.sequenceOrder, b.sequenceOrder));

            for (int i = 0; i < ordered.size() - 1; i++) {
                LineStop from = ordered.get(i);
                LineStop to   = ordered.get(i + 1);
                int travelTime = to.travelTimeFromPrev;

                // Forward direction
                addEdge(from.stopId, to.stopId, lineId, travelTime);
                // Reverse direction (lines are bidirectional in Tunis)
                addEdge(to.stopId, from.stopId, lineId, travelTime);
            }
        }
    }

    /**
     * Find up to {@link #MAX_RESULTS} routes from source stop to destination stop.
     *
     * @param sourceStopId      ID of the origin stop
     * @param destinationStopId ID of the destination stop
     * @return list of RouteResult objects, ordered by total time (fastest first)
     */
    public List<RouteResult> findRoutes(int sourceStopId, int destinationStopId) {
        if (sourceStopId == destinationStopId) return Collections.emptyList();

        List<RouteResult> results = new ArrayList<>();

        PriorityQueue<State> queue = new PriorityQueue<>();
        // visited: (stopId, lineId) pairs already processed at lower cost
        Map<String, Integer> visited = new HashMap<>();

        // Initial state: at source, no line boarded yet
        queue.add(new State(sourceStopId, -1, 0, 0, new ArrayList<>()));

        while (!queue.isEmpty() && results.size() < MAX_RESULTS) {
            State current = queue.poll();

            String key = current.stopId + "," + current.lineId;
            Integer best = visited.get(key);
            if (best != null && best <= current.totalTime) continue;
            visited.put(key, current.totalTime);

            if (current.stopId == destinationStopId && current.lineId != -1) {
                results.add(new RouteResult(current.path));
                continue;
            }

            List<Edge> edges = graph.getOrDefault(current.stopId, Collections.emptyList());
            for (Edge edge : edges) {
                TransportLine line = lineMap.get(edge.lineId);
                if (line == null) continue;

                int addedTime   = 0;
                int newTransfers = current.transfers;

                if (current.lineId == -1) {
                    // First boarding: add initial wait time
                    addedTime = waitTime(line.type);
                } else if (current.lineId != edge.lineId) {
                    // Transfer: walking penalty + wait for new line
                    addedTime = TRANSFER_WALK + waitTime(line.type);
                    newTransfers++;
                }

                addedTime += edge.travelMinutes;

                // Build the new path
                List<RouteStep> newPath = new ArrayList<>(current.path);
                String fromName = stopNames.getOrDefault(current.stopId, "?");
                String toName   = stopNames.getOrDefault(edge.toStopId, "?");

                // Extend the last step if we're still on the same line,
                // otherwise create a new step.
                if (!newPath.isEmpty() && current.lineId == edge.lineId) {
                    RouteStep last = newPath.remove(newPath.size() - 1);
                    newPath.add(new RouteStep(
                            last.fromStopName, toName,
                            last.lineName, last.transportType,
                            last.travelMinutes + edge.travelMinutes,
                            last.waitMinutes
                    ));
                } else {
                    int wait = (current.lineId == -1) ? waitTime(line.type)
                                                       : TRANSFER_WALK + waitTime(line.type);
                    newPath.add(new RouteStep(
                            fromName, toName,
                            line.displayName, line.type,
                            edge.travelMinutes,
                            wait
                    ));
                }

                int newTime = current.totalTime + addedTime;
                queue.add(new State(edge.toStopId, edge.lineId, newTime, newTransfers, newPath));
            }
        }

        return results;
    }

    // ─── Helpers ─────────────────────────────────────────────────────────────────

    private void addEdge(int fromStopId, int toStopId, int lineId, int travelMinutes) {
        graph.computeIfAbsent(fromStopId, k -> new ArrayList<>())
             .add(new Edge(toStopId, lineId, travelMinutes));
    }

    private static int waitTime(TransportType type) {
        switch (type) {
            case METRO: return WAIT_METRO;
            case TRAIN: return WAIT_TRAIN;
            case BUS:   return WAIT_BUS;
            default:    return WAIT_BUS;
        }
    }
}
