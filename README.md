# 2023-clinic-perpetual

## Project Background

Perpetual's goal as a nonprofit is to promote sustainability in large cities by reducing single-use disposable waste.  Currently, individual restaurants may be reluctant to change from disposables to reusables due to higher costs of purchasing the foodware and maintaining in-house washing facilities. This project aims to help perpetual lower the cost of establishing a system for washing and redistributing reusable foodware to participating food and drink establishments (FUEs) throughout a given city.

Perpetual has partnered with Galveston, TX, for its first launch for this system. This quarter's team was responsible for creating the first working model for the collection and distribution process in Galveston and generalizing this city’s model into a pipeline for building models in future participating cities.

## Project Goals

[ to be filled ]

## Usage

### Instructions on using Mapbox API
* Go to https://www.mapbox.com and register for a free Mapbox API.
* Add a `config_mapbox.ini` file at /utils/config_mapbox.ini, with the following content.
```
[mapbox]
token = your_mapbox_token_here
```

### Docker

### Docker & Make

We use `docker` and `make` to run our code. There are three built-in `make` commands:

* `make build-only`: This will build the image only. It is useful for testing and making changes to the Dockerfile.
* `make run-notebooks`: This will run a jupyter server which also mounts the current directory into `\program`.
* `make run-interactive`: This will create a container (with the current directory mounted as `\program`) and loads an interactive session. 

The file `Makefile` contains information about about the specific commands that are run using when calling each `make` statement.

### Developing inside a container with VS Code

If you prefer to develop inside a container with VS Code then do the following steps. Note that this works with both regular scripts as well as jupyter notebooks.

1. Open the repository in VS Code
2. At the bottom right a window may appear that says `Folder contains a Dev Container configuration file...`. If it does, select, `Reopen in Container` and you are done. Otherwise proceed to next step. 
3. Click the blue or green rectangle in the bottom left of VS code (should say something like `><` or `>< WSL`). Options should appear in the top center of your screen. Select `Reopen in Container`.


## Repository Structure

### code
[ to be filled ]

### data
[ to be filled ]
Contains details of acquiring all raw data used in repository. If data is small (<50MB) then it is okay to save it to the repo, making sure to clearly document how to the data is obtained.

If the data is larger than 50MB than you should not add it to the repo and instead document how to get the data in the README.md file in the data directory. 

This [README.md file](/data/README.md) should be kept up to date.

### notebooks
[ to be filled ]

### output
Contains intermediary/resulting data, routes, visualizations, and feasibility reports output by code

### utils
Contains files with commonly used functions stored in utility files

=======
## Project Team
* Yifan Wu, (yifwu@uchicago.edu)
* Jessica Cibrian (jescib123@gmail.com)
* Sarah Walker (swalker10@uchicago.edu)
* Huanlin Dai, (daihuanlin@uchicago.edu)

