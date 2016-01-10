#!/bin/sh

# Print columns 2, 3 and 11 of 'ps aux'

ps aux | awk '{print $2, $3, $11}'
