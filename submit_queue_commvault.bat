@echo OFF

rem Force l'utilisation West European Latin
chcp 1252 > nul

rem Inclut le repertoire binaire powershell dans le path
set PATH_PYTHON=C:\Users\Jdoe\AppData\Local\Programs\Python\Python311\
set PATH=%PATH_PYTHON%;%PATH%

call submit_aff.bat %*
echo _______________________________________________________________________
echo Debut de l'execution ...
date /T
echo %time:~+0,8%
echo _______________________________________________________________________

rem Mode TEST
if "%TOM_JOB_EXEC%" == "TEST" (
	echo Job execute en mode TEST
	%ABM_BIN%\tsend -sT -r0 -m"Traitement termine (mode TEST)"
	%ABM_BIN%\vtgestlog
	goto FIN
)

echo.

rem :LAUNCH
echo %PATH_PYTHON%\python %ABM_BIN%\vtom-commvault_backup-jobs.py --host %1 --client %2 --backup-set %3 --port %4 --use-ssl %5 --subclient %6 --username %7 --password %8 --config-file %9 --check-interval %10 --timeout %11 --verbose %12
%PATH_PYTHON%\python %ABM_BIN%\vtom-commvault_backup-jobs.py --host %1 --client %2 --backup-set %3 --port %4 --use-ssl %5 --subclient %6 --username %7 --password %8 --config-file %9 --check-interval %10 --timeout %11 --verbose %12
set RETCODE=%ERRORLEVEL%
if %RETCODE% equ 0 goto TERMINE
goto ERREUR

:ERREUR
%ABM_BIN%\tsend -sE -r%RETCODE% -m"Traitement en erreur (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo Fin d'execution
date /T
echo %time:~+0,8%
echo Exit [%RETCODE%] donc pas d'acquittement
echo _______________________________________________________________________
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:TERMINE
%ABM_BIN%\tsend -sT -r%RETCODE% -m"Traitement termine (%RETCODE%)"
%ABM_BIN%\vtgestlog
echo _______________________________________________________________________
echo Fin d'execution
date /T
echo %time:~+0,8%
echo Exit [%RETCODE%] donc acquittement
if not "%TOM_LOG_ACTION%"=="   " call Gestlog_wnt.bat
exit %RETCODE%

:FIN
