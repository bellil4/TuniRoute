package com.tuniroute.data.database;

import androidx.room.TypeConverter;
import com.tuniroute.data.model.TransportType;

public class Converters {

    @TypeConverter
    public static TransportType fromString(String value) {
        return value == null ? null : TransportType.valueOf(value);
    }

    @TypeConverter
    public static String fromTransportType(TransportType type) {
        return type == null ? null : type.name();
    }
}
