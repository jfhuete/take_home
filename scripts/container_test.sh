#!/bin/bash

python manage.py test --keepdb -v2

TESTS_RESULT=$?

echo "================================================================================"
echo "Running flake8"
flake8 .
FLAKE8_RESULT=$?
if [ "$FLAKE8_RESULT" -eq "0" ]; then
   echo "==========> FLAKE8 PASSED";
fi
echo "================================================================================"

if [ "$TESTS_RESULT" -ne "0" ] || [ "$FLAKE8_RESULT" -ne "0" ]; then
   echo "==========> TEST FAILED";
else
   echo "==========> TEST PASSED";
fi
