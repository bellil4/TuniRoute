package com.tuniroute.data.database.dao;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;

import com.tuniroute.data.model.TransportLine;

import java.util.List;

@Dao
public interface TransportLineDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insertAll(List<TransportLine> lines);

    @Query("SELECT * FROM transport_lines")
    List<TransportLine> getAllLinesSync();

    @Query("SELECT * FROM transport_lines WHERE id = :id LIMIT 1")
    TransportLine getLineById(int id);

    @Query("SELECT COUNT(*) FROM transport_lines")
    int getCount();
}
