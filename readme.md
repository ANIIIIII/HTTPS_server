# HTTPS_server

## Environment

Ubuntu 20.04 (LTS) x64

HTTP/1.1

## Getting started

0. Before running the server the folders and files should be like:

   ```
   .
   ├── index.html
   ├── login.html
   ├── accounts.txt
   ├── comments.txt
   ├── signinfailed.html
   ├── signupfailed.html
   ├── signupsuccess.html
   ├── error.html
   ├── server.pem
   └── server.py
   ``` 

1. Run `server` with specified port number.

   ```
   python3 server.py
   ```

   > This runs the server on port 8080.
   
   > My linux machine run the server with `screen` command.

2. Now you can test it with `curl`.

   ```
   curl -v -k https://[IP]:8080/
   ```

   or visit directly with browser.

   ```
   https://[IP]:8080/
   ```

   > These send http request to the server with IP [IP] on the port 8080.

## Example

I rent an Ubuntu 20.04 (LTS) x64 machine on DigitalOcean with floating IP `138.197.226.51` and run the server on port `8080`.

One can visit it with `curl`.

   ```
   curl -v -k https://138.197.226.51:8080/
   ```

or visit directly with browser.

   ```
   https://138.197.226.51:8080/
   ```

>These send http request to the server with IP `138.197.226.51` on the port `8080`

## Demo

https://drive.google.com/file/d/1B7QJY-YxNEeb5Zpja2fzXY1rzACZhgwp/view?usp=sharing

>This video demos the `Getting started` part and the useage of my website

## Files and Implementation

The server `server.py` is implemeted with multithread and python3 http.server.

In `server.py` :

`main` set the `account.txt` and `comments` empty, use `ThreadedHTTPServer` and `ssl.wrap_socket` to set HTTPS server and run it.

> The change of port number is allowed and you should change all the port number 8080 in all file with the replaced port number.

`Handler` class serves with several types of services and prints the serving thread and request information in localhost whenever a GET request or POST request is comming.

`login.html` is the interface with sign up and sign in function.

`index.html` is the interface presenting comments with comment function after sign in.

`accounts.txt` stores the registrated accounts information.

`comments.txt` stores the comments information.

`server.pem` is the self-certification derived from `openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes` to implement HTTPS server.

others are simple interfaces of successed, failed or error message.

## Service

`Sign up` : One can registrate its own accounts.

`Sign in` : One can login with its own accounts.

`Logout` : One can logout after login with its own accounts.

`Comment` : After login, one can browse others' comments or comment anything on the comment board.
