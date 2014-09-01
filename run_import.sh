 #! /bin/bash

run_folder_regions ()
{
  for i in {1..10}
  do
    echo "Attempt $i"
    python regions.py "$1"
  done
  find . -type d -empty -exec rmdir {} \;
}

run_folder_millionniki ()
{
  for i in {1..10}
  do
    echo "Attempt $i"
    python millionniki.py "$1"
  done
  find . -type d -empty -exec rmdir {} \;
}


run_folder_millionniki
