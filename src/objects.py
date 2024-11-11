class GitHubIssue:
    def __init__(self, id, title, description, milestone, labels, assignees, state, state_reason):
        self.id = id
        self.title = title
        self.description = description
        self.milestone = milestone
        self.labels = labels
        self.assignees = assignees
        self.state = state
        self.state_reason = state_reason

    def __str__(self):
        return (f"Issue ID: {self.id}\n"
                f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Milestone: {self.milestone}\n"
                f"Labels: {', '.join(self.labels)}\n"
                f"Assignees: {', '.join(self.assignees)}\n"
                f"State: {self.state}\n"
                f"State Reason: {self.state_reason}")
    