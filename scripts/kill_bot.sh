#!/usr/bin/bash

cat nicbot.pid | xargs kill
rm nicbot.pid
