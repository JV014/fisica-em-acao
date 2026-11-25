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

    # --- Métodos de leitura esperados pela interface (ranking_view.py) ---
    def get_total_players(self):
        return int(self.total_players_count)

    def get_registered_players(self):
        return list(self.registered_players)

    def get_first_100_players(self):
        return list(self.registered_players[:100])

    def get_ranking(self, mode):
        return list(self.rankings.get(mode, []))

    def get_top_ranking(self, mode):
        return list(self.rankings.get(mode, [])[:100])

    def get_player_name(self):
        return self.player_name

    # --- Comunicação com o Google Apps Script ---
    async def _web_fetch(self, url):
        js_code = f"""
        window.__py_gas_done = false;
        window.__py_gas_res = "";
        window.__py_gas_err = "";
        fetch({json.dumps(url)})
          .then(function(r) {{ return r.text(); }})
          .then(function(t) {{ window.__py_gas_res = t; window.__py_gas_done = true; }})
          .catch(function(e) {{ window.__py_gas_err = String(e); window.__py_gas_done = true; }});
        """
        platform.window.eval(js_code)

        for _ in range(200):
            await asyncio.sleep(0.05)
            if platform.window.eval("Boolean(window.__py_gas_done)"):
                err = str(platform.window.eval("String(window.__py_gas_err || '')"))
                if err:
                    raise RuntimeError(err)
                text = str(platform.window.eval("String(window.__py_gas_res || '')"))
                return json.loads(text)

        raise TimeoutError("Tempo esgotado ao conectar com a planilha.")

    async def _request(self, params):
        if not GOOGLE_SCRIPT_URL or "COLE_AQUI" in GOOGLE_SCRIPT_URL:
            self.sync_error = "URL da planilha não configurada."
            return None

        query_string = urllib.parse.urlencode(params)
        full_url = f"{GOOGLE_SCRIPT_URL}?{query_string}"

        try:
            if IS_WEB:
                return await self._web_fetch(full_url)
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

    async def register_player_access(self, name):
        return await self.register_player(name)

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

    async def record_score(self, mode, score, difficulty="-"):
        return await self.submit_score(mode, score, difficulty)

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

    async def sync_from_cloud(self):
        return await self.refresh_all()


ranking_manager = RankingManager()