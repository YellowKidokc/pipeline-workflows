PORTABLE TTS - SIMPLE INSTRUCTIONS
==================================

FIRST TIME ON A COMPUTER
1. Double-click SETUP_OR_FIX.bat.
2. Wait until it says READY.

NORMAL USE
1. Put .txt or .md files into one of these permanent lanes:
   INBOX\PRIORITY  - always runs first
   INBOX\SERIES    - runs second
   INBOX\GENERAL   - runs last
2. Choose a launcher:
   RUN_TTS.bat          - 2 jobs at once; safest normal choice
   RUN_TTS_FAST_4X.bat  - 4 jobs at once
   RUN_TTS_MAX_5X.bat   - 5 jobs at once
3. Find the MP3 files in OUTBOX.

You can also drag one .txt or .md file, or an entire folder, onto RUN_TTS.bat.

MOVING IT
Move or copy the entire PORTABLE_TTS folder anywhere. The scripts find their
own location automatically. The .venv folder can usually move with it on the
same computer. On another computer, run SETUP_OR_FIX.bat again.

TROUBLESHOOTING
Double-click TROUBLESHOOT.bat. It creates TTS_DIAGNOSTIC.txt, which can be
shared for diagnosis. SETUP_OR_FIX.bat is safe to rerun.

NOTES
- Uses Microsoft's free Edge voices and therefore needs internet access.
- Default voice: en-US-BrianMultilingualNeural at +6% speed.
- Original text files are never moved, deleted, or overwritten.
- Existing MP3 files are not overwritten; a numbered copy is created.
- Nested INBOX folders are preserved under OUTBOX.
- Each lane finishes before the next lane starts; files within that lane run
  simultaneously. More workers usually helps, but internet limits can make 5
  workers less reliable than 4.
