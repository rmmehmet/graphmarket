import json
import re
import shutil
import subprocess

from app.agents.providers.base import ModelProvider


class ClaudeSubscriptionProvider(ModelProvider):
    """Claude Code CLI'nin abonelik kimlik doğrulamasını kullanır (claude login) — ayrı bir
    API anahtarı gerektirmez. `-p/--print` tek seferlik çıktı modunu, `--restricted` ile
    (Bash/PowerShell gibi komut çalıştıran araçlar kapalı) çağırır — ajan düğümleri bu
    sağlayıcıyı yalnızca metin tamamlama için kullanır, dosya/komut erişimi vermez.
    """

    def _claude_path(self) -> str:
        claude_path = shutil.which("claude")
        if claude_path is None:
            raise RuntimeError("claude CLI bulunamadı (PATH'te değil)")
        return claude_path

    def test_connection(self) -> None:
        claude_path = self._claude_path()
        result = subprocess.run([claude_path, "--version"], capture_output=True, timeout=10)
        if result.returncode != 0:
            raise RuntimeError("claude CLI çalıştırılamadı")

    def complete(self, prompt: str) -> str:
        claude_path = self._claude_path()
        args = [claude_path, "-p", "--restricted", "--output-format", "text"]
        if self.model_name:
            args += ["--model", self.model_name]
        # prompt is piped via stdin, not passed as a CLI arg — long/unicode-heavy
        # prompts get corrupted through the Windows .cmd shim's argument quoting.
        result = subprocess.run(
            args, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=120
        )
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI hatası: {result.stderr.strip()}")
        return result.stdout.strip()

    def search(self, query: str) -> dict:
        """Claude Code'un WebSearch aracıyla gerçek zamanlı web araması yapar (abonelik
        kimlik doğrulaması, ayrı bir arama API anahtarı gerekmez). `--restricted` WebFetch/Bash'i
        kapatır ama WebSearch'ü kapatmaz; yine de izin istemeden çalışması için burada açıkça
        `--allowedTools WebSearch` ile ön onaylanıyor.
        """
        claude_path = self._claude_path()
        args = [
            claude_path,
            "-p",
            "--restricted",
            "--allowedTools",
            "WebSearch",
            "--output-format",
            "text",
        ]
        if self.model_name:
            args += ["--model", self.model_name]
        prompt = (
            "Aşağıdaki sorgu için web'de gerçek zamanlı arama yap ve bulduklarını özetle. "
            "SADECE şu JSON formatında yanıt ver: "
            '{"summary": "2-4 cümlelik özet", "sources": [{"title": "...", "url": "..."}]}'
            f"\n\nSorgu: {query}"
        )
        result = subprocess.run(
            args, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=120
        )
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI hatası: {result.stderr.strip()}")

        match = re.search(r"\{.*\}", result.stdout, re.DOTALL)
        if not match:
            raise ValueError("arama yanıtında JSON nesnesi bulunamadı")
        return json.loads(match.group(0))
