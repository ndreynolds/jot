todo
==================================================================================
todo is a lightweight, CLI To-Do List Manager built with Python and SQLite.
It offers Git-like commands and methods for de-centralized synchronization, while
providing expected features and a few new ones, like search and using configurable
editors.


Installation
----------------------------------------------------------------------------------
It's as simple as cloning the repository and running the install script.

### Requirements: ###
--A unix-like OS (No Windows support yet)
--Python 2.5+ and a few modules from its standard library

### Installing: ###
Clone the Repository
`git clone https://github.com/ndreynolds/todo`
Step inside the new todo directory
`cd todo`
Run the installation script
`python setup.py`
If this fails (most likely because your user does not have permission to copy to /usr/local/bin),
the script may need to be run as root, as shown below:
`sudo python setup.py`
If everything checks out, the installation was successful.

Getting Started
----------------------------------------------------------------------------------
todo uses Git-like commands and parameters. The program is called with `todo` followed by
whitespace and a command.  Here's a short tutorial to get started:

### Adding a new item ###
todo creates, manages, and destroys items.  These items have an identifier, timestamp, priority,
group and content. Let's create a new one:

`todo add` 

This will open your default editor and allow you to enter a message. After typing a short message,
save the file and exit the editor.  The program now displays what was added.  Try adding a few more
items.

* Using the -m flag followed by a string (encapsulated with quotation marks when there's whitespace), adds an
item manually, without opening the editor.

### Editing an item ###

Suppose you forgot to add something to the last message, or wanted to update it later.  Let's edit the last item.
To perform an action on an existing item, we need a way to reference it.  Each item has an identifier (an MD5 hash)
for this reason. You only need to enter as many characters of the identifier as are neccessary to uniquely identify
it to an item. This is rarely more than 4 or 5. 

`todo edit [identifier]`

Items can also be acted on using 'last' in place of an identifier.

`todo edit last`

### Removing an item ###

Sometimes it's neccessary to remove an item--obliterating it from record. Like with edit, we can reference an item
to remove with its identifer or using 'last' like so:

`todo remove [identifier]`

`todo remove last`

Remove also allows the 'all' argument.  This will remove all items.

`todo remove all`

### Displaying items ###

The 'show' command is used to display items.  It does not require a reference to an item, although one is allowed.
The base command will show the five most-recently added items, like so:

`todo show`

If you want to display a specific item, it can be referenced as in the 'remove' and 'edit' commands.

`todo show [identifier]`

`todo show last`

Likewise, to show all items:

`todo show all`

### Syncing with a Peer ###

A peer is any remote installation of todo that is pushed to, pulled from, or cloned from. These operations are all
very simple.  todo just uses scp (which in turn is using ssh) to securely copy log files.  This requires that the remote
machine be accessible via ssh, you have access (via the password or a keyfile), and that todo is already installed on the machine.

There are three commands to interact with a peer:

* push - pushes LOCAL changes to the peer.

* pull - pulls LOCAL changes from the peer.

* clone - makes the local installation identical to the peer.

Local is the most important word above.  Pushes and pulls don't include changes made from other pushes and pulls.  To get those
changes, you would need to pull from where they got them.  Clones work differently, you'll get an exact copy of the peer, but this
also removes anything unique to the local installation.

The 'push', 'pull', and 'clone' commands all require a reference to a peer.  The reference can be anything that ssh will accept.
Some examples:

`todo push ndreynolds@ndreynolds.com`

`todo pull serenity` - where 'serenity' is defined in /etc/hosts

`todo clone 192.168.2.5` - will try to log in using current username
