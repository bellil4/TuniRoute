package com.tuniroute.ui.results;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;
import androidx.recyclerview.widget.LinearLayoutManager;

import com.tuniroute.R;
import com.tuniroute.algorithm.RouteResult;
import com.tuniroute.databinding.FragmentResultsBinding;

public class ResultsFragment extends Fragment {

    private FragmentResultsBinding binding;
    private ResultsViewModel viewModel;
    private RouteResultAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentResultsBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        viewModel = new ViewModelProvider(this).get(ResultsViewModel.class);

        // Get arguments
        String sourceName = getArguments() != null ? getArguments().getString("sourceName", "") : "";
        String destName   = getArguments() != null ? getArguments().getString("destinationName", "") : "";

        // Update toolbar subtitle
        binding.tvRouteHeader.setText(sourceName + "  →  " + destName);

        // Set up RecyclerView
        adapter = new RouteResultAdapter(this::onRouteClicked);
        binding.rvRoutes.setLayoutManager(new LinearLayoutManager(requireContext()));
        binding.rvRoutes.setAdapter(adapter);
        binding.transportMapView.setOnStopTapListener(stop ->
                Toast.makeText(requireContext(), stop.name, Toast.LENGTH_SHORT).show());

        // Observe routes
        viewModel.getRoutes().observe(getViewLifecycleOwner(), routes -> {
            adapter.setRoutes(routes);
            boolean empty = routes == null || routes.isEmpty();
            binding.tvNoRoutes.setVisibility(empty ? View.VISIBLE : View.GONE);
            binding.rvRoutes.setVisibility(empty ? View.GONE : View.VISIBLE);
            binding.transportMapView.setHighlightedRoute(empty ? null : routes.get(0));
        });

        viewModel.getStops().observe(getViewLifecycleOwner(), stops ->
                binding.transportMapView.setGraphData(
                        stops,
                        viewModel.getLines().getValue(),
                        viewModel.getLineStops().getValue()
                ));
        viewModel.getLines().observe(getViewLifecycleOwner(), lines ->
                binding.transportMapView.setGraphData(
                        viewModel.getStops().getValue(),
                        lines,
                        viewModel.getLineStops().getValue()
                ));
        viewModel.getLineStops().observe(getViewLifecycleOwner(), lineStops ->
                binding.transportMapView.setGraphData(
                        viewModel.getStops().getValue(),
                        viewModel.getLines().getValue(),
                        lineStops
                ));

        // Observe loading state
        viewModel.isLoading().observe(getViewLifecycleOwner(), loading -> {
            binding.progressBar.setVisibility(Boolean.TRUE.equals(loading) ? View.VISIBLE : View.GONE);
        });

        // Observe error messages
        viewModel.getErrorMessage().observe(getViewLifecycleOwner(), error -> {
            if (error != null) {
                binding.tvNoRoutes.setText(error);
                binding.tvNoRoutes.setVisibility(View.VISIBLE);
                binding.rvRoutes.setVisibility(View.GONE);
            }
        });

        // Back button
        binding.btnBack.setOnClickListener(v ->
                Navigation.findNavController(v).navigateUp());

        // Trigger search
        if (!sourceName.isEmpty() && !destName.isEmpty()) {
            viewModel.searchRoutes(sourceName, destName);
        }
    }

    private void onRouteClicked(RouteResult route) {
        binding.transportMapView.setHighlightedRoute(route);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
