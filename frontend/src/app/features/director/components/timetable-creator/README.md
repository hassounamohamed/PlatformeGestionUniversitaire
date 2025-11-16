Timetable Creator
=================

Small in-app timetable creator used by the director. Features:

- Drag & drop palette of subjects into day/time cells (Angular CDK DragDrop)
- Save timetable locally via `TimetableCreatorService`
- Route: `/director/timetable/create` (reachable from "Nouvel Emploi du Temps" button)

Notes
-----
- This component is intentionally lightweight; integrate server-side save via `DirectorService.createTimetable` when ready.
- Styling is inspired by the Docendo UI but implemented here with original CSS and transitions.
