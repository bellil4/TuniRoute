package com.tuniroute.data.database;

import com.tuniroute.data.model.LineStop;
import com.tuniroute.data.model.Stop;
import com.tuniroute.data.model.TransportLine;
import com.tuniroute.data.model.TransportType;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Populates the database with sample Tunis public transport data.
 *
 * Transport lines included:
 *  - Métro Léger de Tunis: Lines 1, 2, and 3
 *  - TGM (Train Tunis-Goulette-Marsa)
 *  - Bus Ligne 5 (Bab Bhar → Manouba)
 *  - Bus Ligne 50 (Bab Bhar → Ariana)
 *
 * Key transfer points (stops shared by multiple lines):
 *  - République    : Metro L1, L2, L3
 *  - Bab Saadoun   : Metro L1, Bus 50
 *  - Cité Olympique: Metro L2, Bus 5, Bus 50
 *  - Ariana        : Metro L2, Bus 50
 *  - Khereddine    : Metro L3, TGM
 *  - Tunis Marine  : TGM
 */
public class DataInitializer {

    // ─── Stop IDs ───────────────────────────────────────────────────────────────
    // Shared metro hub
    static final int STOP_REPUBLIQUE        = 1;
    // Metro Line 1 stops
    static final int STOP_BARCELONE         = 2;
    static final int STOP_BAB_SAADOUN       = 3;
    static final int STOP_MONTPLAISIR       = 4;
    static final int STOP_QURTABA           = 5;
    static final int STOP_MOHAMEDIA         = 6;
    static final int STOP_BEN_AROUS         = 7;
    // Metro Line 2 stops
    static final int STOP_PALESTINE         = 8;
    static final int STOP_CITE_OLYMPIQUE    = 9;
    static final int STOP_BOUCHOUCHA        = 10;
    static final int STOP_ARIANA            = 11;
    static final int STOP_EL_GHAZALA        = 12;
    // Metro Line 3 stops
    static final int STOP_BAB_ALIOUA        = 13;
    static final int STOP_BAB_JEDID         = 14;
    static final int STOP_HAY_HLEL          = 15;
    static final int STOP_CITE_DES_SCIENCES = 16;
    static final int STOP_KHEREDDINE        = 17;
    static final int STOP_LAOUINA           = 18;
    // TGM stops
    static final int STOP_TUNIS_MARINE      = 19;
    static final int STOP_LA_GOULETTE_VX    = 20;
    static final int STOP_LA_GOULETTE_NV    = 21;
    static final int STOP_CARTHAGE_SALAMMBO = 22;
    static final int STOP_CARTHAGE_HANNIBAL = 23;
    static final int STOP_SIDI_BOU_SAID     = 24;
    static final int STOP_LA_MARSA          = 25;
    // Bus stops
    static final int STOP_BAB_BHAR          = 26;
    static final int STOP_BAB_EL_KHADRA     = 27;
    static final int STOP_BARDO             = 28;
    static final int STOP_MANOUBA           = 29;

    // ─── Line IDs ───────────────────────────────────────────────────────────────
    static final int LINE_METRO_L1  = 1;
    static final int LINE_METRO_L2  = 2;
    static final int LINE_METRO_L3  = 3;
    static final int LINE_TGM       = 4;
    static final int LINE_BUS_5     = 5;
    static final int LINE_BUS_50    = 6;

    public static void populateDatabase(AppDatabase db) {
        db.stopDao().insertAll(buildStops());
        db.transportLineDao().insertAll(buildLines());
        db.lineStopDao().insertAll(buildLineStops());
    }

    // ─── Stops ──────────────────────────────────────────────────────────────────

    private static List<Stop> buildStops() {
        return Arrays.asList(
            new Stop(STOP_REPUBLIQUE,        "République"),
            new Stop(STOP_BARCELONE,         "Barcelone"),
            new Stop(STOP_BAB_SAADOUN,       "Bab Saadoun"),
            new Stop(STOP_MONTPLAISIR,       "Tunis Montplaisir"),
            new Stop(STOP_QURTABA,           "Qurtaba"),
            new Stop(STOP_MOHAMEDIA,         "Mohamedia"),
            new Stop(STOP_BEN_AROUS,         "Ben Arous"),
            new Stop(STOP_PALESTINE,         "Palestine"),
            new Stop(STOP_CITE_OLYMPIQUE,    "Cité Olympique"),
            new Stop(STOP_BOUCHOUCHA,        "Bouchoucha"),
            new Stop(STOP_ARIANA,            "Ariana"),
            new Stop(STOP_EL_GHAZALA,        "El Ghazala"),
            new Stop(STOP_BAB_ALIOUA,        "Bab Alioua"),
            new Stop(STOP_BAB_JEDID,         "Bab Jedid"),
            new Stop(STOP_HAY_HLEL,          "Hay Hlel"),
            new Stop(STOP_CITE_DES_SCIENCES, "Cité des Sciences"),
            new Stop(STOP_KHEREDDINE,        "Khereddine"),
            new Stop(STOP_LAOUINA,           "L'Aouina"),
            new Stop(STOP_TUNIS_MARINE,      "Tunis Marine"),
            new Stop(STOP_LA_GOULETTE_VX,    "La Goulette Vieille"),
            new Stop(STOP_LA_GOULETTE_NV,    "La Goulette Neuve"),
            new Stop(STOP_CARTHAGE_SALAMMBO, "Carthage Salammbô"),
            new Stop(STOP_CARTHAGE_HANNIBAL, "Carthage Hannibal"),
            new Stop(STOP_SIDI_BOU_SAID,     "Sidi Bou Said"),
            new Stop(STOP_LA_MARSA,          "La Marsa"),
            new Stop(STOP_BAB_BHAR,          "Bab Bhar"),
            new Stop(STOP_BAB_EL_KHADRA,     "Bab El Khadra"),
            new Stop(STOP_BARDO,             "Bardo"),
            new Stop(STOP_MANOUBA,           "Manouba")
        );
    }

