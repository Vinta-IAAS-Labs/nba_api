# NBA API MCP Server

A Model Context Protocol (MCP) server that provides access to NBA statistics, player information, team data, and live game scores through the nba_api package.

## Features

The NBA API MCP Server exposes 12 powerful tools for accessing NBA data:

### Player Tools
- **find_players**: Search for players by name (supports partial matches)
- **get_player_info**: Get detailed player information including personal details and draft info
- **get_player_career_stats**: Get complete career statistics (regular season, playoffs, all-star)
- **get_player_game_log**: Get game-by-game statistics for a specific season

### Team Tools
- **find_teams**: Search for teams by name, city, state, or nickname
- **get_team_roster**: Get current roster for a specific team
- **get_team_game_log**: Get recent game results and statistics for a team
- **get_team_stats**: Get current season statistics for all NBA teams

### Live Data Tools
- **get_todays_scoreboard**: Get live scores and status for all games today
- **get_game_boxscore**: Get detailed boxscore statistics for a specific game

### League Tools
- **get_league_leaders**: Get league leaders in various statistical categories
- **get_player_stats**: Get current season statistics for all NBA players

## Installation

### Prerequisites

This MCP server requires Python 3.10 or higher.

### Installation Steps

1. **Install the nba_api package and its dependencies:**

```bash
pip install nba_api
```

2. **Install the MCP SDK:**

```bash
pip install mcp>=1.0.0
```

Alternatively, install all dependencies at once from the mcp_server directory:

```bash
cd mcp_server
pip install -r requirements.txt
```

Or install the nba_api package in development mode from the parent directory:

```bash
# From the nba_api root directory
pip install -e .
pip install mcp>=1.0.0
```

## Usage

### Running the Server

The MCP server can be run directly:

```bash
python mcp_server/server.py
```

### Configuring with Claude Desktop

