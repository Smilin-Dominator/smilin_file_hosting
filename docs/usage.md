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
Upon first launch, you'll see a window called [credentials](#credentials-window).

If it's your absolute first time setting up the client; Enter the `link` into the link field and hit
register. If the link is valid, the `token` field should be filled with a random token. and a Key will be generated for you<br>
Otherwise, just enter the link into the `link` field and your token into the `token` field, without hitting register.

In the advanced features section, input the maximum number of concurrent uploads and downloads that
can take place parallely. I've found that 4 is the perfect balance for me, but you can change it. I've limited the
numbers to 10, for obvious reasons, but you can always override it by editing the JSON file manually.

Finally, click 'Save and Connect'. If the connection succeeds, you will be transferred to the Main UI. Then,
you can refer to the following section.
    
### The Main Program

#### Credentials Window
You will get this screen if;

* It's the first time launching the program.
* The connection to the server failed.
* The token is invalid.
* You pressed 'credentials'

In the first container (labeled "Credentials"), you'll see 3 Input fields;

| Element | Type  |                                              Function                                               |
|:-------:|:-----:|:---------------------------------------------------------------------------------------------------:|
|  Token  | Entry |                    This is the unique username you use to connect to the server                     |
|  Link   | Entry |                                   This is the link to the server                                    |
|   Key   | Entry | This is your AES key, You can either generate it by hitting 'Register' or entering a 256 Bit String |

In the second container (labeled "Advanced Features"), you'll see 2 Number Input Boxes (SpinBoxes);

|       Element        |  Type   |                         Function                          |
|:--------------------:|:-------:|:---------------------------------------------------------:|
| Concurrent Downloads | SpinBox | The maximum amount of download threads to run in parallel |
|  Concurrent Uploads  | SpinBox |  The maximum amount of upload threads to run in parallel  |


In the third container (labeled "Operations"), you'll see 2 Buttons and 1 Label;

|     Element      |  Type  |                                                          Function                                                           |
|:----------------:|:------:|:---------------------------------------------------------------------------------------------------------------------------:|
|     Register     | Button |                      If the link isn't empty, this will try and connect to the server and register you                      |
|      Status      | Label  |                       This invisible label will display the status; Such as connection errors and all                       |
| Save and Connect | Button | This will overwrite the options in 'credentials/config.json' with the new credentials you entered and connect to the server |


#### Main Window
In the left-most container (labeled "Status"), there are 2 more containers and 1 label:

|      Element      |    Type    |                                          Function                                          |
|:-----------------:|:----------:|:------------------------------------------------------------------------------------------:|
|  Uploading Files  | ListWidget |                  This will display the files that are currently uploading                  |
|      Status       |   Label    | This invisible status will make itself visible and show statuses such as connection errors |
| Downloading Files | ListWidget |                 This will display the files that are currently downloading                 |

In the top-right container (labeled "Files"), there's a TreeWidget:

| Element |    Type     |                              Function                              |
|:-------:|:-----------:|:------------------------------------------------------------------:|
|  Files  | Tree Widget | Displays the files with a checkbox to the left of them (see below) |


In the bottom container (labeled "Operations"), there are 5 Buttons:

|      Element      | Type   |                                Function                                |
|:-----------------:|--------|:----------------------------------------------------------------------:|
| Download Selected | Button |                    Downloads the files you selected                    |
|  Delete Selected  | Button |                     Deletes the files you selected                     |
|      Refresh      | Button |                         Refreshes the file list                        |
|    Upload File    | Button | This opens a file dialog for you to select as many files as you'd like |
|    Credentials    | Button |                    This opens the credentials window                   |
