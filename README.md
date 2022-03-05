# sAURi
simple AUR installer for arch based os-s, written in Python (needs pip3)

used python packages:
```
 - difflib      # to find closest questioned package
 - re           # url and name checking
 - requests     # link_up test
 - wget         # wget the pgk
 - os           # os for directory checking
 - tarfile      # extraction of pkg
 - subprocess   # execution of package installation
 - aur          # aur api for package searching
 - sys          # args listing
 - tqdm         # tar extraction progess bar
```

installing locally:
```bash
curl https://raw.githubusercontent.com/NoteFox/sAURi/main/install_locally.sh | bash
exec $SHELL
```
(Since the AUR library, that sAURi uses has some problems at the moment, searching by name is not available, you can only install by url, which can be found on the aur online (right click on 'download snapshot' and copy the link))

warnings: 
 - reinstalation/update can be done by just running the installation script again (no need for manual reinstalatoin for)
 - installer is creating an alias in your shell config file!
 - the python file can be found in /opt/sauri 
 - the alias is called "sauri"
 - these two things need to be removed when removing

how to use:
```
sauri <package url>
# example: sauri https://aur.archlinux.org/cgit/aur.git/snapshot/hello.tar.gz
```

