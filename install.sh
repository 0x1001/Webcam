#!/bin/bash
#
#  Installs Web Camera third party software
#

# General update of package database
sudo apt-get -y update

# Python pip
sudo apt-get install -y python-pip

# Django
sudo pip install django

# Pydev
sudo apt-get install -y python-dev

# PiCamera
sudo apt-get install -y python-picamera

# PIL
sudo apt-get install python-imaging

# Gevent
sudo pip install gevent

# MP4Box
sudo apt-get install gpac
