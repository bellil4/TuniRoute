package com.tuniroute.data.database.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.tuniroute.data.model.LineStop;

import java.util.List;

@Dao
public interface LineStopDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<LineStop> lineStops);

    @Query("SELECT * FROM line_stops ORDER BY lineId, sequenceOrder ASC")
    List<LineStop> getAllLineStopsSync();

    @Query("SELECT * FROM line_stops WHERE lineId = :lineId ORDER BY sequenceOrder ASC")
    List<LineStop> getStopsForLine(int lineId);

    @Query("SELECT COUNT(*) FROM line_stops")
    int getCount();
}
