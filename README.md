

## Getting started 

To set up the Python environment and run the project, issue the following commands in the terminal from the `cfc/` directory. 

1. Activate the virtual environment:
    ```
    source cfc_project/bin/activate (for bash/zsh, or:)
    C:\> cfc_project\Scripts\activate.bat (for cmd.exe)
    ``` 
see [python3 official venv](https://docs.python.org/3/library/venv.html) for commands for other shells.


2. Install the Python dependencies from `requirements.txt`:
    ```
    (cfc_project) $ pip install -r requirements.txt
    ```

3. (Optionally) run the tests in the project base directory to ensure everything is working:
    ```
    python -m unittest tests/test_main.py
    ```

## Remarks 

Given more time, I would further improve the following points:
- Higher test coverage 
- Task 2 sometimes returns segmentation fault on local machine. To debug the problem with gdb. Seg fault possibly related to the point below - 
- Use a Session object to wrap the tests using requests (cf. https://stackoverflow.com/questions/48160728/resourcewarning-unclosed-socket-in-python-3-unit-test)
