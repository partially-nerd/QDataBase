# QDataBase
A file handling service for _**Linux**_ that allows for the conversion between a custom .fs file to a Python dictionaries, and vice-versa.

QDataBase (QDB for short) uses the Python3 bindings of GTK4 for its interface, and provides syntax highlighting, live conversion to Python dictionaries, and setting of keys via an easy syntax

# Documentation
## Dependencies
- python-dotenv
- pgi (PythonGObject)
- passlib
- munch

Install dependencies with `pip3 install python-dotenv passlib munch`

## Interface
![interface](https://github.com/partially-nerd/QDataBase/assets/108736691/ea6dad75-e9de-4146-8b2e-fa4d41f5d0f5)


## Launching the service
You can start the interface with: `python3 gui`

_By Default,_
_Username: `Admin`_
_Passphrase: `Troy8848$`_

Once logged in, you'll be asked to select a database folder, which, once selected, you'll be taken to the main interface

In the sidebar, serially, you can
- Close the window
- Create a new file
- Save a backup of the active file
- Save changes in the active file
- Delete the active file

In the explorer tab, the files and folders in the database folder are listed

In the workspace, you can edit the active file, and view the changes made to it

In the statusbar, serially, you can:
- View the active file name
- Locate a key in the file
- Get the value of a key
- Set the value of a key

## Examples
Locate the line with the prefect of rose 10, by locating for `sections.rose.classPrefect`. It'll highlight the line in red, until you press a key

Get the name of the prefect of rose 10, by entering `sections.rose.classPrefect` in the `Key` field of the statusbar. It'll set the value of the `Value` field to the value of the key

Set the name of the prefect of rose 10, by entering `sections.rose.classPrefect` in the `Key` field, and `Avinav Chalise` in the `Value` field of the statusbar

Backup `Grade 10.fs` by clicking the copy button in the left-bar

## .FS File Structure
```fs
{
    plantae: {
        divisions: {
            0: algae
            1: bryophyta
            2: {
                division: tracheophyta
                subdivisions: {
                    0: pteridophyta
                    1: gymnosperms
                    2: angiosperms
                }
            }
        }
    }
    animalia: {
        phylum: {
            0: coelenterata
            1: porifera
            2: echinodermata
        }
    }
}
```
kingdoms.fs
