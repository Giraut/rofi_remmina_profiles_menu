#!/usr/bin/env python3

### Parameters
remmina_cfg = "~/.config/remmina/remmina.pref"
remmina_bin = "/usr/bin/remmina"



### Modules
import os
import re
import sys
import subprocess



### Main routine
def main():

  # Get the Remmina data directory path
  with open(os.path.abspath(os.path.expanduser(remmina_cfg)), "r") as f:
    for l in f.readlines():
      m = re.match(r"\s*datadir_path\s*=\s*(.*)$", l.rstrip())
      if m:
        datadir_path = os.path.abspath(os.path.expanduser(m[1]))

  # Parse the Remmina profiles in the directory path, extract their names
  profiles = {}
  for fpath in os.listdir(datadir_path):
    fpath = os.path.join(datadir_path, fpath)
    if os.path.isfile(fpath) and fpath.endswith(".remmina"):
      try:
        with open(fpath, "r") as f:
          for l in f.readlines():
            m = re.match(r"\s*name\s*=\s*(.*)$", l.rstrip())
            if m:
              profiles[m[1]] = fpath
      except:
        pass

  # If rofi passed a profile name as argument, start the corresponding profile
  if len(sys.argv) > 1 and sys.argv[1] in profiles:
    subprocess.Popen([remmina_bin, profiles[sys.argv[1]]],
			stdin=subprocess.DEVNULL,
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL)

  # Otherwise send the list of profile names to rofi
  else:
    for p in sorted(profiles):
      print(p)

  return 0



### Main program
if __name__ == "__main__":
  exit(main())
