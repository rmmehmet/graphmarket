import shutil
import subprocess

from app.agents.providers.base import ModelProvider


class ClaudeSubscriptionProvider(ModelProvider):
    """Claude Code / Claude Agent SDK abonelik kimlik doğrulamasını kullanır (claude login) —
    ayrı bir API anahtarı gerektirmez. Bağlantı testi yerel `claude` CLI'nin PATH'te ve
    çalışır durumda olup olmadığını kontrol eder; gerçek tamamlama Faz 6+'ta LangGraph
    ajan katmanına Claude Agent SDK entegre edildiğinde eklenecek.
    """

    def test_connection(self) -> None:
        claude_path = shutil.which("claude")
        if claude_path is None:
            raise RuntimeError("claude CLI bulunamadı (PATH'te değil)")
        result = subprocess.run([claude_path, "--version"], capture_output=True, timeout=10)
        if result.returncode != 0:
            raise RuntimeError("claude CLI çalıştırılamadı")

    def complete(self, prompt: str) -> str:
        raise NotImplementedError(
            "Claude Agent SDK entegrasyonu ajan katmanı fazında (Faz 6+) eklenecek"
        )
