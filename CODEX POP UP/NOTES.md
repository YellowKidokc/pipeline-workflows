# Popup Hub Notes

This is the first CustomTkinter pass for a Stratum-style popup action hub.

## Classification Approach

- `safe`: read-only status checks, app launchers, or scripts with low side effects.
- `caution`: scripts that may create, move, scaffold, or alter files.
- `admin`: scripts that need elevation or change system settings.
- `destructive`: scripts that delete, uninstall, reboot, shut down, or clear data.

The first catalog intentionally starts with mostly safe entries from:

- `D:\DONT TOUCH BOOT UP\PowerShell-main\scripts`
- `D:\DONT TOUCH BOOT UP\Codex-Powershell_GUI`
- `D:\DONT TOUCH BOOT UP\Python-master`

`Python-master` is treated as a mixed archive. Add scripts there slowly after checking what they do.
