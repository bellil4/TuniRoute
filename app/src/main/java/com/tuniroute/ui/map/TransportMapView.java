package com.tuniroute.ui.map;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.text.TextPaint;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

import androidx.annotation.Nullable;

import com.tuniroute.algorithm.RouteResult;
import com.tuniroute.algorithm.RouteStep;
import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

/**
 * Lightweight schematic graph view for transport stops and connections.
 * Draws a deterministic, programmatic network layout from line/stop data and can highlight a route.
 */
public class TransportMapView extends View {

    private static final float NODE_RADIUS_DP = 6f;
    private static final float TOUCH_RADIUS_DP = 20f;
    private static final float LABEL_OFFSET_DP = 7f;
    private static final float STROKE_WIDTH_DP = 2f;
    private static final float HIGHLIGHT_WIDTH_DP = 4f;

    private final Paint baseEdgePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint nodePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint highlightPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final TextPaint labelPaint = new TextPaint(Paint.ANTI_ALIAS_FLAG);

    private final Map<Integer, Stop> stopsById = new HashMap<>();
    private final Map<Integer, NodePosition> positions = new HashMap<>();
    private final Map<String, Integer> stopIdByNormalizedName = new HashMap<>();
    private final List<GraphEdge> baseEdges = new ArrayList<>();
    private final List<GraphEdge> highlightedEdges = new ArrayList<>();

    @Nullable
    private OnStopTapListener onStopTapListener;

    public interface OnStopTapListener {
        void onStopTapped(Stop stop);
    }

    public TransportMapView(Context context) {
        super(context);
        init();
    }

    public TransportMapView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public TransportMapView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        float density = getResources().getDisplayMetrics().density;
        baseEdgePaint.setColor(Color.parseColor("#BDBDBD"));
        baseEdgePaint.setStyle(Paint.Style.STROKE);
        baseEdgePaint.setStrokeWidth(STROKE_WIDTH_DP * density);
        baseEdgePaint.setStrokeCap(Paint.Cap.ROUND);

        highlightPaint.setColor(Color.parseColor("#1565C0"));
        highlightPaint.setStyle(Paint.Style.STROKE);
        highlightPaint.setStrokeWidth(HIGHLIGHT_WIDTH_DP * density);
        highlightPaint.setStrokeCap(Paint.Cap.ROUND);

        nodePaint.setColor(Color.parseColor("#1E88E5"));
        nodePaint.setStyle(Paint.Style.FILL);

