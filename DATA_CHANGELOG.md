# Data Changelog

All notable corrections to the chart JSON data.

This file follows [Keep a Changelog](https://keepachangelog.com/) conventions.

## [Unreleased]

## [2026-03-06] - 2026-03-06

### Fixed

- **Billboard Latin Songs** — multiple charts fixed for weekly consistency:
  - 1987-10-03 → 1987-10-10 → 1987-10-17
  - 1988-03-05 → 1988-03-12 → 1988-03-19 → 1988-03-26 → 1988-04-02 → 1988-04-09 → 1988-04-16
  - 1988-05-07 → 1988-05-14 → 1988-05-21 → 1988-05-28
  - 1988-06-04 → 1988-06-11 → 1988-06-18
  - 1988-07-16 → 1988-07-23 → 1988-07-30
  All `last_week` values now correctly match the previous chart’s `this_week` for every song.

**Reference:** [Billboard – 1988-06-04](https://www.worldradiohistory.com/Archive-Billboard/80s/1989/Billboard-1988-06-04.pdf)

## [2026-03-03] - 2026-03-03

### Fixed

- **Billboard Hot 100 – 1984-02-18** (`data/billboard/billboard-hot100/1984-02-18.json`)  
  Duplicate `this_week` at position 67.  
  Removed erroneous duplicate entry ("Remember The Nights" by The Motels).  
  Moved correct entry to position 87 and fixed song title from "Remember The Nights" to "Remember The Night".  
  "Looks That Kill" by Mötley Crüe stayed at 67.  
  **Reference:** [Billboard – 1984-02-18](https://www.worldradiohistory.com/Archive-Billboard/80s/1984/Billboard-1984-02-18.pdf)

- **Billboard Hot 100 – 1989-03-11** (`data/billboard/billboard-hot100/1989-03-11.json`)  
  Duplicate `this_week` at position 98.  
  Removed erroneous duplicate entry ("Shake For The Sheik" by The Escape Club).  
  Moved correct entry to position 99.  
  "Little Liar" by Joan Jett & The Blackhearts stayed at 98.  
  **Reference:** [Billboard – 1989-03-11](https://www.worldradiohistory.com/Archive-Billboard/80s/1989/Billboard-1989-03-11.pdf)