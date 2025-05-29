#!/usr/bin/env python3

# Src: https://colab.research.google.com/github/allegroai/clearml/blob/master/docs/tutorials/Getting_Started_3_Remote_Execution.ipynb#scrollTo=gRz3FQFdjKcC

from clearml import Task

tasks = Task.get_tasks(project_name="Snippets", task_name="MNIST Dense Layers")

print([(task.name, task.id) for task in tasks])