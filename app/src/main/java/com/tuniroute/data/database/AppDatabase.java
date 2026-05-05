package com.tuniroute.data.database;

import android.content.Context;

import androidx.annotation.NonNull;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import androidx.room.TypeConverters;
import androidx.sqlite.db.SupportSQLiteDatabase;

import com.tuniroute.data.database.dao.LineStopDao;
import com.tuniroute.data.database.dao.StopDao;
import com.tuniroute.data.database.dao.TransportLineDao;
import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

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

    static final ExecutorService databaseWriteExecutor =
            Executors.newFixedThreadPool(4);

    public static AppDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                            context.getApplicationContext(),
                            AppDatabase.class,
                            "tuniroute_database"
                    )
                    .addCallback(sRoomDatabaseCallback)
                    .build();
                }
            }
        }
        return INSTANCE;
    }

    private static final RoomDatabase.Callback sRoomDatabaseCallback = new RoomDatabase.Callback() {
        @Override
        public void onCreate(@NonNull SupportSQLiteDatabase db) {
            super.onCreate(db);
            databaseWriteExecutor.execute(() -> {
                if (INSTANCE != null) {
                    DataInitializer.populateDatabase(INSTANCE);
                }
            });
        }
    };
}
