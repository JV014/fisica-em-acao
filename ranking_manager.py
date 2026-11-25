import asyncio
import json
import sys
import urllib.parse
import urllib.request

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzC3lBc9BXnlNZNn-Axa9hPgeNgpcHSB5nOoOTKkxXJWA2el0DRcJSnb37QyRvhWFfMPA/exec"

IS_WEB = sys.platform in ("emscripten", "wasi")
if IS_WEB:
    import platform


class RankingManager:
    def __init__(self):
        self.player_name = ""
        self.total_players_count = 0
        self.registered_players = []
        self.rankings = {
            "campaign": [],
            "multiplayer": [],
            "target": [],
        }
        self.sync_error = ""
        self.is_syncing = False

    async def _request(self, params):
        if not GOOGLE_SCRIPT_URL or "COLE_AQUI" in GOOGLE_SCRIPT_URL:
            self.sync_error = "URL da planilha não configurada."
            return None

        query_string = urllib.parse.urlencode(params)
        full_url = f"{GOOGLE_SCRIPT_URL}?{query_string}"

        try:
            if IS_WEB:
                resp = await platform.window.fetch(full_url)
                text = await resp.text()
                return json.loads(str(text))
            else:
                req = urllib.request.Request(full_url)
                with urllib.request.urlopen(req, timeout=8) as response:
                    text = response.read().decode("utf-8")
                    return json.loads(text)
        except Exception as e:
            self.sync_error = str(e)
            print(f"Aviso de sincronização com a planilha: {e}")
            return None

    async def register_player(self, name):
        clean_name = name.strip()
        if not clean_name:
            return False

        self.player_name = clean_name
        self.is_syncing = True
        self.sync_error = ""

        data = await self._request({
            "action": "register",
            "name": clean_name,
        })

        self.is_syncing = False
        if data and data.get("status") == "ok":
            self.total_players_count = int(data.get("total_players_count", self.total_players_count))
            await self.refresh_all()
            return True
        return False

    async def submit_score(self, mode, score, difficulty="-"):
        if not self.player_name:
            return False

        self.is_syncing = True
        self.sync_error = ""

        data = await self._request({
            "action": "score",
            "mode": mode,
            "name": self.player_name,
            "score": int(score),
            "difficulty": str(difficulty),
        })

        self.is_syncing = False
        if data and data.get("status") == "ok":
            await self.refresh_all()
            return True
        return False

    async def refresh_all(self):
        self.is_syncing = True
        self.sync_error = ""

        data = await self._request({"action": "get"})

        self.is_syncing = False
        if data:
            self.total_players_count = int(data.get("total_players_count", 0))
            self.registered_players = data.get("registered_players", [])
            rankings_data = data.get("rankings", {})
            self.rankings["campaign"] = rankings_data.get("campaign", [])
            self.rankings["multiplayer"] = rankings_data.get("multiplayer", [])
            self.rankings["target"] = rankings_data.get("target", [])
            return True
        return False


ranking_manager = RankingManager()