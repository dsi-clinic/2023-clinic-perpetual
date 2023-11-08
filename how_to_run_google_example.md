How to run this vrp example in VSCode inside a Docker container:
https://developers.google.com/optimization/routing/vrp#complete_programs

## setup
- Make sure Docker is running
- Stop all running containers and images in Docker, and then delete them so you have a clean Docker dashboard
- Add “ortools~=9.7” at the end of the requirement.txt

## going the "reopen in container" route 
After "reopen in container", check two things in VSCode to make sure that you are in the container
- On the left corner there is: 
```Dev Container: 2023-autumn-perpetual-devcontainer```
- inside the VSCode terminal, the prompt should say something like: 
```(base)jovyan@...:/project$ ```
### run the example with .py
1. Create run_google_example.py
    - Go to File -> New Text File, click on “Select a language” -> choose Python
    - Save the file at /project/run_google_example.py
    - Copy paste the example code into the file and save the file
    - Go to VS Code terminal to check that your script is there by running:
    
    ```cat /project/run_google_example.py```

    - the terminal should print out the code you just copy pasted
    
2. run run_google_example.py
    - in VSCode terminal run:

    ```python /project/run_google_example.py```

    - the script should run successfully and you will see the result in terminal

### run the example with .ipynb
1. create run_google_example.ipynb
    - Go to File -> New File, select jupyter notebook
    - Save the file at /project/run_google_example.ipynb
    - Copy paste the example code into a code cell and save the file

2. start jupyter notebook server
    - in VSCode terminal run:

    ```jupyter notebook```

    - among the bunch of things that the terminal gives back, locate somthing like this:
    ``` 
    To access the server, open this file in a browser:
            file:///home/jovyan/.local/share/jupyter/runtime/jpserver-19820-open.html
        Or copy and paste one of these URLs:
            http://698ac9489e81:8888/tree?token=2fe16b45b1c9a022079b951ce33af8d8103d46e8b44d2369
            http://127.0.0.1:8888/tree?token=2fe16b45b1c9a022079b951ce33af8d8103d46e8b44d2369
    ```
    - copy the last URL, we are going to use it later
    ```
    http://127.0.0.1:8888/tree?token=2fe16b45b1c9a022079b951ce33af8d8103d46e8b44d2369
    ```
    - you have two options now - run the notebook in a web browser or run the notebook inside the VSCode, either way you are going to use the URL

#### run notebook in a web browser
- paste the URL in a web browser, you should see a familiar jupyter notebook interface
- click into run_google_example.ipynb, run the example code, the code should run successfully and the result should show below the code cell
- notice that on the upper right side where it shows kernel info, it should say "Python3(ipykernel)". To confirm that you are in the container, run "pwd" in the code cell, you should get "/project"
#### run notebook inside VSCode
- open run_example_google.ipynb inside VSCode
- on the upper right side of the notebook, there should be "Select Kernel" (or some python version), clicke it -> then on the top "Select another kernel..." -> select "Existing Jupyter Server..." -> select "Enter the URL of the running Jupyter Server..." -> paste the URL -> hit enter -> the URL will change to 127.0.0.1 -> hit enter again to comfirm -> then select the option called "Python 3(ipykernel) /opt/conda/bin/python"
- now the kernel selected should be Python3(ipykernel)
- to confirm that you are in the container, run "pwd" in the code cell, you should get "/project"
- run the example code, the code should run successfully and the result should show below the code cell

3. exit jupyter notebook server
- it's good to exit jupyter server when you're done
- inside VSCode terminal, Ctrl + C


## not going the "reopen in container" route 
If for some reason, VSCode cannot "reopen in container", we can still run things in the container by interacting with it in terminal. I personally think it is good to learn to do it this way since it relies less on VSCode being a good intermediate. 

To do it this way, make sure you are opening the repo locally in VSCode:
- On the left corner there SHOULD NOT be: 
```Dev Container: 2023-autumn-perpetual-devcontainer```
- inside the VSCode terminal, the prompt SHOULD NOT be: 
```(base)jovyan@...:/project$ ```

### run the example with .py
1. Create run_google_example.py
    - Go to File -> New Text File, click on “Select a language” -> choose Python
    - Save the file at /project/run_google_example.py
    - Copy paste the example code into the file and save the file
    - Go to VS Code terminal to check that your script is there by running:
    
    ```cat /project/run_google_example.py```

    - the terminal should print out the code you just copy pasted
    
2. build image and start a docker container with an interactive session
    - in VSCode terminal run:

    ```make run-interactive```

    - after it's done, the prompt in the terminal should change to something like:

    ```(base) jovyan@b3fb54b029b3:/project$```

     - now you are in the container

3. run run_google_example.py
    - in VSCode terminal run:

    ```python /project/run_google_example.py```

    - the script should run successfully and you will see the result in terminal

4. exit the container
    - in VSCode terminal hit Ctrl D. You will exit the container

### run the example with .ipynb
1. create run_google_example.ipynb
    - Go to File -> New File, select jupyter notebook
    - Save the file at /project/run_google_example.ipynb
    - Copy paste the example code into a code cell and save the file

2. build image and start a container and start a jupyter lab inside the container
    - in VSCode terminal run:

    ```run-notebooks```
    
    - among the bunch of things that the terminal gives back, locate somthing like this:

    ``` 
    [I 2023-10-10 20:13:24.116 ServerApp] Jupyter Server 2.7.3 is running at:
    [I 2023-10-10 20:13:24.116 ServerApp] http://localhost:8888/lab
    [I 2023-10-10 20:13:24.116 ServerApp]     http://127.0.0.1:8888/lab
    [I 2023-10-10 20:13:24.116 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    ```

    - copy the URL, we are going to use it later

    ```
    http://127.0.0.1:8888/lab
    ```

#### run notebook in a web browser
- paste the URL in a web browser, you should see a familiar jupyter lab interface
- click into run_google_example.ipynb, run the example code, the code should run successfully and the result should show below the code cell
- notice that on the upper right side where it shows kernel info, it should say "Python3(ipykernel)". To confirm that you are in the container, run "pwd" in the code cell, you should get "/project"
#### run notebook inside VSCode
- I cannot get it to work right now, but i think the above have provided several good options. 

3. exit jupyter notebook server
- it's good to exit jupyter server when you're done
- inside VSCode terminal, Ctrl + C









