Jot
==================================================================================
Put simply, Jot is a little console app for jotting down notes while in the shell.

In a few more words, Jot is a lightweight, command-line, note manager built with 
Python and SQLite, offering Git-like commands and methods for de-centralized 
synchronization, while providing all the expected features of a note manager, plus 
a few new ones.

Installation
----------------------------------------------------------------------------------

Using Jot requires a Python interpreter (preferably between 2.5 and 2.7). It's 
been tested on OSX 10.6.7 and Ubuntu 10.10, though it will probably work on most
*nixes.

To install, clone the repo and run the setup.py:

    $ git clone https://github.com/ndreynolds/jot
    $ python setup.py

This might fail if the account you're using doesn't have write access to the default
install path, `/user/local/bin`. You can run the command as root or you can use the
`--path` flag and supply another path. Maybe something like this:

    $ python setup.py --path ~/bin


Getting Started
----------------------------------------------------------------------------------

The command structure of Jot is very similar to Git's. You won't be managing any
repositories, but much of it is the same.


To add a new note:

    $ jot add

This opens a text editor--if available, the one specified in your shells $EDITOR
variable--with a temp file. If you save the file, Jot captures its contents and
saves the text in its database. Just like a commit message in Git, if you quit without
saving, it aborts.

To show recent notes:

    $ jot show

This command shows the last 5 notes. Of course, if you have fewer that 5, it will only 
show those.

Jot's notes are identified by MD5 hashes. You can always use this identifier to 
reference a note with commands that accept a reference (edit,show,tag,remove).
Jot also supports a number of keywords like `last`, `last^`, and `all`.  See the 
documentation for more info.

We can then edit the last note with either of the below:

    $ jot edit last
    $ jot edit [identifier]

You can search your notes for keywords or phrases with the `search` command. To search
for the word 'meeting':

    $ jot search meeting

Phrases that include spaces are possible too, just quote them so your shell doesn't get
confused:
    
    $ jot search "My dog skip"

If you have Jot installed on multiple machines, you can easily synchronize them. The
docs cover this in depth, but here are a few quick commands:

    $ jot pull ndreynolds@ndreynolds.com
    $ jot push ndreynolds@ndreynolds.com
    $ jot clone ndreynolds@ndreynolds.com

See the full documentation (doc/jot.txt) for  way more options. 
