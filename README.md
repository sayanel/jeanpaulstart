# Jean Paul Start

_L'enfer, c'est les .bats_

- Execution de batches avec une syntaxe proche de celle d'Ansible

- Fenêtre affichant les icônes correspondant aux batches

## Installation

````bash
pip install git+https://github.com/cube-creative/jeanpaulstart.git
````

## Configuration

### Batches

Un batch décrit un environnement à travers des variables, puis des actions à executer

Exemple pour lancer 3Ds Max

````yaml
---
name: 3Ds Max 2016
icon_path: $ENVIRONMENT\_config\jean-paul-start\icons\max-2016.png
tags: 
  - DCC
  - 3D
  - Max
environment:
  CUBE_ENVIRONMENT: production
  CUBE_MAX_SCRIPTS: $ENVIRONMENT\max-2016
  MAX_VERSION: 2016
  MAX_NAME: Max-$MAX_VERSION
  MAX_DIRECTORY: C:\Program Files\Autodesk\3ds Max $MAX_VERSION
  PYTHONPATH:
    - $MAX_DIRECTORY\python\Lib
    - $ENVIRONMENT\max-2016
    - $ENVIRONMENT\max-2016\python
  INI_TEMPLATE: $ENVIRONMENT\max-2016\config\3dsmax-ini-default-$MAX_VERSION.ini.j2
  INI_SOURCE: $LOCALAPPDATA\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\3dsmax.ini
  INI_TARGET: $LOCALAPPDATA\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\${MAX_NAME}_3dsmax.ini
  PLUGIN_INI_SOURCE: $CUBE_MAX_SCRIPTS\config\Plugin.UserSettings.ini.j2
  PLUGIN_INI_TARGET: $LOCALAPPDATA\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\${MAX_NAME}_Plugin_UserSettings.ini

tasks:
  - name: Copy 3dsmax.ini template if missing
    template:
      src: $INI_TEMPLATE
      dest: $INI_SOURCE
      force: no
      
  - name: Create custom 3dsmax.ini if missing
    copy:
      src: $INI_SOURCE
      dest: $INI_TARGET
      force: no
      
  - name: Additional Icons
    ini_file:
      src: $INI_TARGET
      state: present
      section: Directories
      option: Additional Icons
      value: $ENVIRONMENT\max-2016\resources\icons

  - name: Startup Scripts
    ini_file:
      src: $INI_TARGET
      state: present
      section: Directories
      option: Startup Scripts
      value: $CUBE_MAX_SCRIPTS\maxscript\startupscripts

  - name: AutoBackup Enable
    ini_file:
      src: $INI_TARGET
      state: present
      section: AutoBackup
      value: 1

  - name: Launch 3DS Max 2016
    raw: 
      command: "\"$MAX_DIRECTORY\\3dsmax.exe\" -p ${MAX_NAME}_Plugin_UserSettings.ini %* -i ${MAX_NAME}_3dsmax.ini"
...
````
