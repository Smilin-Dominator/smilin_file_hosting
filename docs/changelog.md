# Changelog

## v1.0
This is the Base Version. It contains a fully functional Server (written in Python's FastAPI) and a GUI Client (written in Python's TKinter).
I also included documentation written in Material-MkDocs.
### Features
- New GUI Client
- New API Server
- Documentation Written In Material-MkDocs
### Fixes
- None


## v1.1
This is the first major update. I changed the Username based authentication to a UUID based authentication system. Unlike
the first version, where anybody could connect using a username, without registering and the table would be created for them.
This time, I created a new table that stores the UUIDs of all the users. If somebody tries to connect without being
registered, the server returns false, unlike earlier, where the server would create a table. To register, you have
to send a POST request to "/register" and it'll add the UUID to the Users Table, create a Table for the UUID and return
the UUID to the client (so you can connect). If you lose the UUID, you won't be able to access your files.
### Features
- UUID Based Authentication
- Switched Database to MariaDB
### Fixes
- \#1 -> Folder Name and Database Name could Differ


## v1.2
This is the second major update; I switched the GUI Framework from Python's TKinter to a much more powerful
PyQt Library, and took the time to design the UIs in Qt Studio and import them at runtime, which makes it easier
to program and improves the result. 
Instead of tucking the credentials section to the right of the main UI, I made a separate window for it, and added a 
few more choices! 
I moved from using a frame for the files to using a TreeWidget, which has Checkboxes and as a result, added new methods
to download and delete the selected files. I also improved the Concurrency features in this release; Using methods like
ThreadPoolExecutors and Locks.

### Features
- New Redesigned User Interface written using the PyQt Library
- Files are now selectable (making Bulk Downloads and Deletes Possible)
- Credentials and the Main UI are in separate windows
- Added an option to specify the maximum amount of concurrent downloads and uploads.
### Fixes
- \#2 -> Error When Decrypting


## v1.3
This is the third major update. I switched the encryption method from GPG to AES-256 CFB. The main reason for this was
GPG being way too slow to decrypt filenames and even files (one would load after each other with a literal second
delay when refreshing); But with AES, all file elements load near instantly.

### Features
- AES 256-Bit Encryption with the CFB Cipher instead of GnuPG
- Wayyy Faster Encryption and Decryption 
- The database has an additional column for the Initialization Vector used to Encrypt the File and Filename
### Fixes
- None


## v1.3.1
I improved the credentials window by adding tabs. There's three so far;
- Credentials
- Directories
- Advanced

I also added support for choosing a Temporary Directory and a Files Directory; Which can be set in the credentials window, but the configuration file stays in the same location!

### Features
- Customizable Temp and Files Directories

### Fixes
- Changed the package 'cryptography' to 'pycryptodome' (Major Issue)
- Displayed a String instead of Bytes in the Key Entry field (Major Issue)
- Changed writing the key in the format "b'xxx'" to "xxx" (Major Issue)


## v1.3.2
I added import and export functions to the program. There are two new QPushButtons in the Credentials UI.

### Features
- Import and Export Functions

### Fixes
- None


## v1.3.3
I handled all the known exceptions that make the program crash, and described why they occur. I also added
two new exception types

### Features
- New Exceptions
- Credentials' Status is more Descriptive
- If the amount of files received from the request is not equal to the amount of TreeItems after decrypting, an error is raised

### Fixes
- Handled Errors, The Program Doesn't Crash Often
