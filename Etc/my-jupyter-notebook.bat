@ECHO OFF

REM my-jupyter-notebook
REM  Version: 0.1
REM    2022-03-23: CEF, inital version

echo MY-JUPYTER-NOTEBOOK launcher..

REM %windir%\System32\cmd.exe "/K" %HOMEPATH%\Anaconda3\Sc2 ripts\activate.bat %HOMEPATH%\Anaconda3 swmal
@CALL "%HOMEPATH%\Anaconda3\condabin\conda.bat" activate swmal %* 

REM note book start in this directory, you may change it:
cd \

jupyter-notebook 

echo DONE