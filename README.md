# Project Title

This is a basic README file for the project.

## Description

This project provides a Python script designed to automate the transfer of issues from a GitLab project to a GitHub project. It is particularly well-suited for smaller projects and should ideally be managed by a single administrator. This tool is most effective for mirrored repositories, which are typically read-only.

Due to GitHub's lack of an API for deleting issues, the following conditions must be met:

- Issues in the original repository must neither have been deleted previously nor be deleted in the future; they should be either reused or closed.
- The created issues in the GitHub repository will always be modified by this script; never manually
- Milestones from the original repository must be present in the GitHub repository with matching IDs.

Additional considerations include:

- Although new labels will be created automatically, they may not have the same descriptions or colors as those in the original repository.

## Getting Started

### System Overview

Describes the architecture and major components of the system.

### Start the Application

Instructions for setting up and launching the project.
