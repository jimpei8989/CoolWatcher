# Cool Watcher

### Basic Requirements
- A chrome driver, try to find one. For MacOSX users, easy download with `brew cask install chromedriver`.
- `selenium==3.141.0`

### Basic Usage
```txt
usage: main.py [-h] [--courseId COURSEID] [--numWorkers NUMWORKERS]

optional arguments:
  -h, --help            show this help message and exit
  --courseId COURSEID
  --numWorkers NUMWORKERS
```
- courseId: find it on NTU Cool
- numWorkers: number of workers to play the videos (default 4)

### Secret
Place your username / password in a `secret.py` file. For example,
```python
username = 'b06902000' # this is not my username
password = 'abcdefghijk' # this is not my password
```

### Be careful!
- **Roughly** and only tested on my macOS.

### Some notes
You might notice that there are several sleeps in this script, the main reason is to avoid simultaneous connections, or things might mess up. You may tune the sleeping time for better performance :)

