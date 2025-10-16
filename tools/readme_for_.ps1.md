This is the command to use within powershell to quickly make a colapsible html document for review. Note this will overwrite files, so make sure the files you want to keep do not match the same file name.

powershell -NoProfile -ExecutionPolicy Bypass -File "c:\workspace\github.com\concrete_calcs\data\export_with_collapsible.ps1" -notebook "..\shear_moment_diagram.ipynb" 