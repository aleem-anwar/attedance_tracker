# IIITP Attendance Tracker for CSE-SEC-A

A web app built with Python and Streamlit to help IIIT Pune students track their semester attendance, figure out how many classes they can safely skip to keep above 75%, and manage schedule updates.

---

## What It Does

* **Kinetic UI:** High-contrast dark mode interface with custom styling and a scrolling ticker for top-level stats.
* **Official Schedule Integration:** Built around the IIIT Pune academic calendar (Odd Semester running from August 20 to December 11, 2026) and the Section A timetable, accounting for holidays, mid-sems, and sports events[cite: 1, 2].
* **Batch Customization:** Choose between lab batches (`G1`, `G2`, `G3`) so your lab schedules match your actual timetable[cite: 2].
* **Absence-Based Logging:** It assumes you attend everything by default and only asks you to log days you skip, making it fast to update.
* **Skip Calculator:** Instantly shows your current percentage and how many skips you have left before hitting the 75% cutoff.
* **Role Management:** Separate views for students (attendance tracking, 80% warning alerts) and admins (canceling classes, adding extra lectures, viewing user lists).

---

## Disclaimer

> **Note:** This tool is meant for personal planning and estimation only. Because it relies on manual tracking and custom inputs, calculations might occasionally drift from official institute records. Do not rely entirely on this app for managing your official attendance requirements—always cross-check with official notices.

---