    // ─── Lines ──────────────────────────────────────────────────────────────────

    private static List<TransportLine> buildLines() {
        return Arrays.asList(
            new TransportLine(LINE_METRO_L1, "metro_l1", "Métro Ligne 1", TransportType.METRO, "#4CAF50"),
            new TransportLine(LINE_METRO_L2, "metro_l2", "Métro Ligne 2", TransportType.METRO, "#F44336"),
            new TransportLine(LINE_METRO_L3, "metro_l3", "Métro Ligne 3", TransportType.METRO, "#2196F3"),
            new TransportLine(LINE_TGM,      "tgm",      "TGM",           TransportType.TRAIN, "#9C27B0"),
            new TransportLine(LINE_BUS_5,    "bus_5",    "Bus Ligne 5",   TransportType.BUS,   "#FF9800"),
            new TransportLine(LINE_BUS_50,   "bus_50",   "Bus Ligne 50",  TransportType.BUS,   "#FF5722")
        );
    }

    // ─── Line Stops ─────────────────────────────────────────────────────────────

    private static List<LineStop> buildLineStops() {
        List<LineStop> list = new ArrayList<>();

        // Metro Ligne 1: République → Ben Arous
        // Avg travel time between stops: 2–3 min
        addStops(list, LINE_METRO_L1,
            STOP_REPUBLIQUE,  0,
            STOP_BARCELONE,   2,
            STOP_BAB_SAADOUN, 2,
            STOP_MONTPLAISIR, 3,
            STOP_QURTABA,     2,
            STOP_MOHAMEDIA,   2,
            STOP_BEN_AROUS,   3
        );

        // Metro Ligne 2: République → El Ghazala
        addStops(list, LINE_METRO_L2,
            STOP_REPUBLIQUE,     0,
            STOP_PALESTINE,      2,
            STOP_CITE_OLYMPIQUE, 3,
            STOP_BOUCHOUCHA,     2,
            STOP_ARIANA,         3,
            STOP_EL_GHAZALA,     3
        );

        // Metro Ligne 3: République → L'Aouina
        addStops(list, LINE_METRO_L3,
            STOP_REPUBLIQUE,        0,
            STOP_BAB_ALIOUA,        2,
            STOP_BAB_JEDID,         2,
            STOP_HAY_HLEL,          2,
            STOP_CITE_DES_SCIENCES, 3,
            STOP_KHEREDDINE,        3,
            STOP_LAOUINA,           3
        );

        // TGM: Tunis Marine → La Marsa
        addStops(list, LINE_TGM,
            STOP_TUNIS_MARINE,      0,
            STOP_LA_GOULETTE_VX,    3,
            STOP_LA_GOULETTE_NV,    2,
            STOP_KHEREDDINE,        3,
            STOP_CARTHAGE_SALAMMBO, 3,
            STOP_CARTHAGE_HANNIBAL, 2,
            STOP_SIDI_BOU_SAID,     4,
            STOP_LA_MARSA,          4
        );

        // Bus Ligne 5: Bab Bhar → Manouba
        addStops(list, LINE_BUS_5,
            STOP_BAB_BHAR,       0,
            STOP_BAB_EL_KHADRA,  5,
            STOP_CITE_OLYMPIQUE, 8,
            STOP_BARDO,          10,
            STOP_MANOUBA,        12
        );

        // Bus Ligne 50: Bab Bhar → Ariana
        addStops(list, LINE_BUS_50,
            STOP_BAB_BHAR,       0,
            STOP_BAB_SAADOUN,    10,
            STOP_CITE_OLYMPIQUE, 8,
            STOP_ARIANA,         12
        );

        return list;
    }

    /**
     * Convenience helper: adds consecutive (stopId, travelTime) pairs for a line.
     * Parameters after lineId must be alternating (stopId, travelTime) pairs.
     */
    private static void addStops(List<LineStop> list, int lineId, int... stopIdAndTimes) {
        for (int i = 0; i < stopIdAndTimes.length; i += 2) {
            int stopId   = stopIdAndTimes[i];
            int travelTime = stopIdAndTimes[i + 1];
            int seq = (i / 2) + 1;
            list.add(new LineStop(lineId, stopId, seq, travelTime));
        }
    }
}
