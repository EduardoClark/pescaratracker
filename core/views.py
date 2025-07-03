from django.shortcuts import render
from .models import Game, Player, Attendance
from django.db.models import Count, Sum, Q
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from .models import Player, Attendance, Game, Team, WeeklyStanding

def home(request):
    games = Game.objects.all().order_by('week')
    players = Player.objects.all()

    total_games = games.count()
    total_wins = games.filter(result='W').count()
    total_losses = games.filter(result='L').count()
    total_ties = games.filter(result='T').count()
    total_points = total_wins * 3 + total_ties
    total_goals_for = games.aggregate(Sum('goals_for'))['goals_for__sum'] or 0
    total_goals_against = games.aggregate(Sum('goals_against'))['goals_against__sum'] or 0

    player_stats = []
    for player in players:
        attended = Attendance.objects.filter(player=player).count()
        goals = Attendance.objects.filter(player=player).aggregate(Sum('goals'))['goals__sum'] or 0
        gpg = round(goals / attended, 2) if attended else 0
        att_pct = round(attended / total_games * 100) if total_games > 0 else 0
        player_stats.append({
            'player': player,
            'games': attended,
            'goals': goals,
            'gpg': gpg,
            'att_pct': att_pct,
        })

    teams = Team.objects.all()
    latest_week = WeeklyStanding.objects.order_by('-week').first()
    max_week = latest_week.week if latest_week else 0

    team_data = []
    for team in teams:
        standings = WeeklyStanding.objects.filter(team=team).order_by('week')
        week_positions = {s.week: s.position for s in standings}
        current_points = standings.last().points if standings else 0
        team_data.append({
            'team': team,
            'points': current_points,
            'positions': week_positions,
        })

    context = {
        'games': games,
        'total_games': total_games,
        'total_wins': total_wins,
        'total_losses': total_losses,
        'total_ties': total_ties,
        'total_points': total_points,
        'total_goals_for': total_goals_for,
        'total_goals_against': total_goals_against,
        'goal_diff': total_goals_for - total_goals_against,
        'player_stats': player_stats,
        'team_data': team_data,
        'weeks': range(1, max_week + 1),
    }
    return render(request, 'core/home.html', context)

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    # Games where this player attended
    attended = Attendance.objects.filter(player=player).select_related('game')
    total_attended = attended.count()
    total_goals = sum([a.goals for a in attended])
    total_games = Game.objects.count()
    gpg = round(total_goals / total_attended, 2) if total_attended else 0
    att_pct = round(100 * total_attended / total_games) if total_games > 0 else 0

    match_performances = []
    for att in attended:
        game = att.game
        match_performances.append({
            'week': game.week,
            'date': game.date,
            'opponent': game.opponent_name,
            'opponent_logo': game.opponent_logo,
            'score': f"{game.goals_for}–{game.goals_against}",
            'goals': att.goals
        })

    context = {
        'player': player,
        'games_played': total_attended,
        'attendance': att_pct,
        'total_goals': total_goals,
        'goals_per_game': gpg,
        'match_performances': match_performances
    }
    return render(request, 'core/player_detail.html', context)

def league_table(request):
    teams = Team.objects.all()
    latest_week = WeeklyStanding.objects.order_by('-week').first()
    if latest_week:
        max_week = latest_week.week
    else:
        max_week = 0

    team_data = []
    for team in teams:
        standings = WeeklyStanding.objects.filter(team=team).order_by('week')
        week_positions = {s.week: s.position for s in standings}
        current_points = standings.last().points if standings else 0
        team_data.append({
            'team': team,
            'points': current_points,
            'positions': week_positions,
        })

    context = {
        'team_data': team_data,
        'weeks': range(1, max_week + 1),
    }
    return render(request, 'core/league_table.html', context)