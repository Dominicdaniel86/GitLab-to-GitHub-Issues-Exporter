# GitHub Issue Importer

## Description

This tool automates the transfer of issues from a GitLab project to a GitHub repository, ideal for projects that are mirrored between the platforms. It ensures that GitHub reflects the current state of issues, maintaining consistency across both environments.

## Customizability

Issues:

- ID and Title are always exported

Labels:

- Export feature for labels can be toggled on or off
- Optionally, choose to create missing labels on GitHub or export only existing ones. Newly created labels will adopt a default color and description, as custom settings from GitLab are not imported

Milestones:

- Export feature for milestones can be toggled on or off
- Missing milestones will not be exported. Choose whether this reults in an export failure or if they are simply ignored

Assignees:

- Export feature for assignees can be toggled on or off
- Assignees must have the same username on both platforms and be a contributer to both projects
- Missing assignees are not exported. Choose whether this results in an export failure or if they are simply ignored

Description:

- Export feature for the description can be toggled on or off
- On GitHub, descriptions are added as comments. Choose to either add a new comment with the updated description or if existing comments will be overwritten by a new one

## Technical Considerations

### Regarding Issues

You have two options:

1. Run the script once to gurantee a successful single export
2. Run the script regulary to reflect ongoing changes on GitHub. This apporach adds new issues and updates existing ones. However, deleting issues in GitLab created placeholder issues in GitHub to maintain ID consistency, as GitLab's API does not currently support issued deletion through an API. You can avoid this by not deleting issues on GitLab

### Labels and Milestones

The script can automatically create missing labels but might not exactly replicate their descriptions or colors. Milestones must be predefined with corresponding in GitHub to ensure a seamless transfer.

### Assignee Matching

Assignees must have identical usernames across both platforms and be added as contributors to be correcly exported.

## Usage and Configuration

Requirements: Python 3.10 or higher.

Configure the script by modifying the parameters at the top of main.py:

- Set the URLs of both repositories
- Input the corresponding access tokens
- Adjust the customizable options as needed

## Getting Started

1. Install Python 3.10+ if it's not already installed
2. Clone the project and open main.py
3. Adjust the parameters as described in the Usage section
4. Execute the script by navigating to the *src* folder and running *python main.py* from your command line

## Future Updates

Currently planned future updates:

- Option to export all labels and milestones from a GitLab project to the GitHub project
- Enhanced robustness with additional safety checks
- A user-friendly interface, using Tkinter
- Providing a standalone installation that eliminates the need for a installed Python interpreter
- Exporting issues from GitHub to GitLab (in the distant future)

Not planned:

- Exports between the same platform
- Implementing a workaround to prevent the creation of placeholder issues. Doing so would significantly reduce the clarity and detail of the export feedback, such as the number of issues added or updated
