# Music Chart Explorer

**A clean, modular Python toolkit to explore decades of music chart history.**

Search for chart anniversaries, full song histories, songs that reached the Top 10 in any period, and more — all from local JSON archives.

Built for music lovers, chart historians, and data enthusiasts who want fast, accurate answers without scraping or APIs.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ Features

- **Anniversary Search** — Find what was #1 (or any position) exactly X years ago this week
- **Song Chart History** — Complete run of any song across any chart (peak, weeks, every date)
- **Position Range Search** — Discover all songs that hit the Top 10, Top 5, etc. in a given time span
- **Multi-Chart Support** — Works with Billboard Hot 100, Latin, Dance/Club, and any future charts you add
- Fully modular & extensible — easy to add new scripts and new chart archives

---

## 📁 Project Structure

```
music-chart-explorer/
├── data/                    # ← Put your chart JSON files here
│   ├── billboard-metadata.json
│   ├── billboard/
│   │   ├── billboard-hot-100/
│   │   └── ...
│   └── ...
├── scripts/                 # All Python tools
│   ├── anniversary_search.py
│   ├── song_chart_history_search.py
│   ├── songs_in_position_range_search.py
│   ├── chart_discovery.py
│   ├── data_handler.py
│   ├── time_engine.py
│   ├── chart_format.py
│   └── json_beautifier.py
└── ...
```

---

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/YOURUSERNAME/music-chart-explorer.git
   cd music-chart-explorer
   ```

2. Place your chart JSON files inside the `data/` folder (following the structure shown above).

3. Run any script directly:
   ```bash
   python scripts/anniversary_search.py
   ```

   or

   ```bash
   python scripts/song_chart_history_search.py
   ```

---

## 📋 Supported Charts (example)

- **Billboard Hot 100** (1980–1989)
- **Billboard Latin Songs**  (1986–1989)
- **Billboard Dance/Club Play Songs** (1980–1989)

*More charts and international lists coming soon — just drop in a new `-metadata.json` and the corresponding date-based JSON files.*

---

## 🛠️ Adding New Charts (Future-proof)

1. Create a new folder inside `data/` (e.g. `uk-singles`)
2. Add a `uk-singles-metadata.json` (see `billboard-metadata.json` for format)
3. Place your `YYYY-MM-DD.json` files in the chart subfolder
4. Run any script — everything works automatically

---

## Acknowledgements

This project is built on the excellent open-source foundations provided by:

- **[Michael Hollingshead](https://github.com/mhollingshead)** — [billboard-hot-100](https://github.com/mhollingshead/billboard-hot-100)  
  (standardized JSON chart format)

- **[Mykhailo Dorokhin](https://github.com/adjorno)** — [billibdata](https://github.com/adjorno/billibdata)  
  (chart data structure and metadata format)

Thank you both.

---

## Roadmap

- More built-in queries (e.g. artist career overview, #1 streaks, debut dates)
- Optional web interface (Streamlit/Gradio)
- Support for Spotify, Apple Music, and official archive formats
- Export to CSV / Excel

---

## Contributing

See CONTRIBUTING.md for details on how to contribute.

---

**Made with ❤️ for music chart nerds everywhere.**

Star ⭐ the repo if you find it useful, and feel free to open issues or pull requests!