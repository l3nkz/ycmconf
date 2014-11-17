My YCM Extra Configuration
=========================

As I don't like to have a ".ycm_extra_conf.py" for every project I am working on,
I decided to write a global configuration which is loaded for every project.


The main purpose of this file is to be able to serve as many projects as possible.
Therefore multiple formats to specify compiler flags are supported.


Supported Formats
================

1. Clang Compile Commands
-------------------------
A very powerful format is the clang compile commands database saved in a
"compile_commands.json". This is a file which can be generated for your
project using cmake. The file then contains for each source file (ending
on .c, .cpp or .cc) in your projects the exact flags to compile them.


2. Clang Complete
-----------------
As I previously used clang complete as completion plugin for VIM, I already had some
".clang_complete" files for my projects. These files are easy to parse because they
simply contain newline separated list of flags used to compile the project.


Parse Algorithm
================

This configuration file will try to search for the in the supported formats section specified
files. The search will start in the folder where the currently edited file is located. If none
of the configuration files are found, the parent directory is checked next. This continues
until the root directory of the file system. The algorithm will first look for the first format
and afterwards for the second one. If none of them are found a default list of flags is used.


Usage
=====

If you want to use this configuration file with your YCM plugin, copy the "ycm_extra_conf.py"
file to your preferred location and add the following option to your ".vimrc".

    let g:ycm_global_ycm_extra_conf = path_to_your_conf_here

And thats it. Now you can use the listed flag formats in your projects without any hassle.
