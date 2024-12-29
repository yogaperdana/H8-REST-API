# Learning REST API with Python

This repository is used for my learning based on course _[Membuat Rest API dengan Python](https://udemy.com/course/membuat-rest-api-dengan-python)_ by [Hacktiv8](https://hacktiv8.com/).

The source code is mostly modified, adding various updated methods, so it doesn't become too similar anymore compared to what has been taught in the course.

> [!IMPORTANT]
> 
> **Package Adjustment**
> 
> The course uses the [Flask RestPlus](https://github.com/noirbizarre/flask-restplus) package, but now it has been forked by the community into [Flask RESTX](https://github.com/python-restx/flask-restx) package, making it more up to date with newer versions of Python and of course Flask itself.
> 
> In summary, this project uses **`flask_restx`** package, instead of `flask_restplus`.

## Environment Setup

This project uses **Python v3.12.8**.

Execute the command line by line on the terminal according to one of the following methods:

1.  Using `venv`:

    <details><summary><small><strong>Windows</strong> (Command Prompt)</small></summary>

    ```
    python -m venv .venv
    .venv\Scripts\activate.bat
    pip install -r requirements.txt
    ```

    </details>
    <details><summary><small><strong>Windows</strong> (PowerShell)</small></summary>

    ```
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    </details>
    <details><summary><small><strong>UNIX/macOS</strong> (bash/zsh)</small></summary>

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    ```

    </details>

2.  Using `conda`:

    ```
    conda create --name restapi --file requirements.txt
    conda activate restapi
    ```

## Run Application

Run the app by executing this command on the terminal:
```sh
flask run
```
or add `--debug` parameter to run with debug mode.

Access the API documentation through a web browser with URL displayed on the terminal screen and point to directory `docs` (e.g. http://127.0.0.1:5000/docs/)
