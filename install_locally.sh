#!/bin/bash

alias="alias sauri='python3 /opt/sauri/sAURi.py'"

# hceking if directory exists
if [ ! -d "/opt/sauri" ]; then
  echo "creating dir"
  sudo mkdir /opt/sauri
fi

curl "https://raw.githubusercontent.com/NoteFox/sAURi/main/sAURi.py" | sudo tee /opt/sauri/sAURi.py 1>/dev/null
curl "https://raw.githubusercontent.com/NoteFox/sAURi/main/scripts/install_pips.sh" | sudo tee /opt/sauri/install_pips.sh 1>/dev/null

sudo chown $USER /opt/sauri/sAURi.py
sudo chown $USER /opt/sauri/install_pips.sh


# automatic config file detection directly copied from
# https://github.com/rbenv/rbenv/blob/master/libexec/rbenv-init
# Software licensed un the "MIT License"

shell="$1"
if [ -z "$shell" ]; then
  shell="$(ps -p "$PPID" -o 'args=' 2>/dev/null || true)"
  shell="${shell%% *}"
  shell="${shell##-}"
  shell="${shell:-$SHELL}"
  shell="${shell##*/}"
  shell="${shell%%-*}"
fi

case "$shell" in
bash )
  if [ -f "${HOME}/.bashrc" ] && [ ! -f "${HOME}/.bash_profile" ]; then
    profile="$HOME/.bashrc"
  else
    profile="$HOME/.bash_profile"
  fi
  ;;
zsh )
  profile="$HOME/.zshrc"
  ;;
ksh )
  profile="$HOME/.profile"
  ;;
fish )
  profile="$HOME/.config/fish/config.fish"
  ;;
esac

# -- copy end --

if grep -Fxq "$alias" "$profile"
then
    echo "alias already exists"
else
    echo "$alias" | sudo tee -a "$profile" >/dev/null
    echo "alias added to $profile"
fi

exec $SHELL
