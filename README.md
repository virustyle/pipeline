# xPipe 1.0

## Requirements

* Python 2.7
* `pip install git+git://github.com/shotgunsoftware/python-api.git`
* `pip install PySide`

## Configuration

* `export $PIPEDEV='E:/pipeline/root/dir'`
* `export $PYTHONPATH=$PYTHONPATH:'E:/pipeline/root/dir'`

## Important Environment Variables in a project context
* Assets
`PROJECT`: Picks up the project context from this environment variable
`ASSET`: Currently active asset is known from this environment variable
`TASKSTEP`: Currently active department / process of the asset / shot will be 
known from this variable like (model/rig/lighting/fx etc.)

## Overview 

This is quick and simple pipeline based on simple directory structure and simple database
for version control and metadata information