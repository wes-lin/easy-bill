@echo off
SET ENV=..\env\Scripts\activate.bat

cd src

if exist %ENV% (
   echo 'env is exist' 
   call %ENV% 
)
py main.py
pause