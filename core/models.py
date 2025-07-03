from django.db import models

class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='player_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} #{self.number}"

class Game(models.Model):
    RESULT_CHOICES = [
        ("W", "Win"),
        ("L", "Loss"),
        ("T", "Tie"),
    ]

    week = models.PositiveIntegerField()
    date = models.DateField()
    opponent_name = models.CharField(max_length=100)
    opponent_logo = models.ImageField(upload_to='opponent_logos/', blank=True, null=True)
    goals_for = models.PositiveIntegerField()
    goals_against = models.PositiveIntegerField()
    result = models.CharField(max_length=1, choices=RESULT_CHOICES)

    attendees = models.ManyToManyField(Player, through='Attendance', related_name='attended_games')

    def __str__(self):
        return f"Week {self.week} vs {self.opponent_name} ({self.date})"

class Attendance(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('game', 'player')

    def __str__(self):
        return f"{self.player} - {self.goals} goals in {self.game}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/')

    def __str__(self):
        return self.name

class WeeklyStanding(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='standings')
    week = models.PositiveIntegerField()
    position = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    class Meta:
        unique_together = ('team', 'week')
        ordering = ['week']

    def __str__(self):
        return f"{self.team.name} - Week {self.week}"