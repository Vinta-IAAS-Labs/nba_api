# NBA API MCP Server - Example Usage

This document provides practical examples of using the NBA API MCP Server with Claude.

## Setup

After configuring the server in Claude Desktop (see README.md), you can use natural language to interact with NBA data.

## Example Conversations

### Example 1: Finding and Analyzing a Player

**You:** "Find information about LeBron James and show me his career statistics"

**Claude will:**
1. Use `find_players` with name "LeBron James"
2. Extract the player ID from the results
3. Use `get_player_info` to get detailed information
4. Use `get_player_career_stats` to get career stats
5. Present the information in an organized, readable format

### Example 2: Comparing Players

**You:** "Compare the career stats of Michael Jordan and LeBron James"

**Claude will:**
1. Find both players using `find_players`
2. Get career stats for both players
3. Create a comparison showing key statistics side-by-side

### Example 3: Team Analysis

**You:** "Show me the current Lakers roster and their recent game results"

**Claude will:**
1. Use `find_teams` to find the Lakers
2. Use `get_team_roster` to get the current roster
3. Use `get_team_game_log` to get recent games
4. Present the roster with player details and recent performance

### Example 4: Live Game Tracking

**You:** "What NBA games are happening today and what are the scores?"

**Claude will:**
1. Use `get_todays_scoreboard` to fetch live data
2. Present current scores, game status, and quarter information
3. Highlight close games or noteworthy performances

### Example 5: League Leaders

**You:** "Who are the top 10 scorers in the NBA this season?"

**Claude will:**
1. Use `get_league_leaders` with stat_category "PTS"
2. Present the top scorers with their points per game
3. Provide context about their performance

### Example 6: Historical Analysis

**You:** "Show me Stephen Curry's performance in the 2015-16 season"

**Claude will:**
1. Find Stephen Curry using `find_players`
2. Use `get_player_game_log` with season "2015-16"
3. Analyze game-by-game performance
4. Calculate averages and highlight best games

### Example 7: Team Statistics

**You:** "Which team has the best offensive rating this season?"

**Claude will:**
1. Use `get_team_stats` to get all team statistics
2. Sort by offensive rating
3. Present top teams with relevant metrics

### Example 8: Player Comparison by Position

**You:** "Compare all starting point guards' assist numbers this season"

**Claude will:**
1. Use `get_player_stats` to get all player statistics
2. Filter for point guards
3. Sort by assists
4. Present comparison with context

### Example 9: Game Analysis

**You:** "Give me the boxscore for game ID 0022400125"

**Claude will:**
1. Use `get_game_boxscore` with the game ID
2. Present player statistics for both teams
3. Highlight top performers
4. Show final score and game details

### Example 10: Draft Analysis

**You:** "Find all players from the 2003 NBA draft and compare their careers"

**Claude will:**
1. Use `find_players` to search for players (may need multiple searches)
2. Get career stats for each player
3. Create a comprehensive comparison
4. Rank players by career achievements

## Advanced Queries

### Multi-Step Analysis

**You:** "Analyze the Nuggets' championship run in 2023"

**Claude will:**
1. Find the Nuggets team
2. Get their playoff game log for 2022-23
3. Get roster information
4. Analyze key games and player performances
5. Present a comprehensive narrative

### Statistical Trends

**You:** "Has Luka Dončić improved his three-point shooting over the years?"

**Claude will:**
1. Find Luka Dončić
2. Get career stats with yearly breakdown
3. Analyze three-point percentage trends
4. Provide year-over-year comparison

### Team Building Analysis

**You:** "What players on the Celtics roster have playoff experience?"

**Claude will:**
1. Find the Celtics
2. Get current roster
3. For each player, check career stats for playoff games
4. Summarize playoff experience

## Tips for Best Results

1. **Be Specific**: Include full names or specific details
   - Good: "LeBron James career stats"
   - Less good: "LeBron stats"

2. **Use Proper Seasons**: Format seasons as "YYYY-YY"
   - Good: "2023-24 season"
   - Less good: "last season"

3. **Player/Team IDs**: If you know them, they're faster
   - "Get stats for player ID 2544"

4. **Combine Requests**: Ask for multiple things at once
   - "Compare Jokić and Embiid's stats and show their head-to-head games"

5. **Current Data**: For live games, be aware of time zones
   - "Today's scoreboard" shows games for the current date

## Common Use Cases

### Fantasy Basketball
- "Who are the top rebounders available as free agents?"
- "Compare player X and player Y for my fantasy team"
- "Show me players averaging over 20 points per game"

### Sports Analysis
- "Analyze the Warriors' three-point shooting efficiency"
- "Which teams have the best home court advantage?"
- "Compare rookie performances this season"

### Historical Research
- "Show me the career progression of Tim Duncan"
- "Compare the 1996 Bulls to the 2017 Warriors"
- "Who were the leading scorers in the 2000s?"

### Betting/Odds Analysis
- "What's the recent form of teams playing tonight?"
- "Show me head-to-head records between Lakers and Celtics"
- "Which team has the best record in close games?"

## Error Handling Examples

If a request fails, Claude will inform you and might suggest alternatives:

**You:** "Get stats for player ID 999999999"

**Claude:** "That player ID doesn't exist. Let me search for the player by name instead. What's the player's name?"

## Rate Limiting

If you make many requests quickly, you might hit rate limits:

**Claude:** "I'm hitting rate limits from the NBA API. Let me wait a moment and try again."

The server handles this gracefully and will retry when appropriate.
