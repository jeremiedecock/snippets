#!/bin/bash

# Infinite loop
while true; do
  quarto render dashboard_datetime.qmd
  sleep 60      # Wait for 60 seconds
done
