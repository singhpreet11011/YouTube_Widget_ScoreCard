from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40rshBains0219@localhost/scorecard_widget' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Teams model
class Team(db.Model):
    __tablename__ = 'Teams'
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
   

# Define the Matches model
class Match(db.Model):
    __tablename__ = 'Matches'
    match_id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('Teams.team_id'))
    match_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('scheduled', 'in_progress', 'completed'), default='scheduled')
 

# Define the Scores model
class Score(db.Model):
    __tablename__ = 'Scores'
    score_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('Matches.match_id'))
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)
    

# Define the Score Updates model
class ScoreUpdate(db.Model):
    __tablename__ = 'Score_Updates'
    update_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('Matches.match_id'))
    score1 = db.Column(db.Integer)
    score2 = db.Column(db.Integer)
    

# API to get all matches
@app.route('/matches', methods=['GET'])
def get_matches():
    matches = Match.query.all()
    return jsonify([{
        'match_id': match.match_id,
        'team1_id': match.team1_id,
        'team2_id': match.team2_id,
        'match_date': match.match_date,
        'status': match.status
    } for match in matches])

# API to get scores for a specific match
@app.route('/matches/<int:match_id>/scores', methods=['GET'])
def get_scores(match_id):
    score = Score.query.filter_by(match_id=match_id).first()
    if score:
        return jsonify({
            'team1_score': score.team1_score,
            'team2_score': score.team2_score
        })
    return jsonify({'message': 'Match not found'}), 404

@app.route('/matches/<int:match_id>/updates', methods=['POST'])
def add_score_update(match_id):
    data = request.get_json()

    # Validate input
    if 'score1' not in data or 'score2' not in data:
        return jsonify({'message': 'Score1 and Score2 must be provided'}), 400

    # Create a new score update
    new_update = ScoreUpdate(match_id=match_id, score1=data['score1'], score2=data['score2'])
    db.session.add(new_update)

    # Update the Scores table
    score = Score.query.filter_by(match_id=match_id).first()
    if score:
        score.team1_score = data['score1']
        score.team2_score = data['score2']
    else:
        # If no score entry exists, create a new one
        score = Score(match_id=match_id, team1_score=data['score1'], team2_score=data['score2'])
        db.session.add(score)

    db.session.commit()
    
    return jsonify({'message': 'Score updated successfully'}), 201

# API to serve the widget
@app.route('/widget/<int:match_id>', methods=['GET'])
def score_widget(match_id):
    # Get match details
    match = Match.query.filter_by(match_id=match_id).first()
    if not match:
        return "Match not found", 404
    
    # Get team names
    team1 = Team.query.filter_by(team_id=match.team1_id).first()
    team2 = Team.query.filter_by(team_id=match.team2_id).first()
    
    team1_name = team1.team_name if team1 else "Team 1"
    team2_name = team2.team_name if team2 else "Team 2"

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scorecard Widget</title>
        <style>
            #scorecard {{
                font-family: Arial, sans-serif;
                border: 1px solid #ccc;
                padding: 10px;
                width: 200px;
                text-align: center;
                margin-top: 0px; /* Less margin at the top */
            }}
            h2 {{
                margin-top: 0; /* No margin at the top of Scorecard text */
                margin-bottom: 10px; /* Margin below Scorecard title */
            }}
            .score {{
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px; /* Margin below the score */
            }}
            h3 {{
                margin-top: 0px; /* Less margin above team names */
                margin-bottom: 10px; /* Margin below team names */
            }}
            button {{
                margin-top: 0px; /* Margin above the button */
                padding: 3px 6px; /* Reduced padding for a smaller button */
                font-size: 14px; /* Smaller font size for button */
            }}
        </style>
    </head>
    <body>
        <div id="scorecard">
            <h2>Scorecard</h2>
            <div class="score" id="score">Loading...</div>
            <h3>{team1_name} vs {team2_name}</h3>
            <button onclick="refreshScore()">Refresh Score</button>
        </div>
        <script>
            async function fetchScores() {{
                const response = await fetch('/matches/' + {match_id} + '/scores');
                if (response.ok) {{
                    const data = await response.json();
                    document.getElementById('score').innerText = data.team1_score + ' - ' + data.team2_score;
                }} else {{
                    document.getElementById('score').innerText = 'Match not found';
                }}
            }}
            function refreshScore() {{
                fetchScores();
            }}
            // Set interval to refresh score every 2 seconds
            setInterval(fetchScores, 2000);
            // Initial fetch
            fetchScores();
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=8000)



