import json
import sys
import urllib.request
import urllib.parse

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxc73Sv4bDlVZLlCFo_XX5WOfdaETNQHSXYyV5M67bAsnG_JiaXUsRkVRc71X9W4BTQZg/exec"

IS_WEB = (sys.platform == "emscripten")

if IS_WEB:
    import platform

class RankingManager:
    def __init__(self):
        self.url = GOOGLE_SCRIPT_URL
        self.is_syncing = False
        self.data = {
            "total_players_count": 0,
            "registered_players": [],
            "rankings": {
                "campaign": [],
                "multiplayer": [],
                "target": []
            }
        }

    async def _request(self, params):
        if not self.url or "COLE_SUA_URL" in self.url:
            return None

        query_string = urllib.parse.urlencode(params)
        full_url = f"{self.url}?{query_string}"

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
            print(f"Aviso de sincronização com a planilha: {e}")
            return None

    async def sync_from_cloud(self):
        """Busca o contador global e os rankings atualizados em tempo real."""
        self.is_syncing = True
        res = await self._request({"action": "get"})
        if res and "rankings" in res:
            self.data = res
        self.is_syncing = False

    async def register_player_access(self, player_name):
        """Envia o acesso do jogador para a aba 'Acessos' da Planilha Google."""
        clean_name = player_name.strip()
        if not clean_name:
            clean_name = "Anônimo"

        res = await self._request({
            "action": "register",
            "name": clean_name
        })
        if res and "total_players_count" in res:
            self.data["total_players_count"] = res["total_players_count"]
        return clean_name

    async def add_score(self, mode, player_name, score, difficulty=None):
        """Envia a pontuação para a aba correspondente da Planilha Google."""
        diff_val = difficulty if difficulty else "-"
        await self._request({
            "action": "score",
            "mode": mode,
            "name": player_name,
            "score": score,
            "difficulty": diff_val
        })
        await self.sync_from_cloud()

    def get_ranking(self, mode):
        return self.data["rankings"].get(mode, [])

    def get_total_players(self):
        return self.data.get("total_players_count", 0)

    def get_first_100_players(self):
        return self.data.get("registered_players", [])