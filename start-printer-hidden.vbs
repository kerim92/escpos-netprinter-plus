Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & WScript.ScriptFullName & "\..\start-printer.bat" & chr(34), 0
Set WshShell = Nothing
