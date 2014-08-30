#! /bin/bash

run_folder ()
{
  for i in {1..10}
  do
    echo "Attempt $i"
    python regions.py "$1"
  done
  find . -type d -empty -exec rmdir {} \;
}

run_folder 'Сибирский федеральный округ'
run_folder 'Центральный федеральный округ'
run_folder 'Автономная Республика Крым'
reboot
