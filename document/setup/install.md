Installation instructions for SDMdata
===

Email: u1mail2me@gmail.com

Date: 2014-10-15

## Source code
You can download the source code from <https://github.com/howl-anderson/SDMdata>.
## System require
SDMdata require UNIX, Mac OS X or Linux operating system. For those user who use Windows system, we feel sorry that SDMdata currently not support Windows yet for some technical reason. If user still want use SDMdata on Windows, we think use a virtual machine is a good choice (we recommend VirtualBox <http://www.virtualbox.org>), setup a virtual machine and install a Linux distribution (for example Ubuntu), so system require will be satisfied.

## Software require
SDMdata was written in python language and use several library that default may not be installed in operating system. For technical and convenient reason, we do not recommend user check depend relationship by yourself. We have provide a script to check depend relationship. If something is missing, the script will do that for you. Currently we add a script to help user install software in Ubuntu system. Helper script for other linux distribution, Mac OS X or UNIX operating system currently is lacked. In the `install` directory of SDMdata, there is a file named `ubuntu.sh` and run a terminal and type command:

    ./install/ubuntu.sh
    
This command will install system-wide package that SDMdata needed.

If you have not yet installed MySQL database, we will provide a script to help install it. In the same directory, there is a file named `install_database.sh`, which will install MySql for you. Notice that during the install process, you need set database administrator account and password.
   
User should notice that you may need to have the correct permissions to do this job. For example, using a root user account. If not, you may use `sudo` command before previous command, if you don’t know how to do this or what is this, ask someone who familiar with this operating system. 

## Database require
SDMdata require a SQL database as store container. We recommend some big SQL database such as MySQL and PostgreSQL. Current version of SDMdata do not support SQLite quite well, especially when the data become bigger (we may fix this issue, or find the reason in the feature), so you’d better not use the SQLite as database.

###Configure SDMdata

The only thing need to be configured is the database, you will be require to tell SDMdata which database to be use and give username and password (if any). In the `/sdmdata/sdmdata` directory, you can find a file named “db_config.py”, open it with text editor, you will can see a line as this:

`DATABASE_URI = 'mysql://root:123456@localhost:3306/sdmdata?charset=utf8'`

The part of `'mysql://root:123456@localhost:3306/sdmdata?charset=utf8'` will indicate the database information. This string actually is a database URI, for details you can see <http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html>, here we give an example for MySQL and PostgreSQL:

* Database user name: USER
* Database user password: PASSWORD
* Database host name or IP: HOST
* Database port: PORT
* Database name: DATABASE_NAME

So you can use:

* For MySQL database: `mysql://USER:PASSWORD@HOST:PORT/DATABASE_NAME`
* For PostgreSQL database: `postgresql:// USER:PASSWORD@ HOST:PORT/DATABASE_NAME`

For user do not know a lot about database, we have create a helper script named `create_database.py` in user's SDMdata top directory. Run this script, it will create a database named "sdmdata" for you.


##Create admin account
The next thing before use the SDMdata is create admin account. In the top directory, there is a file named `create_admin.py`, execute it in the terminal. It will create the admin account. If everything is ok, it will print “Admin account is created! Password: admin”, if the admin account already exists, it will not work and print “admin already exists! Nothing change!”, if it print some not like that, it may be the database connection issue, check you database configure and make sure the database is running. 
Notice: default administrator account is “admin” and the password for admin is “admin”, you can change the password when you login as admin. For security reason, you should change your admin password when you first time login.

##Control and configure SDMdata web server
In the root directory of SDMdata, there have a file named `server.py`, in the terminal, you run the command that will allowed you to control the SDMdata server. You run the server with `./server.py start`, stop the server with `./server.py stop`. 

Maybe you want configure the server IP and the port. In this case, you open the “server.sh” with text editor, you will find a line like:

    server_host = ”0.0.0.0”
    
This is which host you server to, default is “0.0.0.0” this means everyone who can access this host will be allowed to access the SDMdata server. If you want to access localhost only, you can change the host to “127.0.0.1” or “localhost”.

If you want to configure the port of server, you can find a line like:

    server_port = "8000"
    
Change the `8000` to any port you want. Here is a tips you’d better not change the port to “80”, this port was reserved to other HTTP server. In generally, you should not use the port below 1024, to be more safety you’d better use the port above 5000. If you know what you are doing, please ignore this tips.

## More support
If you have any question or suggestion, please send E-mail to us.