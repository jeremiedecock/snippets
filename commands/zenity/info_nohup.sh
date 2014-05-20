#!/bin/sh

# This can be used with Cron, for instance:
#    30 17 * * * DISPLAY=:0 zenity --info --text="C'est l'heure..."

DISPLAY=:0 zenity --info --title "Hello" --text "hello\nworld"
