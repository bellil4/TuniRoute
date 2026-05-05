package com.tuniroute.ui.results;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.tuniroute.R;
import com.tuniroute.algorithm.RouteResult;
import com.tuniroute.algorithm.RouteStep;
import com.tuniroute.data.model.TransportType;

import java.util.ArrayList;
import java.util.List;

public class RouteResultAdapter extends RecyclerView.Adapter<RouteResultAdapter.ViewHolder> {

    public interface OnRouteClickListener {
        void onRouteClick(RouteResult route);
    }

    private List<RouteResult> routes = new ArrayList<>();
    private final OnRouteClickListener listener;

    public RouteResultAdapter(OnRouteClickListener listener) {
        this.listener = listener;
    }

    public void setRoutes(List<RouteResult> routes) {
        this.routes = routes != null ? routes : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_route_result, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        RouteResult route = routes.get(position);
        holder.bind(route, listener);
    }

    @Override
    public int getItemCount() {
        return routes.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {

        private final TextView tvSummary;
        private final TextView tvTotalTime;
        private final TextView tvTransfers;
        private final LinearLayout stepsContainer;

        ViewHolder(@NonNull View itemView) {
            super(itemView);
            tvSummary      = itemView.findViewById(R.id.tv_route_summary);
            tvTotalTime    = itemView.findViewById(R.id.tv_total_time);
            tvTransfers    = itemView.findViewById(R.id.tv_transfers);
            stepsContainer = itemView.findViewById(R.id.steps_container);
        }

        void bind(RouteResult route, OnRouteClickListener listener) {
            tvSummary.setText(route.getSummary());
            tvTotalTime.setText(formatTime(route.totalMinutes));
            tvTransfers.setText(route.transferCount == 0
                    ? "Direct"
                    : route.transferCount + (route.transferCount == 1 ? " transfer" : " transfers"));

            // Build step rows dynamically
            stepsContainer.removeAllViews();
            for (RouteStep step : route.steps) {
                View stepView = LayoutInflater.from(itemView.getContext())
                        .inflate(R.layout.item_route_step, stepsContainer, false);

                TextView tvLine     = stepView.findViewById(R.id.tv_step_line);
                TextView tvFrom     = stepView.findViewById(R.id.tv_step_from);
                TextView tvTo       = stepView.findViewById(R.id.tv_step_to);
                TextView tvTime     = stepView.findViewById(R.id.tv_step_time);
                View     colorBar   = stepView.findViewById(R.id.view_type_color);
                ImageView ivIcon    = stepView.findViewById(R.id.iv_transport_icon);

                tvLine.setText(step.lineName);
                tvFrom.setText(step.fromStopName);
                tvTo.setText(step.toStopName);
                tvTime.setText(formatTime(step.totalMinutes()));

                // Set icon and color based on transport type
                int iconRes = iconForType(step.transportType);
                ivIcon.setImageResource(iconRes);
                colorBar.setBackgroundColor(colorForType(step.transportType));

                stepsContainer.addView(stepView);
            }

            itemView.setOnClickListener(v -> {
                if (listener != null) listener.onRouteClick(route);
            });
        }

        private String formatTime(int minutes) {
            if (minutes < 60) return minutes + " min";
            int h = minutes / 60;
            int m = minutes % 60;
            return m == 0 ? h + " h" : h + " h " + m + " min";
        }

        private int iconForType(TransportType type) {
            switch (type) {
                case METRO: return R.drawable.ic_metro;
                case TRAIN: return R.drawable.ic_train;
                default:    return R.drawable.ic_bus;
            }
        }

        private int colorForType(TransportType type) {
            switch (type) {
                case METRO: return Color.parseColor("#4CAF50");
                case TRAIN: return Color.parseColor("#9C27B0");
                default:    return Color.parseColor("#FF9800");
            }
        }
    }
}
