#!/bin/bash
wmctrl -l | awk '{print $1}' | xargs -n1 wmctrl -ic
