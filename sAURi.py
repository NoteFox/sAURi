#!/usr/bin/python3


import difflib  # to find closest questioned package
import re  # url and name checking
import requests  # link_up test
import wget  # wget the pgk
import os  # os for directory checking
import tarfile  # extraction of pkg
import subprocess  # execution of package installation
import aur  # aur api for package searching
import sys  # args listing

from tqdm import tqdm  # tar extraction progress bar

directDownloadPath = "/home/note/Downloads/Compressed"  # path to first pkg download
packageInstallPath = "/home/note/Downloads/Programs"  # path to extraction dir

# pattern for url checking
url_existence_pattern = re.compile("^(https://aur.archlinux.org/cgit/aur.git/snapshot/)")
# file name extraction
file_name_pattern = re.compile(r'(/snapshot/)(.)*$')


# url checker
def is_pgk_url(string):
    if len(url_existence_pattern.findall(string)) == 0 or requests.get(string).status_code != 200:
        return False
    return True


# selector for different found pkg over the aur api
def selectOutOfList(title, listing, pkg_dict ,none_option):
    print(title)
    for i in range(len(listing)):
        print(str(i) + ")", listing[i], " | " + pkg_dict[listing[i]].description)
    if none_option:
        print("-1) none")
    selection = input("select -> ")

    try:
        if int(selection) == -1:
            return None

        return listing[int(selection)]
    except (IndexError, ValueError, TypeError) as err:
        print(err)
        exit(1)


# getting the pkg name over the url
def get_package_name(_url):
    for i in file_name_pattern.finditer(_url):
        return i.group()[10:]


# decompression of pkg file
def decompress(tar_file, path, members=None):
    """
    Extracts `tar_file` and puts the `members` to `path`.
    If members is None, all members on `tar_file` will be extracted.

    code copied from: https://www.thepythoncode.com/article/compress-decompress-files-tarfile-python
    """
    tar = tarfile.open(tar_file, mode="r:gz")
    if members is None:
        members = tar.getmembers()
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        tar.extract(member, path=path)
        # set the progress description of the progress bar
        progress.set_description(f"Extracting {member.name}")
    # or use this
    # tar.extractall(members=members, path=path)
    # close the file
    tar.close()


# installation process for a given pkg url
def install(aur_link):
    if not is_pgk_url(aur_link):
        print(aur_link, "isn't a package, or can't be called")
        exit(1)

    if not os.listdir(directDownloadPath).__contains__(get_package_name(aur_link)):
        print("downloading package...")
        file_name = wget.download(aur_link, out=directDownloadPath)
    else:
        print(get_package_name(aur_link), "already found, not downloading it again")
        file_name = directDownloadPath + "/" + get_package_name(aur_link)

    if not os.listdir(packageInstallPath).__contains__(get_package_name(aur_link).replace(".tar.gz", "")):
        decompress(file_name, packageInstallPath)
    else:
        print("already decompressed package found, will not be overwritten")

    print("installing package now")
    os.chdir(packageInstallPath + "/" + get_package_name(aur_link).replace(".tar.gz", ""))
    print(subprocess.call(["makepkg", "-si"]))


# installing aur pkg by giving name
def installByName(name):

    pkg_dict = dict()

    for pkg in aur.search(name):
        pkg_dict[pkg.name] = pkg

    installing = selectOutOfList(title="multiple packages found\nwhich package do you want to install",
                                 listing=difflib.get_close_matches(name, pkg_dict.keys()),
                                 pkg_dict=pkg_dict,
                                 none_option=True)

    if installing is None:
        print("nothing selected, exiting")
        exit(0)
    else:
        install("https://aur.archlinux.org" + pkg_dict[installing].url_path)
        print(" -> done installing", pkg_dict[installing].name)


if __name__ == '__main__':

    if len(sys.argv) >= 2:

        for arg in sys.argv[1:]:
            if not is_pgk_url(arg):
                installByName(arg)
                pass
            else:
                install(aur_link=arg)
                print(" -> done installing", get_package_name(arg))

    else:
        print("no name or url given")

    # url = input("installer url -> ")
    # install(aur_link=url)
