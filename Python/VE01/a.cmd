@echo.
@echo Set str var
@set str=%*
@echo.
@echo Echo raw command string
@echo "C:\Users\ssimha\AppData\Local\Google\Chrome\Application\chrome.exe" "%str:chm:=%"
@echo.
@echo %%*
@echo "%*"
@pause
@"C:\Users\ssimha\AppData\Local\Google\Chrome\Application\chrome.exe" "%str:chm:=%"
