package com.tuniroute.ui.results;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import com.tuniroute.algorithm.RouteFinder;
import com.tuniroute.algorithm.RouteResult;
import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;
import com.tuniroute.data.repository.TransportRepository;

import java.util.ArrayList;
import java.util.List;

public class ResultsViewModel extends AndroidViewModel {

    private final TransportRepository repository;
    private final MutableLiveData<List<RouteResult>> routes = new MutableLiveData<>();
    private final MutableLiveData<Boolean> isLoading = new MutableLiveData<>(false);
    private final MutableLiveData<String> errorMessage = new MutableLiveData<>();
    private final MutableLiveData<List<Stop>> stops = new MutableLiveData<>();
    private final MutableLiveData<List<TransportLine>> lines = new MutableLiveData<>();
    private final MutableLiveData<List<LineStop>> lineStops = new MutableLiveData<>();

    public ResultsViewModel(@NonNull Application application) {
        super(application);
        repository = new TransportRepository(application);
    }

    public LiveData<List<RouteResult>> getRoutes() {
        return routes;
    }

    public LiveData<Boolean> isLoading() {
        return isLoading;
    }

    public LiveData<String> getErrorMessage() {
        return errorMessage;
    }

    public LiveData<List<Stop>> getStops() {
        return stops;
    }

    public LiveData<List<TransportLine>> getLines() {
        return lines;
    }

    public LiveData<List<LineStop>> getLineStops() {
        return lineStops;
    }

    /**
     * Search for routes between the given stop names.
     * Executes on a background thread and posts results via LiveData.
     */
    public void searchRoutes(String sourceName, String destinationName) {
        isLoading.setValue(true);
        errorMessage.setValue(null);

        repository.getExecutor().execute(() -> {
            try {
                Stop source = repository.getStopByName(sourceName.trim());
                Stop dest   = repository.getStopByName(destinationName.trim());

                if (source == null) {
                    errorMessage.postValue("Stop not found: " + sourceName);
                    isLoading.postValue(false);
                    return;
                }
                if (dest == null) {
                    errorMessage.postValue("Stop not found: " + destinationName);
                    isLoading.postValue(false);
                    return;
                }

                List<Stop> allStops      = repository.getAllStopsSync();
                List<TransportLine> lines = repository.getAllLinesSync();
                List<LineStop> lineStops  = repository.getAllLineStopsSync();
                stops.postValue(allStops);
                this.lines.postValue(lines);
                this.lineStops.postValue(lineStops);

                RouteFinder finder = new RouteFinder();
                finder.buildGraph(allStops, lines, lineStops);
                List<RouteResult> results = finder.findRoutes(source.id, dest.id);

                if (results.isEmpty()) {
                    errorMessage.postValue("No route found between " + sourceName + " and " + destinationName + ".");
                }
                routes.postValue(results);
            } catch (Exception e) {
                errorMessage.postValue("An error occurred: " + e.getMessage());
                routes.postValue(new ArrayList<>());
            } finally {
                isLoading.postValue(false);
            }
        });
    }
}
