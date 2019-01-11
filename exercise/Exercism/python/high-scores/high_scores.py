class HighScores(object):
    def __init__(self, scores):
        self.scores = scores
        self.scores_sorted = sorted(scores, reverse=True)

    def latest(self):
        return self.scores[-1]

    def personal_best(self):
        return self.scores_sorted[0]

    def personal_top(self):
        return self.scores_sorted[:3]

    def report(self):
        short = ''
        if self.scores_sorted[0] is not self.scores[-1]:
            short = str(self.scores_sorted[0] - self.scores[-1]) + " short of "
        return f"Your latest score was {self.scores[-1]}. That's {short}your personal best!"
