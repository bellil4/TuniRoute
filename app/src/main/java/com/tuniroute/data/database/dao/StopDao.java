package com.tuniroute.data.database.dao;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.tuniroute.data.model.Stop;

import java.util.List;

@Dao
public interface StopDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<Stop> stops);

    @Query("SELECT * FROM stops ORDER BY name ASC")
    LiveData<List<Stop>> getAllStops();

    @Query("SELECT * FROM stops ORDER BY name ASC")
    List<Stop> getAllStopsSync();

    @Query("SELECT * FROM stops WHERE id = :id LIMIT 1")
    Stop getStopById(int id);

    @Query("SELECT * FROM stops WHERE name = :name LIMIT 1")
    Stop getStopByName(String name);

    @Query("SELECT COUNT(*) FROM stops")
    int getCount();
}
