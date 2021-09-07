# ID3 Editor
![OpenSource](https://img.shields.io/badge/Open%20Source-%E2%99%A5-red)
![Apache 2.0](https://img.shields.io/github/license/dan-sazonov/id3-editor)
![Tested on linux, Win10](https://img.shields.io/badge/tested%20on-Linux%20|%20Win10-blue)<br>

**The simplest console tool for batch editing of mp3 metadata in interactive or manual mode**

## 📦 Installation
Clone this repo, change the directory and install the necessary requirements:
```
$ git clone https://github.com/dan-sazonov/id3-editor.git
$ cd id3-editor
$ python3 -m pip install -r requirements.txt
```
_note: you may need to enter_ `python` _instead of_ `python3`.<br>
The program was tested on Win10 x64 and Ubuntu 20.04 x64 on Python 3.9.0. I do not know if everything will work fine on other os, and it will be great if you share
your experience of using it and tell me about the found bugs.

## ⚙ Usage
The easiest way to start is just:
```
$ python3 main.py
```
After that, you will be asked to enter the path to directory where the tracks need to be edited. Then change the value of each parameter for each file. If you want to
apply the value from the brackets, just press [Enter]. It looks like this:
<p align="center"><img src="./img/demo1.png" width="555" height="253"></p>

<h3>Default Parameters</h3>
If there is a same values for each tracks in this folder, you can predefine it by specifying one of the flags when starting the program (see below). The value of this
parameter will be asked once at start, and will be applied to all tracks. It looks like this:
<p align="center"><img src="./img/demo2.png" width="556" height="373"></p>
<details> 
  <summary><b>Flags:</b></summary>
  <ul>
    <li><code>'-T', '--title'</code> - set a title for all tracks;</li>
    <li><code>'-R', '--artist'</code> - set an artist for all tracks;</li>
    <li><code>'-A', '--album'</code> - set an album for all tracks;</li>
    <li><code>'-N', '--number'</code> - set a number for all tracks;</li>
    <li><code>'-G', '--genre'</code> - set a genre for all tracks;</li>
    <li><code>'-D', '--date'</code> - set a date for all tracks.</li>
  </ul>
</details>

<h3>Logging and manual mode</h3>

If you want you can get a json log with the metadata of the edited files. To do this, run the program with the `-l` or `--log` flag. By the path that is stored in the
`LOG_PATH` variable in the file `config.py`, a file of the following format will be created:
```json
{
  "file-name.mp3": {
    "data": ["value"]
  }
}
 ```
You can restore metadata based on information from any log file. For example, this may be useful if you have the same files in different directories and you need to edit 
them all. Run the program with the `-p` or `--parse` flag, set the log file and enter the path to the required directory. Any others flags except `-r` or `--rename` will be ignored.  
  
Also you can write the current unchanged metadata to a json file. To do this, run the program with the `-s` or `--scan` flag. I call this **manual mode** - at first you
create a json file with the unchanged metadata, then you edit them and apply it by running the program with the `-p` or `--parse` flag.

<h3>More Features</h3>

- If the file contains information about the copyright holder and you want to leave it, use the `-c` or `--copyright` flag.
- You can run the program in minimal mode with `-m` or `--minimal` flag. It will only ask for title, artist, album and genre. Other data will be cleared.
- Files could be renamed in the form of `artist_track-title.mp3`. Use the `-r` or `--rename` flag. Please note that the information in the logs will be associated with the new name.
- To remove all data from the tracks, run the program with the `-d` or `--delete` flag. Any other flags will be ignored.
- If you need to go back to editing the previous track in the interactive mode, enter the `^` character in any field.
- In interactive mode, two colons after the letters _a_, _o_ or _u_ will be replaced with this letter with an umlaut. For example, `Mo::tley Cru::e` will be replaced by `Mötley Crüe`.
- To avoid bugs, the data entered by the user will be validated. To disable it, set the `SKIP_VALIDATION` variable in `config.py` to `True`. Be careful using it!
- By default, the track number and the release year will be deleted in the minimal mode. To leave them, set the `LEAVE_SOME_DATA` variable in `config.py` to `True`.
- To view the quick help, run the program with the `-h` or `--help` flag.

## 🤝 Contributing
If you have any ideas or found any bugs here, plz open the [issue](https://github.com/dan-sazonov/id3-editor/issues)
 or make a fork and offer a [pull request](https://github.com/dan-sazonov/id3-editor/pulls). And it will be
 great if you tell me about these ideas, maybe I'm already working on them.
 
## 👨‍💻 Author
The author of this repository and code - [@dan-sazonov](https://github.com/dan-sazonov). <br>
**Reach me:**<br>
[✈️ Telegram](https://t.me/dan_sazonov) <br>
[📧 Email](mailto:p-294803@yandex.com) <br>

