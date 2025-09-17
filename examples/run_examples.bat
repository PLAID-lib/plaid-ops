@echo off
for %%f in (mesh\*.py) do (
  echo --------------------------------------------------------------------------------------
  echo #---# run python %%f
  python %%f || exit /b 1
)