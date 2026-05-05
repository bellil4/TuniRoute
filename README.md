# TuniRoute 🚌🚇🚆

**TuniRoute** is an Android application that helps users find optimal routes through the Tunis public transport network — including the **Métro Léger**, **TGM train**, and **bus lines**.

---

## Features

| Feature | Details |
|---------|---------|
| 🔍 Route Search | Enter any origin and destination stop to find the best route |
| 🔄 Multi-modal | Combines Metro, TGM train, and bus lines seamlessly |
| ⏱ Time Estimation | Estimates total travel time including waiting and transfer times |
| 🔁 Transfer Support | Handles up to 3+ line changes with walk/wait overhead |
| 📱 Modern UI | Material Design 3 with a clean card-based layout |
| 💾 Room Database | Transport data stored locally with Room; preloaded on first launch |
| 🏗 MVVM Architecture | Clean separation of concerns (ViewModel + Repository + Room) |

---

## Transport Data Included

### Métro Léger de Tunis
| Line | Route | Stops |
|------|-------|-------|
| **Ligne 1** (Green) | République → Ben Arous | 7 stops |
| **Ligne 2** (Red) | République → El Ghazala | 6 stops |
| **Ligne 3** (Blue) | République → L'Aouina | 7 stops |

### Train
| Line | Route | Stops |
|------|-------|-------|
| **TGM** (Purple) | Tunis Marine → La Marsa | 8 stops |

### Bus
| Line | Route | Stops |
|------|-------|-------|
| **Bus Ligne 5** (Orange) | Bab Bhar → Manouba | 5 stops |
| **Bus Ligne 50** (Deep Orange) | Bab Bhar → Ariana | 4 stops |

### Key Transfer Points
- **République** — Metro L1, L2, L3
- **Bab Saadoun** — Metro L1 ↔ Bus 50
- **Cité Olympique** — Metro L2 ↔ Bus 5 ↔ Bus 50
- **Khereddine** — Metro L3 ↔ TGM
- **Ariana** — Metro L2 ↔ Bus 50

---

## Architecture

```
com.tuniroute/
├── MainActivity.java
├── data/
│   ├── model/          # Room entities (Stop, TransportLine, LineStop)
│   ├── database/       # AppDatabase, DAOs, TypeConverters, DataInitializer
│   └── repository/     # TransportRepository
├── algorithm/
│   ├── RouteFinder.java   # Dijkstra-based route finder
│   ├── RouteResult.java
│   └── RouteStep.java
└── ui/
    ├── home/           # HomeFragment + HomeViewModel
    └── results/        # ResultsFragment + ResultsViewModel + RouteResultAdapter
```

**Architecture pattern:** MVVM (Model-View-ViewModel)  
**Database:** Room (SQLite)  
**Navigation:** AndroidX Navigation Component  
**UI:** Material Design 3, ViewBinding, RecyclerView

---

## Route-Finding Algorithm

The app uses **Dijkstra's algorithm** on a state-space graph:

- **Nodes:** each physical stop in the network  
- **Edges:** bidirectional connections between consecutive stops on each line  
- **State:** `(stopId, activeLineId)` — tracks which line the passenger is currently riding  
- **Transfer penalty:** 3 min walking + average wait time when switching lines  
- **Wait times:** Metro 5 min · Train 10 min · Bus 8 min  

Returns up to **3 route options**, sorted by fastest total time.

---

## Getting Started

### Prerequisites
- Android Studio Hedgehog (2023.1.1) or later
- Android SDK 21+
- Java 8+

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bellil4/TuniRoute.git
   cd TuniRoute
   ```

2. **Open in Android Studio**  
   File → Open → select the `TuniRoute` directory

3. **Build and run**  
   Connect a device or start an emulator, then click **Run ▶**

   Or via command line:
   ```bash
   ./gradlew assembleDebug
   ```

### First Launch
On the first app launch, Room automatically populates the database with the sample transport data (defined in `DataInitializer.java`). No internet connection is required.

---

## Usage

1. Open the app — you'll see the home screen with two input fields
2. Type the name of your **starting stop** (autocomplete will suggest matching stops)
3. Type the name of your **destination stop**
4. Tap **Find Route**
5. The results screen shows up to 3 route options with:
   - Transport lines used
   - Step-by-step directions (board at X → ride to Y)
   - Estimated travel time per segment
   - Total journey time and number of transfers

### Example Routes to Try
| From | To | Expected Route |
|------|----|---------------|
| Bab Bhar | République | Bus 50 → République |
| République | La Marsa | Metro L3 → TGM |
| Bab Bhar | Khereddine | Bus 50 + Metro L3 |
| Ben Arous | La Marsa | Metro L1 + Metro L3 + TGM |

---

## Extending the App

### Adding more transport lines
Edit `DataInitializer.java`:

```java
// 1. Add stop IDs and stop rows in buildStops()
new Stop(30, "New Stop"),

// 2. Add the line in buildLines()
new TransportLine(7, "bus_12", "Bus Ligne 12", TransportType.BUS, "#607D8B"),

// 3. Add line stops in buildLineStops()
addStops(list, 7,
    STOP_X, 0,
    30,     8   // New Stop, 8 min from prev
);
```

Then uninstall and reinstall the app to trigger `DataInitializer` again (Room `onCreate` only runs when the DB is first created).

### Adding a schedule feature
Extend `TransportLine` with departure times and modify the wait-time calculation in `RouteFinder` to use real schedules.

---

## License

This project is licensed under the MIT License.
