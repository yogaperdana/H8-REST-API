# Learning REST API with Go

> This repository is used for my learning based on course _[Rest API dengan Golang](https://www.udemy.com/course/rest-api-dengan-golang)_ by [Hacktiv8](https://hacktiv8.com/).

Just a simple REST API application to read, create, update and delete item from static data (which means restarting it also will reset the stored data).

The source code is mostly modified, adding various updated methods, so it doesn't become too similar anymore compared to what has been taught in the course.

This project uses **GO v1.23.4**. please install Golang first to build this source.

## Run Application

Run the app by executing this command on the terminal:

```sh
go build -o api && ./api
```

For Windows OS, add an executable extension after the filename, for example: `go build -o api.exe`

To quit, simply press <kbd>Ctrl+C</kbd> or another keyboard interrupt shortcut depends on your terminal.

## Test Application

I've included a [Postman](https://postman.com)'s collection JSON file on this repository that you can import it to your Postman and run the test case.
