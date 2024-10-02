# YouTube Scorecard Widget Project

This project is a football scorecard widget designed to provide real-time match updates by YouTube. The widget is easily embeddable on external websites using an iframe. The backend is built using Flask and connects to a MySQL database that stores information about teams, matches, and score updates.

## Database Design

### New Entities
The following entities were created to support football match tracking and real-time score updates:

#### Teams
- **team_id**: Unique identifier for each team (Primary Key).
- **team_name**: Name of the team.

#### Matches
- **match_id**: Unique identifier for each match (Primary Key).
- **team1_id**: Foreign Key 
- **team2_id**: Foreign Key 
- **match_date**: Scheduled DateTime
- **status**: Current status of the match (scheduled, in_progress, completed).

#### Scores
- **score_id**: Unique identifier for each score entry (Primary Key).
- **match_id**: Foreign Key referencing the match.
- **team1_score**: Current score for the first team.
- **team2_score**: Current score for the second team.
- **updated_at**: Timestamp when the score was last updated.

#### Score Updates
- **update_id**: Unique identifier for each score update (Primary Key).
- **match_id**: Foreign Key referencing the match.
- **score1**: New score for the first team.
- **score2**: New score for the second team.
- **update_time**: Timestamp when the score update was made.

### Existing Entities (Related to YouTube-like Features)
Assuming the existing entities that YouTube might already have, there are many entities we can consider. However, for this project, we will focus on the entities that are most relevant to our scorecard widget:


#### Live Streams
- **stream_id**: Unique identifier for the live stream.
- **stream_title**: Title of the live stream.
- **start_time**: When the stream begins.
- **end_time**: When the stream ends.
- **Match_id**: ID of the match being streamed.

#### Stream Chat
- **chat_id**: Unique identifier for each chat message.
- **stream_id**: Foreign Key referencing the live stream.
- **user_id**: ID of the user sending the message.
- **message**: Content of the chat message.
- **timestamp**: When the message was sent.

#### Stream Viewers
- **viewer_id**: Unique identifier for each viewer.
- **stream_id**: Foreign Key referencing the live stream.
- **user_id**: ID of the viewer.

## APIs

To allow interaction with the scorecard widget, the following RESTful APIs were developed:

### Fetch All Matches
- **Endpoint**: `/matches`
- **Method**: GET
- **Description**: Retrieves a list of all matches, including details like match date and status.
```http
  GET http://localhost:8000/matches

[
  {
    "match_id": 1,
    "team1_id": 101,
    "team2_id": 102,
    "match_date": "2024-10-05T15:00:00Z",
    "status": "scheduled",
  },
  {
    "match_id": 2,
    "team1_id": 103,
    "team2_id": 104,
    "match_date": "2024-10-06T15:00:00Z",
    "status": "in_progress",
  }
]
  ````

### Fetch Scores for a Specific Match
- **Endpoint**: `/matches/<int:match_id>/scores`
- **Method**: GET
- **Description**: Retrieves the current scores for a specified match.
```
  GET http://localhost:8000/matches/1/scores

{
  "match_id": 1,
  "team1_score": 2,
  "team2_score": 1,
  "updated_at": "2024-10-05T16:00:00Z"
}

  ```

### Submit Score Update
- **Endpoint**: `/matches/<int:match_id>/updates`
- **Method**: POST
- **Description**: Allows score updates for a specific match. The POST request adds a new score entry to the Score_Updates table and updates the main Scores table.

```
POST http://localhost:8000/matches/1/updates
Content-Type: application/json

{
  "score1": 3,
  "score2": 2
}

```

## Embedding the Scorecard Widget

Users can easily embed the scorecard widget into their websites using an iframe. This widget will display live scores for the selected match.

### Steps to Embed:
1. **Copy the iFrame Code**:
   ```html
   <iframe src="http://localhost:8000/widget/1" width="320" height="150" frameborder="0" scrolling="no"></iframe>

2. **Update the Match ID**: The `/widget/1` in the URL refers to match ID 1. Modify this to display a different match by changing the match ID in the URL. For example, use `/widget/2` for match ID 2.

3. **Resize the iFrame**: Adjust the width and height attributes as necessary to fit the design of your website.

4. **Paste the Code**: Embed the updated iFrame code directly into your website's HTML to display the widget.
You can copy and paste this into your README file. Let me know if you need any further 