        labelPaint.setColor(Color.parseColor("#424242"));
        labelPaint.setTextSize(11f * density);
    }

    public void setOnStopTapListener(@Nullable OnStopTapListener listener) {
        this.onStopTapListener = listener;
    }

    public void setGraphData(List<Stop> stops, List<TransportLine> lines, List<LineStop> lineStops) {
        stopsById.clear();
        positions.clear();
        stopIdByNormalizedName.clear();
        baseEdges.clear();
        highlightedEdges.clear();

        if (stops == null || lines == null || lineStops == null || stops.isEmpty()) {
            invalidate();
            return;
        }

        for (Stop stop : stops) {
            stopsById.put(stop.id, stop);
            stopIdByNormalizedName.put(normalize(stop.name), stop.id);
        }

        Map<Integer, List<LineStop>> lineStopsByLine = new HashMap<>();
        for (LineStop lineStop : lineStops) {
            lineStopsByLine.computeIfAbsent(lineStop.lineId, key -> new ArrayList<>()).add(lineStop);
        }

        List<TransportLine> orderedLines = new ArrayList<>(lines);
        Collections.sort(orderedLines, Comparator.comparingInt(line -> line.id));

        Map<Integer, List<NodePosition>> occurrences = new HashMap<>();
        int lineDenominator = orderedLines.size() > 1 ? orderedLines.size() - 1 : 1;

        for (int lineIndex = 0; lineIndex < orderedLines.size(); lineIndex++) {
            TransportLine line = orderedLines.get(lineIndex);
            List<LineStop> sequence = lineStopsByLine.get(line.id);
            if (sequence == null || sequence.isEmpty()) {
                continue;
            }
            Collections.sort(sequence, Comparator.comparingInt(item -> item.sequenceOrder));

            int stopCount = Math.max(1, sequence.size() - 1);
            for (int i = 0; i < sequence.size(); i++) {
                float x = 0.1f + (0.8f * i / stopCount);
                float y = 0.15f + (0.7f * lineIndex / lineDenominator);
                NodePosition position = new NodePosition(x, y);
                occurrences.computeIfAbsent(sequence.get(i).stopId, key -> new ArrayList<>()).add(position);
            }

            for (int i = 0; i < sequence.size() - 1; i++) {
                baseEdges.add(new GraphEdge(sequence.get(i).stopId, sequence.get(i + 1).stopId));
            }
        }

        for (Map.Entry<Integer, List<NodePosition>> entry : occurrences.entrySet()) {
            List<NodePosition> list = entry.getValue();
            float sumX = 0f;
            float sumY = 0f;
            for (NodePosition nodePosition : list) {
                sumX += nodePosition.x;
                sumY += nodePosition.y;
            }
            positions.put(entry.getKey(), new NodePosition(sumX / list.size(), sumY / list.size()));
        }

        invalidate();
    }

    public void setHighlightedRoute(@Nullable RouteResult route) {
        highlightedEdges.clear();
        if (route != null && route.steps != null) {
            for (RouteStep step : route.steps) {
                Integer fromId = stopIdByNormalizedName.get(normalize(step.fromStopName));
                Integer toId = stopIdByNormalizedName.get(normalize(step.toStopName));
                if (fromId != null && toId != null) {
                    highlightedEdges.add(new GraphEdge(fromId, toId));
                }
            }
        }
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        float radius = dpToPx(NODE_RADIUS_DP);
        float labelOffset = dpToPx(LABEL_OFFSET_DP);

        drawEdges(canvas, baseEdges, baseEdgePaint);
        drawEdges(canvas, highlightedEdges, highlightPaint);

        List<Map.Entry<Integer, NodePosition>> orderedNodes = new ArrayList<>(positions.entrySet());
        Collections.sort(orderedNodes, Comparator.comparingInt(Map.Entry::getKey));

        for (Map.Entry<Integer, NodePosition> entry : orderedNodes) {
            Stop stop = stopsById.get(entry.getKey());
            if (stop == null) continue;

            float cx = entry.getValue().x * getWidth();
            float cy = entry.getValue().y * getHeight();
            canvas.drawCircle(cx, cy, radius, nodePaint);
            canvas.drawText(stop.name, cx + labelOffset, cy - labelOffset, labelPaint);
        }
    }

    private void drawEdges(Canvas canvas, List<GraphEdge> edges, Paint paint) {
        Set<GraphEdge> unique = new HashSet<>(edges);
        for (GraphEdge edge : unique) {
            NodePosition from = positions.get(edge.fromStopId);
            NodePosition to = positions.get(edge.toStopId);
            if (from == null || to == null) continue;
            canvas.drawLine(from.x * getWidth(), from.y * getHeight(), to.x * getWidth(), to.y * getHeight(), paint);
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getAction() != MotionEvent.ACTION_UP) {
            return true;
        }

        float touchRadius = dpToPx(TOUCH_RADIUS_DP);
        float x = event.getX();
        float y = event.getY();

        Integer tappedStopId = findTappedStopId(x, y, touchRadius);
        if (tappedStopId != null) {
            performClick();
            if (onStopTapListener != null) {
                Stop stop = stopsById.get(tappedStopId);
                if (stop != null) {
                    onStopTapListener.onStopTapped(stop);
                }
            }
            return true;
        }
        return super.onTouchEvent(event);
    }

    @Override
    public boolean performClick() {
        return super.performClick();
    }

    @Nullable
    private Integer findTappedStopId(float x, float y, float radius) {
        float minDistanceSquared = Float.MAX_VALUE;
        Integer candidate = null;
        for (Map.Entry<Integer, NodePosition> entry : positions.entrySet()) {
            float cx = entry.getValue().x * getWidth();
            float cy = entry.getValue().y * getHeight();
            float dx = x - cx;
            float dy = y - cy;
            float distanceSquared = (dx * dx) + (dy * dy);
            if (distanceSquared <= radius * radius && distanceSquared < minDistanceSquared) {
                minDistanceSquared = distanceSquared;
                candidate = entry.getKey();
            }
        }
        return candidate;
    }

    private float dpToPx(float dp) {
        return dp * getResources().getDisplayMetrics().density;
    }

    private String normalize(String value) {
        return value == null ? "" : value.trim().toLowerCase(Locale.ROOT);
    }

    private static class NodePosition {
        final float x;
        final float y;

        NodePosition(float x, float y) {
            this.x = x;
            this.y = y;
        }
    }

    private static class GraphEdge {
        final int fromStopId;
        final int toStopId;

        GraphEdge(int fromStopId, int toStopId) {
            if (fromStopId <= toStopId) {
                this.fromStopId = fromStopId;
                this.toStopId = toStopId;
            } else {
                this.fromStopId = toStopId;
                this.toStopId = fromStopId;
            }
        }

        @Override
        public boolean equals(Object other) {
            if (this == other) return true;
            if (!(other instanceof GraphEdge)) return false;
            GraphEdge edge = (GraphEdge) other;
            return fromStopId == edge.fromStopId && toStopId == edge.toStopId;
        }

        @Override
        public int hashCode() {
            return 31 * fromStopId + toStopId;
        }
    }
}
