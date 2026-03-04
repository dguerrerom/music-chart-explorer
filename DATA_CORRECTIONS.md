# Data Corrections

**Last updated:** March 03, 2026

## Purpose

This document records all errors detected in the chart JSON files and the corrections that were applied.

Although the original Billboard magazine archives are an invaluable source, some files contain transcription, OCR, scanning, or data-entry errors (e.g., duplicate positions, missing entries, incorrect rankings, or wrong metadata). These issues are systematically identified using the detection scripts and corrected after verification against the original printed magazine issues.

Documenting every change here ensures full transparency, reproducibility, and historical accuracy.

---

## Correction Log

Corrections are grouped by **date of correction** (newest first).

### 2026-03-03

**Chart:** Billboard Hot 100  
**Chart Date:** 1984-02-18  
**File:** `data/billboard/billboard-hot100/1984-02-18.json`  
**Source:** Manual verification against original magazine scan  
**Issue:** Duplicate `this_week` value at position 67 (two different songs incorrectly assigned the same rank — ties do not exist in official Billboard charts)

**Changes:**
- Removed duplicate entry at position 67 ("Remember The Nights" by The Motels)
- Moved "Remember The Nights" by The Motels to its correct position 87
- Change song name ""Remember The Nights" to "Remember The Night"
- "Looks That Kill" by Mötley Crüe remained at 67
- Reordered subsequent entries to restore proper ranking

**Replaced fields:**
- `this_week` changed from 67 to 87 for "Remember The Night" – The Motels

**Reference:**  
[Billboard Magazine – February 18, 1984](https://www.worldradiohistory.com/Archive-Billboard/80s/1984/Billboard-1984-02-18.pdf) (World Radio History)

---

**Chart:** Billboard Hot 100  
**Chart Date:** 1989-03-11  
**File:** `data/billboard/billboard-hot100/1989-03-11.json`  
**Source:** Manual verification against original magazine scan  
**Issue:** Duplicate `this_week` value at position 98 (two different songs incorrectly assigned the same rank — ties do not exist in official Billboard charts)

**Changes:**
- Removed duplicate entry at position 98 ("Shake For The Sheik" by The Escape Club)
- Moved "Shake For The Sheik" by The Escape Club to its correct position 99
- "Little Liar" by Joan Jett & The Blackhearts remained at 98
- Reordered subsequent entries to restore proper ranking

**Replaced fields:**
- `this_week` changed from 98 to 99 for "Shake For The Sheik" – The Escape Club

**Reference:**  
[Billboard Magazine – March 11, 1989](https://www.worldradiohistory.com/Archive-Billboard/80s/1989/Billboard-1989-03-11.pdf) (World Radio History)

---

### How to add a new correction

Copy the template below and place it at the top of the log (newest first):

```markdown
### YYYY-MM-DD

**Chart:** Billboard Hot 100 / Latin Songs / Dance Club Songs  
**Chart Date:** YYYY-MM-DD  
**File:** `data/.../YYYY-MM-DD.json`  
**Source:** [Verification method]  
**Issue:** Short description of the problem  

**Changes:**
- Bullet list of actions taken

**Replaced fields:**
- `field_name` (from X to Y for "Song Title" – Artist)

**Reference:**  
- Link or source name
```

---

**Note:** All corrections are performed manually and only after cross-checking the original printed magazine. Contributions with supporting evidence are welcome — feel free to open a Pull Request!