To use this server with Claude Desktop, add the following configuration to your Claude Desktop config file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "nba-api": {
      "command": "python",
      "args": ["/absolute/path/to/nba_api/mcp_server/server.py"]
    }
  }
}
```

Replace `/absolute/path/to/nba_api/` with the actual path to your nba_api directory.

### Alternative: Using uv (Recommended)

If you have `uv` installed, you can use this configuration:

```json
{
  "mcpServers": {
    "nba-api": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/nba_api/mcp_server",
        "run",
        "server.py"
      ]
    }
  }
}
```

## Example Usage

Once configured, you can interact with the NBA API through Claude. Here are some example prompts:

### Finding Players
```
Find information about LeBron James
```

### Getting Player Stats
```
Get career statistics for player ID 2544 (LeBron James)
```

### Team Information
```
Find the Lakers team and get their current roster
```

### Live Scores
```
What are today's NBA game scores?
```

### League Leaders
```
Who are the top scorers in the NBA this season?
```

## Tool Reference

### find_players
Search for NBA players by name.

**Parameters:**
- `name` (required): Player name or partial name
- `active_only` (optional): Only return active players (default: false)

**Example:**
```json
{
  "name": "Curry",
  "active_only": true
}
```

### get_player_info
Get detailed player information.

**Parameters:**
- `player_id` (required): NBA player ID

**Example:**
```json
{
  "player_id": "201939"
}
```

### get_player_career_stats
Get career statistics for a player.

**Parameters:**
- `player_id` (required): NBA player ID
- `per_mode` (optional): "Totals", "PerGame", or "Per36" (default: "PerGame")

**Example:**
```json
{
  "player_id": "2544",
  "per_mode": "PerGame"
}
```

### get_player_game_log
Get game-by-game statistics.

**Parameters:**
- `player_id` (required): NBA player ID
- `season` (optional): Season format "YYYY-YY" (default: "2024-25")
- `season_type` (optional): "Regular Season" or "Playoffs" (default: "Regular Season")

**Example:**
```json
{
  "player_id": "203999",
  "season": "2024-25",
  "season_type": "Regular Season"
}
```

### find_teams
Search for NBA teams.

**Parameters:**
- `query` (required): Search term
- `search_by` (optional): "name", "city", "state", or "nickname" (default: "name")

**Example:**
```json
{
  "query": "Lakers",
  "search_by": "nickname"
}
```

### get_team_roster
Get team roster.

**Parameters:**
- `team_id` (required): NBA team ID
- `season` (optional): Season format "YYYY-YY" (default: "2024-25")

**Example:**
```json
{
  "team_id": "1610612747",
  "season": "2024-25"
}
```

### get_team_game_log
Get team game log.

**Parameters:**
- `team_id` (required): NBA team ID
- `season` (optional): Season format "YYYY-YY" (default: "2024-25")
- `season_type` (optional): "Regular Season" or "Playoffs" (default: "Regular Season")

**Example:**
```json
{
  "team_id": "1610612747",
  "season": "2024-25"
}
```

### get_todays_scoreboard
Get today's games and scores.

**Parameters:** None

### get_game_boxscore
Get game boxscore.

**Parameters:**
- `game_id` (required): NBA game ID

**Example:**
```json
{
  "game_id": "0022400001"
}
```

### get_league_leaders
Get league leaders.

**Parameters:**
- `stat_category` (optional): "PTS", "REB", "AST", "FG_PCT", "FG3_PCT", "FT_PCT", "STL", "BLK" (default: "PTS")
- `season` (optional): Season format "YYYY-YY" (default: "2024-25")
- `season_type` (optional): "Regular Season" or "Playoffs" (default: "Regular Season")

**Example:**
```json
{
  "stat_category": "PTS",
  "season": "2024-25"
}
```

### get_team_stats
Get team statistics.

**Parameters:**
- `season` (optional): Season format "YYYY-YY" (default: "2024-25")
- `season_type` (optional): "Regular Season" or "Playoffs" (default: "Regular Season")

**Example:**
```json
{
  "season": "2024-25",
  "season_type": "Regular Season"
}
```

### get_player_stats
Get player statistics.

**Parameters:**
- `season` (optional): Season format "YYYY-YY" (default: "2024-25")
- `season_type` (optional): "Regular Season" or "Playoffs" (default: "Regular Season")
- `per_mode` (optional): "Totals", "PerGame", or "Per36" (default: "PerGame")

**Example:**
```json
{
  "season": "2024-25",
  "per_mode": "PerGame"
}
```

## Common Player and Team IDs

### Popular Players
- LeBron James: `2544`
- Stephen Curry: `201939`
- Kevin Durant: `201142`
- Nikola Jokić: `203999`
- Giannis Antetokounmpo: `203507`
- Luka Dončić: `1629029`

### Teams
- Lakers: `1610612747`
- Warriors: `1610612744`
- Celtics: `1610612738`
- Heat: `1610612748`
- Nuggets: `1610612743`
- Bucks: `1610612749`

Use the `find_players` and `find_teams` tools to discover more IDs.

## Error Handling

The server includes comprehensive error handling. If an API call fails, you'll receive a response with:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

## Data Sources

This MCP server uses the official nba_api package, which accesses data from:
- **NBA Stats API**: Historical and statistical data
- **NBA Live API**: Real-time game data and scores

## Rate Limiting

The NBA API has rate limits. If you encounter rate limit errors, wait a few seconds between requests. The server implements basic error handling for these cases.

## Development

To modify or extend the server:

1. Edit `server.py` to add new tools or modify existing ones
2. Follow the MCP protocol for tool definitions
3. Test your changes by running the server and connecting it to Claude Desktop

## License

This MCP server is part of the nba_api project and follows the same MIT License.

## Support

For issues or questions:
- NBA API issues: https://github.com/swar/nba_api/issues
- MCP protocol: https://modelcontextprotocol.io

## Contributing

Contributions are welcome! Please follow the nba_api contribution guidelines when submitting changes.
