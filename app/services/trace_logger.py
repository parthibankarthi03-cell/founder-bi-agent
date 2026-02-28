class TraceLogger:

    def __init__(self):
        self.steps = []

    def add(self, action, details):
        self.steps.append({
            "action": action,
            "details": details
        })

    def get_trace(self):
        return self.steps