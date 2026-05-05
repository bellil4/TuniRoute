package com.tuniroute.data.database;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import androidx.room.TypeConverters;

import com.tuniroute.data.database.dao.LineStopDao;
import com.tuniroute.data.database.dao.StopDao;
import com.tuniroute.data.database.dao.TransportLineDao;
import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;

@Database(
    entities = {Stop.class, TransportLine.class, LineStop.class},
    version = 1,
    exportSchema = false
)
@TypeConverters({Converters.class})
public abstract class AppDatabase extends RoomDatabase {

    public abstract StopDao stopDao();
    public abstract TransportLineDao transportLineDao();
    public abstract LineStopDao lineStopDao();

    private static volatile AppDatabase INSTANCE;

    public static AppDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                            context.getApplicationContext(),
                            AppDatabase.class,
                            "tuniroute_database"
                    ).build();
                }
            }
        }
        return INSTANCE;
    }
}
