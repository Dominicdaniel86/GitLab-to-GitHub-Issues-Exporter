class GitHubIssue:
    def __init__(self, id, title, description, assignee, milestone, labels, assignees, state, state_reason):
        self.id = id
        self.title = title
        self.description = description
        self.assignee = assignee
        self.milestone = milestone
        self.labels = labels
        self.assignees = assignees
        self.state = state
        self.state_reason = state_reason
