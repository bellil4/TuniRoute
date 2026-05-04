package com.tuniroute.ui.home;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.tuniroute.data.model.Stop;
import com.tuniroute.data.repository.TransportRepository;

import java.util.ArrayList;
import java.util.List;

public class HomeViewModel extends AndroidViewModel {

    private final TransportRepository repository;
    private final MutableLiveData<List<String>> stopNames = new MutableLiveData<>(new ArrayList<>());
    private final MutableLiveData<String> errorMessage = new MutableLiveData<>();

    public HomeViewModel(@NonNull Application application) {
        super(application);
        repository = new TransportRepository(application);
        loadStopNames();
    }

    private void loadStopNames() {
        repository.getExecutor().execute(() -> {
            List<Stop> stops = repository.getAllStopsSync();
            List<String> names = new ArrayList<>();
            for (Stop s : stops) {
                names.add(s.name);
            }
            stopNames.postValue(names);
        });
    }

    public LiveData<List<String>> getStopNames() {
        return stopNames;
    }

    public LiveData<String> getErrorMessage() {
        return errorMessage;
    }

    /**
     * Validates the input and returns true if a search can proceed.
     */
    public boolean validateInput(String source, String destination) {
        if (source == null || source.trim().isEmpty()) {
            errorMessage.setValue("Please enter a source stop.");
            return false;
        }
        if (destination == null || destination.trim().isEmpty()) {
            errorMessage.setValue("Please enter a destination stop.");
            return false;
        }
        if (source.trim().equalsIgnoreCase(destination.trim())) {
            errorMessage.setValue("Source and destination must be different.");
            return false;
        }
        return true;
    }
}
