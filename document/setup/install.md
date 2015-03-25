Installation instructions for SDMdata
===
Author: Xiaoquan Kong

Email: u1mail2me@gmail.com

Date: 2015-1-25

## Source code
User can download the source code from <https://github.com/howl-anderson/SDMdata>.
## System require
### Linux
SDMdata is developed under Linux operation system (for more specific "ubuntu"). This instruction mainly guide user how  to intall SDMdata into ubuntu. For other system user, see following section.
### UNIX
Simliar with Linux, see Linux install progress for review.
### Mac OS X
Because we do not have any Mac OS X device, we can not test SDMdata on this system. But Mac OS X was quite like UNIX and Linux system. They have shared a lot of common library. SDMdata can be installed on Mac OS X just like ubuntu, but it may be have some different operation.
### Windows
For those user who use Windows system, we feel sorry that SDMdata currently do not support Windows yet for some technical reason. If user still want to use SDMdata on Windows, we think it may be a good choice to use virtual machine. We have made an independent document on how to install SDMdata through virtual machine step by step. Please see []   (/document/install/windows/install.pdf)
## Software require
SDMdata is written in python language, and SDMdata with several library by default may not be installed in operating system. For technical and convenient reason, we do not recommend user to check depend relationship by yourself. We have provide a script to check depend relationship. If something is missing, the script will do that for you. Currently we add a script to help user install software in Ubuntu system. Helper script for other linux distribution, Mac OS X or UNIX operating system currently is lacked. In the `install` directory of SDMdata, there is a file named `ubuntu.sh` and run a terminal and type command:

    ./install/ubuntu.sh
    
This command will install system-wide package that SDMdata needed.

If you have not yet installed MySQL database, we will provide a script to help install it. In the same directory, there is a file named `install_database.sh`, which will install MySQL for you. Notice that during the install process, you need set database administrator account and password.
   
User should notice that you may need to have the correct permissions to do this job. For example, using a root user account. If not, you may use `sudo` command before previous command, if you don’t know how to do this or what is this, ask someone who familiar with this operating system. 

## Database require
SDMdata require a SQL database as store container. We recommend some big SQL database such as MySQL and PostgreSQL. Although we want to use SQLite as database, but maybe because SQLite is not parallel written so well, in our big example test, SQLite sometimes do not work so well, so you’d better not to use the SQLite as database. If you don't know how to install MySQL or PostgreSQL on ubuntu, here we wrote a tiny tourial on that <document/install/ubuntu/MySQL.md>

###Configure SDMdata
The only thing need to be configured is the database, you will be require to tell SDMdata which database to be use and give username and password (if any). In the `/sdmdata/configure` directory, you can find a file named “configure.yaml”, open it with text editor, you will can see a line as this:

`DATABASE_HOST_URI: mysql://root:123456@localhost:3306`

The part of `'mysql://root:123456@localhost:3306'` will indicate the database information. This string actually is a database URI, for details you can see <http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html>, here we gave an example for MySQL and PostgreSQL:

* Database user name: USER
* Database user password: PASSWORD
* Database host name or IP: HOST
* Database port: PORT

So you can use:

* For MySQL database: `mysql://USER:PASSWORD@HOST:PORT`
* For PostgreSQL database: `postgresql://USER:PASSWORD@HOST:PORT`

For user do not know a lot about database, we have created a helper script named `create_database.py` in user's SDMdata top directory. Run this script, it will create a database named "sdmdata" for you.


##Create admin account
The next thing before using the SDMdata is to create admin account. In the top directory, there is a file named `create_admin.py`, execute it in the terminal. It will create the admin account. If everything is ok, it will print “Admin account is created! Password: admin”, if the admin account has already existed, it will not work and print “admin already exists! Nothing change!”, if it print something not like that, it may be the database connection issue, check your database configure and make sure that the database is running. 
Notice: default administrator account is “admin” and the password for admin is “admin”, you can change the password when you login as admin. For security reason, you should change your admin password when you  login at first time.

##Control and configure SDMdata web server
In the root directory of SDMdata, there is a file named `server.py`, in the terminal, you run the command that will allow  you to control the SDMdata server. You can run the server with `./server.py start`, and stop the server with `./server.py stop`. 

Maybe you want to configure the server IP and the port. In this case, you open the “server.sh” with text editor, you will find a line like:

    server_host = ”0.0.0.0”
    
This is which host you serve to, default is “0.0.0.0” which means everyone who can access this host will be allowed to access the SDMdata server. If you want to access localhost only, you can change the host to “127.0.0.1” or “localhost”.

If you want to configure the port of server, you can find a line like:

    server_port = "8000"
    
Change the `8000` to any port you want. Here is a tips you’d better not change the port to “80”, this port was reserved to other HTTP server. In generally, you should not use the port below 1024, to be more safety you’d better use the port above 5000. If you know what you are doing, please ignore this tips.

## More support
If you have any question or suggestion, please send E-mail to us.
