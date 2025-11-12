#!/usr/bin/env python3
"""
NBA API MCP Server

This MCP server provides tools to access NBA statistics, player information,
team data, and live game scores through the nba_api package.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add the parent directory's src to the path for local development
parent_dir = Path(__file__).parent.parent
src_dir = parent_dir / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

# MCP SDK imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# NBA API imports
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    playercareerstats,
    commonplayerinfo,
    commonteamroster,
    playergamelog,
    leagueleaders,
    teamgamelog,
    leaguedashteamstats,
    leaguedashplayerstats,
)
from nba_api.live.nba.endpoints import scoreboard, boxscore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nba-mcp-server")

# Create server instance
app = Server("nba-api")


def safe_api_call(func, *args, **kwargs) -> dict[str, Any]:
    """
    Safely execute an NBA API call and return the result.

    Args:
        func: The API function to call
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Dictionary with either the data or an error message
    """
    try:
        result = func(*args, **kwargs)
        return {"success": True, "data": result.get_dict()}
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return {"success": False, "error": str(e)}


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available NBA API tools.

    Returns:
        List of Tool objects describing available NBA API operations
    """
    return [
        Tool(
            name="find_players",
            description="Search for NBA players by name. Supports partial matches and returns player ID, name, and active status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Player name or partial name to search for (e.g., 'LeBron', 'Curry', 'Jokic')"
                    },
                    "active_only": {
                        "type": "boolean",
                        "description": "If true, only return currently active players",
                        "default": False
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_player_info",
            description="Get detailed information about a specific player including personal details, draft info, and career summary.",
            inputSchema={
                "type": "object",
                "properties": {
                    "player_id": {
                        "type": "string",
                        "description": "The NBA player ID (e.g., '2544' for LeBron James)"
                    }
                },
                "required": ["player_id"]
            }
        ),
        Tool(
            name="get_player_career_stats",
            description="Get complete career statistics for a player including regular season, playoffs, and all-star games.",
            inputSchema={
                "type": "object",
                "properties": {
                    "player_id": {
                        "type": "string",
                        "description": "The NBA player ID"
                    },
                    "per_mode": {
                        "type": "string",
                        "description": "Statistics mode: 'Totals', 'PerGame', or 'Per36'",
                        "enum": ["Totals", "PerGame", "Per36"],
                        "default": "PerGame"
                    }
                },
                "required": ["player_id"]
            }
        ),
        Tool(
            name="get_player_game_log",
            description="Get recent game-by-game statistics for a player in a specific season.",
            inputSchema={
                "type": "object",
                "properties": {
                    "player_id": {
                        "type": "string",
                        "description": "The NBA player ID"
                    },
                    "season": {
                        "type": "string",
                        "description": "Season in format 'YYYY-YY' (e.g., '2024-25')",
                        "default": "2024-25"
                    },
                    "season_type": {
                        "type": "string",
                        "description": "Type of season: 'Regular Season' or 'Playoffs'",
                        "enum": ["Regular Season", "Playoffs"],
                        "default": "Regular Season"
                    }
                },
                "required": ["player_id"]
            }
        ),
        Tool(
            name="find_teams",
            description="Search for NBA teams by name, city, state, or nickname.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Team name, city, state, or nickname to search for (e.g., 'Lakers', 'Boston', 'Warriors')"
                    },
                    "search_by": {
                        "type": "string",
                        "description": "Field to search in: 'name', 'city', 'state', or 'nickname'",
                        "enum": ["name", "city", "state", "nickname"],
                        "default": "name"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_team_roster",
            description="Get the current roster for a specific NBA team.",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_id": {
                        "type": "string",
                        "description": "The NBA team ID (e.g., '1610612747' for Lakers)"
                    },
                    "season": {
                        "type": "string",
                        "description": "Season in format 'YYYY-YY' (e.g., '2024-25')",
                        "default": "2024-25"
                    }
                },
                "required": ["team_id"]
            }
        ),
        Tool(
            name="get_team_game_log",
            description="Get recent game results and statistics for a team.",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_id": {
                        "type": "string",
                        "description": "The NBA team ID"
                    },
                    "season": {
                        "type": "string",
                        "description": "Season in format 'YYYY-YY' (e.g., '2024-25')",
                        "default": "2024-25"
                    },
                    "season_type": {
                        "type": "string",
                        "description": "Type of season: 'Regular Season' or 'Playoffs'",
                        "enum": ["Regular Season", "Playoffs"],
                        "default": "Regular Season"
                    }
                },
                "required": ["team_id"]
            }
        ),
        Tool(
            name="get_todays_scoreboard",
            description="Get live scores and status for all NBA games today.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_game_boxscore",
            description="Get detailed boxscore statistics for a specific game.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game_id": {
                        "type": "string",
                        "description": "The NBA game ID (e.g., '0022400001')"
                    }
                },
                "required": ["game_id"]
            }
        ),
        Tool(
            name="get_league_leaders",
            description="Get league leaders for various statistical categories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "stat_category": {
                        "type": "string",
                        "description": "Statistical category to get leaders for",
                        "enum": ["PTS", "REB", "AST", "FG_PCT", "FG3_PCT", "FT_PCT", "STL", "BLK"],
                        "default": "PTS"
                    },
                    "season": {
                        "type": "string",
                        "description": "Season in format 'YYYY-YY' (e.g., '2024-25')",
                        "default": "2024-25"
                    },
                    "season_type": {
                        "type": "string",
                        "description": "Type of season: 'Regular Season' or 'Playoffs'",
                        "enum": ["Regular Season", "Playoffs"],
                        "default": "Regular Season"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_team_stats",
            description="Get current season statistics for all NBA teams.",
            inputSchema={
                "type": "object",
                "properties": {
                    "season": {
                        "type": "string",
                        "description": "Season in format 'YYYY-YY' (e.g., '2024-25')",
                        "default": "2024-25"
                    },
                    "season_type": {
                        "type": "string",
                        "description": "Type of season: 'Regular Season' or 'Playoffs'",
                        "enum": ["Regular Season", "Playoffs"],
                        "default": "Regular Season"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="get_player_stats",
            description="Get current season statistics for all NBA players.",
            inputSchema={
                "type": "object",
                "properties": {
                    "season": {
                        "type": "string",
                        "description": "Season in format 'YYYY-YY' (e.g., '2024-25')",
                        "default": "2024-25"
                    },
                    "season_type": {
                        "type": "string",
                        "description": "Type of season: 'Regular Season' or 'Playoffs'",
                        "enum": ["Regular Season", "Playoffs"],
                        "default": "Regular Season"
                    },
                    "per_mode": {
                        "type": "string",
                        "description": "Statistics mode: 'Totals', 'PerGame', or 'Per36'",
                        "enum": ["Totals", "PerGame", "Per36"],
                        "default": "PerGame"
                    }
                },
                "required": []
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool execution requests.

    Args:
        name: Name of the tool to execute
        arguments: Dictionary of arguments for the tool

    Returns:
        List containing a TextContent with the result
    """
    try:
        if name == "find_players":
            player_name = arguments["name"]
            active_only = arguments.get("active_only", False)

            # Search for players
            found_players = players.find_players_by_full_name(player_name)

            if active_only:
                found_players = [p for p in found_players if p["is_active"]]

            result = {
                "query": player_name,
                "active_only": active_only,
                "count": len(found_players),
                "players": found_players
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_player_info":
            player_id = arguments["player_id"]
            result = safe_api_call(commonplayerinfo.CommonPlayerInfo, player_id=player_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_player_career_stats":
            player_id = arguments["player_id"]
            per_mode = arguments.get("per_mode", "PerGame")
            result = safe_api_call(
                playercareerstats.PlayerCareerStats,
                player_id=player_id,
                per_mode36=per_mode
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_player_game_log":
            player_id = arguments["player_id"]
            season = arguments.get("season", "2024-25")
            season_type = arguments.get("season_type", "Regular Season")
            result = safe_api_call(
                playergamelog.PlayerGameLog,
                player_id=player_id,
                season=season,
                season_type_all_star=season_type
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "find_teams":
            query = arguments["query"]
            search_by = arguments.get("search_by", "name")

            if search_by == "name":
                found_teams = teams.find_teams_by_full_name(query)
            elif search_by == "city":
                found_teams = teams.find_teams_by_city(query)
            elif search_by == "state":
                found_teams = teams.find_teams_by_state(query)
            elif search_by == "nickname":
                found_teams = teams.find_teams_by_nickname(query)
            else:
                found_teams = []

            result = {
                "query": query,
                "search_by": search_by,
                "count": len(found_teams),
                "teams": found_teams
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_team_roster":
            team_id = arguments["team_id"]
            season = arguments.get("season", "2024-25")
            result = safe_api_call(
                commonteamroster.CommonTeamRoster,
                team_id=team_id,
                season=season
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_team_game_log":
            team_id = arguments["team_id"]
            season = arguments.get("season", "2024-25")
            season_type = arguments.get("season_type", "Regular Season")
            result = safe_api_call(
                teamgamelog.TeamGameLog,
                team_id=team_id,
                season=season,
                season_type_all_star=season_type
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_todays_scoreboard":
            result = safe_api_call(scoreboard.ScoreBoard)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_game_boxscore":
            game_id = arguments["game_id"]
            result = safe_api_call(boxscore.BoxScore, game_id=game_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_league_leaders":
            stat_category = arguments.get("stat_category", "PTS")
            season = arguments.get("season", "2024-25")
            season_type = arguments.get("season_type", "Regular Season")
            result = safe_api_call(
                leagueleaders.LeagueLeaders,
                stat_category_abbreviation=stat_category,
                season=season,
                season_type_all_star=season_type
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_team_stats":
            season = arguments.get("season", "2024-25")
            season_type = arguments.get("season_type", "Regular Season")
            result = safe_api_call(
                leaguedashteamstats.LeagueDashTeamStats,
                season=season,
                season_type_all_star=season_type
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_player_stats":
            season = arguments.get("season", "2024-25")
            season_type = arguments.get("season_type", "Regular Season")
            per_mode = arguments.get("per_mode", "PerGame")
            result = safe_api_call(
                leaguedashplayerstats.LeagueDashPlayerStats,
                season=season,
                season_type_all_star=season_type,
                per_mode_detailed=per_mode
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        error_result = {
            "error": str(e),
            "tool": name,
            "arguments": arguments
        }
        return [TextContent(type="text", text=json.dumps(error_result, indent=2))]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        logger.info("NBA API MCP Server starting...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
