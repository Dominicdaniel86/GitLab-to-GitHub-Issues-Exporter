class GitHubIssue:
    def __init__(self, id, title, description, milestone, labels, assignees, state):
        self.id = id
        self.title = title
        self.description = description
        self.milestone = milestone
        self.labels = labels
        self.assignees = assignees
        self.state = state

    def __str__(self):
        return (f"Issue ID: {self.id}\n"
                f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Milestone: {self.milestone}\n"
                f"Labels: {', '.join(self.labels)}\n"
                f"Assignees: {', '.join(self.assignees)}\n"
                f"State: {self.state}\n")
    
    def __eq__(self, other):
        if not isinstance(other, GitHubIssue):
            return NotImplemented

        return (self.id == other.id and
                self.title == other.title and
                # self.description == other.description and
                self.milestone == other.milestone and
                self.labels == other.labels and
                # self.assignees == other.assignees and
                self.state == other.state)
    
    def to_add_dict(self):
        return {
            'title': self.title,
            # 'body': self.description,
            # 'assignees': self.assignees,
            'milestone': self.milestone,
            'labels': self.labels
        }

    def to_modify_dict(self):
        return {
            'title': self.title,
            # 'body': self.description,
            # 'assignees': self.assignees,
            'milestone': self.milestone,
            'labels': self.labels,
            'state': self.state,
        }