from typing import Optional

from pydantic import BaseModel
from deepeval.models import OllamaModel


class NoThinkOllamaModel(OllamaModel):
    """OllamaModel with qwen's "thinking" step turned off.

    With thinking on, the judge spends minutes reasoning and often returns an
    empty answer. deepeval's OllamaModel has no option to disable it, so we
    make the chat call ourselves with think=False.
    """

    def _chat_kwargs(self, prompt: str, schema: Optional[BaseModel]):
        return dict(
            model=self.name,
            messages=[{"role": "user", "content": prompt}],
            format=schema.model_json_schema() if schema else None,
            options={"temperature": self.temperature, **self.generation_kwargs},
            think=False,
        )

    def _parse(self, content: str, schema: Optional[BaseModel]):
        return (schema.model_validate_json(content) if schema else content), 0

    def generate(self, prompt: str, schema: Optional[BaseModel] = None, **kwargs):
        response = self.load_model().chat(**self._chat_kwargs(prompt, schema))
        return self._parse(response.message.content, schema)

    async def a_generate(self, prompt: str, schema: Optional[BaseModel] = None, **kwargs):
        response = await self.load_model(async_mode=True).chat(
            **self._chat_kwargs(prompt, schema)
        )
        return self._parse(response.message.content, schema)


# Judge model that scores the agent. Runs locally through Ollama.
# The 16k-context variant leaves room for the full agent trace in the judge prompt.
eval_model = NoThinkOllamaModel(
    model="qwen3.5-4b-16k",
    base_url="http://localhost:11434",
    temperature=0,
)
