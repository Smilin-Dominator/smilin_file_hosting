# Usage
This section describes how to use the program.

## Server
After issuing the `docker-compose up -d` command, the MySQL Database should start in about 30 Seconds, but the
API might take about a minute or two, depending on your;

* Network Speed (as it needs to install the requirements) 
* Clock Speed (to start the API inside a Container).

Afterwards, you can test the API by issuing the command `curl -X GET http://(server):2356/(token)/`, replacing
`server` with the server's domain/ip and `token` with a random string. It should return `false`, as there's no
UUID registered (but if you used a registered token, it'll return True)

All the Server Interaction is done through the client, so there's no need to use `curl` or `wget` to
send requests to the server again.


## Client
This guide assumes that you've performed all the actions mentioned in the installation page.

### First Time Setup
As soon as you run the client for the first time, you should see a screen with a section on the left, and the rest of the
area blank. (See [Credentials](#credentials))

First, enter data into the `link` and `email` fields respectively. Afterwards, hit 'register'. If the URL was valid,
it'll override the username field with your Token (Write this down or save it somewhere, as this is the only way
to access your data), but if the URL wasn't valid, there'll be no change.

Afterwards, press connect. If the connection succeeds, you'll see the rest of the elements of the program appear, if not,
check if the link and username are correct.

Note that your credentials are saved in a file called `config.json` in the credentials directory of client. Each time you
open the program after the first time, your credentials will autoload for you. If you put different credentials and
press 'connect', it'll override the previous credentials and autoload those next time.

    
### The Main Program

#### Credentials

This section displays 3 Entry Fields and One Button;

* `Name (Entry)`  **->** Username that you use to connect to the server.
* `Link (Entry)`  **->** URL to the server hosting the service, with the Port (:2356) at the End.
* `Email (Entry)` **->** The email that's attached to your GPG Key (The one you set in the installation page)
* `Connect (Button)` **->** This will save the credentials to the configuration file and connect to the server.
* `Register (Button)` **->** If you've entered a link, this will connect to the link and generate+register a Token/Username for you.

???+ "The Importance Of Tokens"
    Remember! If you lose your token, you lose your files.


#### Files

This section displays a list of decrypted filenames along with buttons to download and delete them.

* If you press download, it downloads and decrypts the file into a folder in the client directory called 'files'
* If you press delete, it deletes the file from the database and from the server's folder

#### Status

* Upload (Button)

    > This will open a file(s) selection dialog. Select as many files as you like and then submit. After you do,
    > it'll encrypt the files and their filenames and upload them. 

* Uploading (Frame)

    > This displays the files that are currently being uploaded

* Downloading (Frame)

    > This displays the files that are currently being downloaded

