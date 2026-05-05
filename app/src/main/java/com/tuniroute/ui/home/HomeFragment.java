package com.tuniroute.ui.home;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.navigation.Navigation;

import com.tuniroute.R;
import com.tuniroute.databinding.FragmentHomeBinding;

import java.util.List;

public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;
    private HomeViewModel viewModel;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentHomeBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        viewModel = new ViewModelProvider(this).get(HomeViewModel.class);

        // Observe stop names for autocomplete
        viewModel.getStopNames().observe(getViewLifecycleOwner(), this::setupAutocomplete);

        // Observe validation errors
        viewModel.getErrorMessage().observe(getViewLifecycleOwner(), error -> {
            if (error != null) {
                Toast.makeText(requireContext(), error, Toast.LENGTH_SHORT).show();
            }
        });

        // Search button click
        binding.btnSearch.setOnClickListener(v -> {
            String source = binding.etSource.getText().toString();
            String dest   = binding.etDestination.getText().toString();

            if (viewModel.validateInput(source, dest)) {
                Bundle args = new Bundle();
                args.putString("sourceName", source.trim());
                args.putString("destinationName", dest.trim());
                Navigation.findNavController(v)
                          .navigate(R.id.action_home_to_results, args);
            }
        });

        // Swap source/destination button
        binding.btnSwap.setOnClickListener(v -> {
            String temp = binding.etSource.getText().toString();
            binding.etSource.setText(binding.etDestination.getText().toString());
            binding.etDestination.setText(temp);
        });
    }

    private void setupAutocomplete(List<String> names) {
        if (names == null || names.isEmpty()) return;
        ArrayAdapter<String> adapter = new ArrayAdapter<>(
                requireContext(),
                android.R.layout.simple_dropdown_item_1line,
                names
        );
        binding.etSource.setAdapter(adapter);
        binding.etDestination.setAdapter(adapter);
        binding.etSource.setThreshold(1);
        binding.etDestination.setThreshold(1);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
