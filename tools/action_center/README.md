# Pipeline Action Center

Double-click `ACTION_CENTER.bat` at the repository root. The desktop window:

- inventories every existing `.bat`, `.cmd`, and `.ps1` launcher without moving or deleting it;
- sorts launchers into readable categories and provides search;
- offers curated entries for workflows, Markdown combining, file grouping, and Excel conversion;
- lets you select a file, a folder, or both where an action supports them;
- previews the exact command and asks for confirmation before opening it in a separate console.

The action center is a launcher, not a replacement for the underlying tools. A discovered legacy launcher is deliberately shown with **no automatic input arguments**, so its original prompts keep working. File behavior (including overwrite, rename, move, or delete behavior) remains controlled by that tool; review its prompt and console output before proceeding.

To add a polished action, add an entry to `catalog.json`. Commands are arrays (not shell strings) and support `{python}`, `{powershell}`, `{file}`, and `{folder}`. Valid selection values are `none`, `file`, `folder`, and `file_and_folder`.

