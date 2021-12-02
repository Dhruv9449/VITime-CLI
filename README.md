# VITime
CLI tool to view your timetable from terminal anytime!

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-blue.svg" alt="built with Python3" /></a>
<a href="https://badge.fury.io/py/vitime"><img src="https://img.shields.io/pypi/v/vitime?color=blue&label=pypi%20package" alt="PyPI version" height="18"></a>


## Preview

![VITime](/assets/VITime.gif)




## Installation
### PyPI
Open terminal and install the package using python package installer.
```sh
pip install vitime
```
### Source code
- Download latest release via [zip file](https://github.com/Dhruv9449/VITime-CLI/archive/refs/tags/v0.0.1.zip) or [tar file](https://github.com/Dhruv9449/VITime-CLI/archive/refs/tags/v0.0.1.tar.gz)
- Extract the folder to your desired location
- Then install it in your desired terminal using suitable command
#### Linux or Max OS X
```sh
user@hostname:~$ sudo python3 setup.py install
```
#### Windows
Run command prompt as administrator and
```psh
C:\users\username> python setup.py install
```



## Setting up
### Commands
#### `vitime timetable`

Command to add entire timetable.  
> **Note:** This deletes any existing timetable.  
<p>
1. Copying timetable from vtop  

![copying timetable](/assets/copying_timetable.gif)</p>   

<p>
2. Adding timetable using VITime  

![vitime addtimetable](/assets/vitime_addtimetable.gif)</p>


#### `vitime addcourse`

Command to add a course.

![vitime addcourse](/assets/vitime_addcourse.gif)



## Usage
### Commands
#### `vitime today`  

Shows all ongoing/left classes for the day.  
> **Note:** This does not show all the classes during the day, to view all classes use `vitable showday` command.

![vitime today](/assets/vitime_today.gif)

#### `vitime showday`

Shows all the classes on the day entered by the user.

![vitime showday](/assets/vitime_showday.gif)

#### `vitime full`

Shows the entire timetable.

![vitime full](/assets/vitime_full.gif)

#### `vitime deletecourse`

Deletes the given course from timetable.

![vitime deletecourse](/assets/vitime_deletecourse.gif)


#### `vitime deletetimetable`

Deletes the entire timetable.  
> **Note:** The confirmation message is case sensitive so 'YES', 'Yes' will not work.

![vitime deletetimetable](/assets/vitime_deletetimetable.gif)



## License
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/Dhruv9449/VITime-CLI/blob/main/LICENSE)  

Copyright (c) 2021 Dhruv9449  
[MIT license](LICENSE)

<br>
<br>

<p align="center">
Developed by <a href="https://github.com/Dhruv9449" target=_blank>Dhruv Shah</a>
</p>
