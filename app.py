from flask import Flask, render_template
import sys
# Add the directory containing analysis_engine to the Python path
sys.path.append("/home/ubuntu")
import analysis_engine
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    # Get top picks data from the analysis engine
    # In a real app, you might adjust the number of picks based on settings
    top_picks = analysis_engine.get_daily_top_picks(num_picks=5) 
    
    # Prepare data for the analytical table (example: using the first pick's reasoning)
    # This needs refinement for actual interaction (e.g., clicking a row)
    analytical_data = []
    if top_picks:
        first_pick = top_picks[0]
        analytical_data.append({
            "bet": first_pick["bet_type"],
            "reason": "\n".join(first_pick["reasoning"]),
            "data_source": "Simulated H2H, Form, Stats" # Placeholder
        })
        # Add more reasoning details if available in the pick object
        # Example: Add specific stats used if the engine provided them
        if 'match_obj' in first_pick and first_pick['match_obj'].current_stats:
             stats = first_pick['match_obj'].current_stats
             team_a = first_pick['match_obj'].team_a
             team_b = first_pick['match_obj'].team_b
             if first_pick['match_obj'].sport == 'football':
                 analytical_data[0]["data_source"] += f"; {team_a} Corners Avg: {stats[team_a].corners_avg:.1f}, {team_b} Corners Avg: {stats[team_b].corners_avg:.1f}"

    return render_template('index.html', top_picks=top_picks, analytical_data=analytical_data)

@app.route('/football')
def football():
    # Get football matches and bets
    football_matches = []
    football_bets = []
    
    # Create some example football matches
    match1 = analysis_engine.Match("football", "Chelsea", "Arsenal", datetime.now(), "Premier League")
    match2 = analysis_engine.Match("football", "Man City", "Liverpool", datetime.now(), "Premier League")
    match3 = analysis_engine.Match("football", "Barcelona", "Real Madrid", datetime.now(), "La Liga")
    
    # Fetch data and analyze
    matches = [match1, match2, match3]
    for match in matches:
        match = analysis_engine.fetch_match_data(match)
        football_matches.append(match)
        
        analysis = analysis_engine.analyze_football_match(match)
        if analysis:
            match.analysis_results = analysis
            suggestions = analysis_engine.suggest_bets(match)
            football_bets.extend(suggestions)
    
    return render_template('football.html', football_matches=football_matches, football_bets=football_bets)

@app.route('/tennis')
def tennis():
    # Get tennis matches and bets
    tennis_matches = []
    tennis_bets = []
    
    # Create some example tennis matches
    match1 = analysis_engine.Match("tennis", "Djokovic", "Alcaraz", datetime.now(), "Wimbledon")
    match2 = analysis_engine.Match("tennis", "Nadal", "Federer", datetime.now(), "Roland Garros")
    match3 = analysis_engine.Match("tennis", "Swiatek", "Sabalenka", datetime.now(), "US Open")
    
    # Fetch data and analyze
    matches = [match1, match2, match3]
    for match in matches:
        match = analysis_engine.fetch_match_data(match)
        tennis_matches.append(match)
        
        analysis = analysis_engine.analyze_tennis_match(match)
        if analysis:
            match.analysis_results = analysis
            suggestions = analysis_engine.suggest_bets(match)
            tennis_bets.extend(suggestions)
    
    return render_template('tennis.html', tennis_matches=tennis_matches, tennis_bets=tennis_bets)

@app.route('/chess')
def chess():
    # Get top 5 chess players
    top_chess_players = analysis_engine.get_top_chess_players(5)
    
    # Get chess matches and bets
    chess_matches = []
    chess_bets = []
    
    # Create some example chess matches - mix of top 5 and non-top 5 players
    match1 = analysis_engine.Match("chess", "Magnus Carlsen", "Fabiano Caruana", datetime.now(), "World Championship")
    match2 = analysis_engine.Match("chess", "Ding Liren", "Ian Nepomniachtchi", datetime.now(), "Candidates Tournament")
    match3 = analysis_engine.Match("chess", "Magnus Carlsen", "Alireza Firouzja", datetime.now(), "Norway Chess")
    match4 = analysis_engine.Match("chess", "Magnus Carlsen", "Hikaru Nakamura", datetime.now(), "Speed Chess Championship")
    match5 = analysis_engine.Match("chess", "Wesley So", "Levon Aronian", datetime.now(), "Grand Chess Tour")
    
    # Fetch data and analyze - only for matches involving top 5 players
    matches = [match1, match2, match3, match4, match5]
    for match in matches:
        # Check if both players are in top 5 before analyzing
        if match.team_a in top_chess_players and match.team_b in top_chess_players:
            match = analysis_engine.fetch_match_data(match)
            chess_matches.append(match)
            
            analysis = analysis_engine.analyze_chess_match(match)
            if analysis:
                match.analysis_results = analysis
                suggestions = analysis_engine.suggest_bets(match)
                chess_bets.extend(suggestions)
        elif match.team_a in top_chess_players or match.team_b in top_chess_players:
            # If at least one player is in top 5, show the match but don't analyze
            match.status = "لا يتم تحليلها (أحد اللاعبين خارج أفضل 5)"
            chess_matches.append(match)
    
    return render_template('chess.html', chess_matches=chess_matches, chess_bets=chess_bets, top_chess_players=top_chess_players)

@app.route('/chat')
def chat():
    # Placeholder for chat functionality
    return render_template('chat.html')

@app.route('/settings')
def settings():
    # Placeholder for settings functionality
    return render_template('settings.html')

if __name__ == '__main__':
    # Listen on all interfaces, essential for exposing the port later
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
