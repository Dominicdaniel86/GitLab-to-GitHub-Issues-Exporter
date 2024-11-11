# GitHub Issue Importer

## Description

This tool automates the transfer of issues from a GitLab project to a GitHub repository, ideal for smaller, mirrored projects managed by a single administrator. It's designed to reflect the current state of issues on GitHub, maintaining consistency across platforms despite some technical limitations.

## Technical Considerations

There are two important technical limitations, which result out of GitHub's lack for certain APIs, e.g. for delting an issue.

### Regarding Issues

You have two options:

1. either run the script once, which gurantees one export which will always work
2. or run this script regulary, to show the current issue state in GitHub while developing

To run it regulary, certain conditions must be met:

- Issues in the original repository must neither have been deleted previously nor be deleted in the future; they should be either reused or closed
- The created issues in the GitHub repository will always be modified by this script; never manually

### Labels and Milestones

The script automatically creates missing labels, but might not replicate descriptions or colors exactly. Milestones must be predefined in GitHub with corresponding IDs to ensure a smooth transfer.

### Assignee Matching

Usernames for assignees must match exactly across both platforms to enable a correct export. If the project members or their usernames vary, assignees cannot be exported.

## Usage and Configuration

To use this script, you will need a Python Interpreter with version 3.10 or higher.
Configure the script by editing the parameters at the top of main.py:

- set the URLs of both repositories
- specify whether assignees are importable
- the number of issues

## Getting Started

Here's how to run your first migration:

1. Installl Python 3.10+ if not already installed
2. Clone the project and open main.py
3. Adjust the parameters as described in the Usage section
4. Execute the script from your command line by navigating to the *src* folder and running *python main.py*
