# KaraokeMusicVideoManager
A software that scans folders after music videos, brings them together in a list and starts them. After this there will also come a website where people can say/post which song they want to do next.

## What is the KaraokeMusicVideoManager about?

It's a program to manage your Karaoke evening/event :sing:.

You can import all your karaoke music video files via selecting the folder they are within and then see every music video with the following format in a searchable and sortable table:

|     Artist     | " - " |             Title             | `.avi`/`.mp4`/`.mkv`/`.wmv`/`.mov`/`.mpg` |
| :------------: | :---: | :---------------------------: | :--------------------------------------: |
| Example Artist |   -   | Title that also can contain - |                   .mp4                   |

If one of your file isn't in this format you can just go into the tab **Source folders** and open with the button **Wrong formatted files ** to find them and rename them within the program.

If you click one entry in the file the music video file get's instantly opened by your native system video player.

You can do even more if you press the right mouse button in the music video list table tab. You can ignore a file completely, rename it, show it in the file explorer or even add them to a playlist.

*But there is even more:*

You can also setup a server (with for example a Raspberry Pi 3 and Apache) and every guest in the same network as the server and your computer where you run the program can add themselves music video files to the playlist and even vote which they want to sing or watch after a quick setup on your computer.

## Setup the program

"Normal" setup:

1. Download either the portable or the Windows installer version from **[GitHub Releases](https://github.com/AnonymerNiklasistanonym/KaraokeMusicVideoManager/releases)**.
2. Run the portable or version or install it on Windows with the Windows installer version and run it there like a normal program.
3. Choose the folders with your music videos by clicking for every folder the button **Add Source Folder** and choose the folder via your native file explorer.
4. Now select the tab **Music video list** to search the list and run each music video on right click.

Server setup:

1. Click in the upper right the button **Network** to open a new login window.
2. Now enter all the information needed to login to the server and add files to the root directory of the there installed webserver (that also supports PHP). Therefore enter:
   - The IP address of the server/Raspberry Pi 3
   - The root directory of the web server (where the `index.html` file is within [`/var/www/html/`])
   - The username of your account
   - The password to your account
3. Now click login to get automatically logged in with your provided information.
4. Then click in the menu bar the entry **Network**, then **Server setup** and then choose what service you want to provide:
   - Static list (only a list of all files)
   - Static searchable list (the same but with a interactive search)
   - Party list (contains a list, a playlist, and a form where everybody can add an entry to the playlist)
5. Click the service you want to have and automatically every time you refresh the playlist table tab (Right mouse button, click **Refresh**) it fetches all the information from the server and sorts it after votes and then time.
6. Have fun!

## Documentation

Links to the big parts of this project:

### :arrow_forward: [How to open/edit/export the main Java project?](Documentation/HOW_TO_JAVA.md)

### :arrow_forward: [How to open/edit the web interfaces?](Documentation/HOW_TO_WEB.md)

### :arrow_forward: [How to open/edit the logo/any images?](Documentation/HOW_TO_IMAGES.md)

### :arrow_forward: [How to open/edit/compile the Windows installer?](Documentation/HOW_TO_NSIS.md)

### :arrow_forward: [How to update/create/compile everything at once?](Documentation/HOW_TO_MAGIC.md)

### :arrow_forward: [How to setup a server for the 'party-mode' (Raspberry Pi 3)](Documentation/HOW_TO_SERVER.md)

### :arrow_forward: [Frequently asked questions](Documentation/FAQ.md)

## Advanced instructions: How can I download/install/run the program?

### General

The program runs on every computer that has Java (a Java Runtime from the last one/two years) installed:

:arrow_right_hook: You can download the portable runnable `.jar` file from [GitHub Releases](https://github.com/AnonymerNiklasistanonym/KaraokeMusicVideoManager/releases) (the latest release).

Just double click the file and the program should be running.

### Windows Instructions

If you have Java not installed or an old version install the newest and securest version form the official website: https://www.java.com/en/download/

* Find the `.jar` file in the Windows Explorer and double click it to start the program.
* For the Windows Operating System we even built an installer for the program:
  * You can download the executable Windows installer `.exe` file from [GitHub Releases](https://github.com/AnonymerNiklasistanonym/KaraokeMusicVideoManager/releases).
  * Double click it after you found it in the Windows Explorer and follow the instructions
  * After the installation is finished you will find three new entries in a folder in your start menu:
    * one will bring you right here to this website
    * one will launch the program
    * one will uninstall the program

### Linux

If you have Java not installed or an old version install the newest and securest version form the official repository:

```
# Ubuntu
sudo apt-get install oracle-java8-jdk
# Manjaro
sudo pacman -S jdk8-openjdk
```

Because this program uses a Java Library named JavaFx you additional need to install this too:

```sh
# Ubuntu
sudo apt-get install openjfx
# Manjaro
sudo pacman -S java8-openjfx
```

Now you can run the program with the following command through the command line:

```
java -jar path/to/downloaded/file.jar
```

## Frequently asked questions

[Click this text to get to the frequently asked questions (FAQ's).](Documentation/FAQ.md)

## Still have a Question/Problem/Idea?

If you still have any kind of questions, problems or great ideas open an issue or open a pull-request.

Have fun using this program!

:smiley:
