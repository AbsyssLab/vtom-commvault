@echo OFF

rem Forces the use of West European Latin
chcp 1252 > nul

rem Include the PowerShell binary directory in the PATH
set PATH_PYTHON=C:\Users\Jdoe\AppData\Local\Programs\Python\Python311\
set PATH=%PATH_PYTHON%;%PATH%

call submit_aff.bat %*
echo _______________________________________________________________________
echo Start of execution ...
date /T
echo %time:~+0,8%
echo _______________________________________________________________________

rem Test Mode
if "%TOM_JOB_EXEC%" == "TEST" (
	echo Job execute in Test mode
	%ABM_BIN%\tsend -sT -r0 -m"Job finished (TEST mode)"
	%ABM_BIN%\vtgestlog
	goto FIN
)

echo.

rem :LAUNCH
echo %PATH_PYTHON%\python %ABM_BIN%\vtom-commvault_backup-jobs.py --host %1 --client %2 --backup-set %3 --port %4 --use-ssl %5 --subclient %6 --username %7 --password %8 --config-file %9 --check-interval %10 --timeout %11 --verbose %12
%PATH_PYTHON%\python %ABM_BIN%\vtom-commvault_backup-jobs.py --host %1 --client %2 --backup-set %3 --port %4 --use-ssl %5 --subclient %6 --username %7 --password %8 --config-file %9 --check-interval %10 --timeout %11 --verbose %12
set RETCODE=%ERRORLEVEL%
if %RETCODE% equ 0 goto FINISHED
goto ERROR

:ERROR
%ABM_BIN%\tsend -sE -r%RETCODE% -m"Job in error (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo End of execution
date /T
echo %time:~+0,8%
echo Exit [%RETCODE%] No acknowledgment
echo _______________________________________________________________________
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:FINISHED
%ABM_BIN%\tsend -sT -r%RETCODE% -m"Job finished (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo End of execution
date /T
echo %time:~+0,8%
echo Exit [%RETCODE%] Acknowledgement
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:END
