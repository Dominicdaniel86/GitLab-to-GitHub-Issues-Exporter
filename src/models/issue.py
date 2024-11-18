class Issue:
    def __init__(self, id, title, description, labels, state, milestone_id, milestone_title, assignees):
        self.id = id # int
        self.title = title # str
        self.description = description # str
        self.labels = labels # list
        self.state = state # str
        self.milestone_id = milestone_id # str
        self.milestone_title = milestone_title # int
        self.assignees = assignees # list

    def __str__(self):
        return (f"Issue ID: {self.id}\n"
                f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Labels: {', '.join(self.labels)}\n"
                f"State:  {self.state}\n"
                f"Milestone ID: {self.milestone_id}\n"
    	        f"Milestone Title: {self.milestone_title}\n"
                f"Assignees: {', '.join(self.assignees)}\n")

    def __eq__(self, other):
        if not isinstance(other, Issue):
            return NotImplemented

        return (self.id == other.id and
                self.title == other.title and
                self.description == other.description and
                sorted(self.labels) == sorted(other.labels) and
                self.state == other.state and
                self.milestone_title == other.milestone_title and
                sorted(self.assignees) == sorted(other.assignees))

    def to_create_dict(self):
        return {
            'title': self.title,
            'body': self.description,
            'labels': self.labels,
            'milestone': self.milestone_id,
            'assignees': self.assignees
        }

    def to_update_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.description,
            'labels': self.labels,
            'state': self.state,
            'milestone': self.milestone_id,
            'assignees': self.assignees
        }
