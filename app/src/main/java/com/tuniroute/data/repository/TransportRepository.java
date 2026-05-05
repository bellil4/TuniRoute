package com.tuniroute.data.repository;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.tuniroute.data.database.AppDatabase;
import com.tuniroute.data.database.DataInitializer;
import com.tuniroute.data.database.dao.LineStopDao;
import com.tuniroute.data.database.dao.StopDao;
import com.tuniroute.data.database.dao.TransportLineDao;
import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Single source of truth for transport data.
 * Abstracts the data source (Room database) from the ViewModels.
 */
public class TransportRepository {

    private final AppDatabase db;
    private final StopDao stopDao;
    private final TransportLineDao transportLineDao;
    private final LineStopDao lineStopDao;

    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    /** Tracks whether we have already verified / seeded the database this session. */
    private boolean initialized = false;

    public TransportRepository(Application application) {
        db = AppDatabase.getDatabase(application);
        stopDao = db.stopDao();
        transportLineDao = db.transportLineDao();
        lineStopDao = db.lineStopDao();
    }

    /**
     * Ensures the database is populated with seed data on first run.
     * Must be called on a background thread (it performs synchronous DB I/O).
     * Safe to call multiple times; only populates when the stops table is empty.
     */
    private void ensureInitialized() {
        if (!initialized) {
            initialized = true;
            if (stopDao.getCount() == 0) {
                DataInitializer.populateDatabase(db);
            }
        }
    }

    // ─── Stops ──────────────────────────────────────────────────────────────────

    public LiveData<List<Stop>> getAllStops() {
        return stopDao.getAllStops();
    }

    public List<Stop> getAllStopsSync() {
        ensureInitialized();
        return stopDao.getAllStopsSync();
    }

    public Stop getStopByName(String name) {
        ensureInitialized();
        return stopDao.getStopByName(name);
    }

    // ─── Lines ──────────────────────────────────────────────────────────────────

    public List<TransportLine> getAllLinesSync() {
        ensureInitialized();
        return transportLineDao.getAllLinesSync();
    }

    public TransportLine getLineById(int id) {
        return transportLineDao.getLineById(id);
    }

    // ─── Line Stops ─────────────────────────────────────────────────────────────

    public List<LineStop> getAllLineStopsSync() {
        ensureInitialized();
        return lineStopDao.getAllLineStopsSync();
    }

    // ─── Async helpers ───────────────────────────────────────────────────────────

    public ExecutorService getExecutor() {
        return executor;
    }
}
