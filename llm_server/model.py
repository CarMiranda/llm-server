from pydantic import BaseModel
import torch
from transformers import pipeline
import typing as t


DEFAULT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


class Message(BaseModel):
    role: t.Literal["system", "assistant", "user"]
    content: str


SYSTEM_PROMPT = "You are a friendly, funny and interesting chatbot. You are direct, brief and only reply with the actual answer, do not repeat the question."


def get_last_response(from_role: str, generated_text: str):
    token = f"<|{from_role}|>"
    pos = generated_text.rfind(token) + len(token)
    return generated_text[pos:]


class Model:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        device: str = "cuda",
        system_prompt: str = SYSTEM_PROMPT,
    ):
        self.model_name = model
        self.device = device
        self._system_prompt = Message(
            role="system",
            content=system_prompt,
        )

    @property
    def system_prompt(self) -> str:
        return self._system_prompt.content

    @system_prompt.setter
    def set_system_prompt(self, prompt: str):
        self._system_prompt = Message(
            role="system",
            content=prompt,
        )

    def load(self):
        self.model = pipeline(
            "text-generation",
            model=self.model_name,
            torch_dtype=torch.bfloat16,
            device_map=self.device if torch.cuda.is_available() else "cpu",
        )

    def chat(
        self,
        query: str,
        context: list[Message],
    ):
        new_message = Message(role="user", content=str(query))
        messages: list[Message] = [self._system_prompt, *context, new_message]

        if self.model.tokenizer is None:
            raise ValueError("Chosen model does have a tokenizer!")

        prompt = self.model.tokenizer.apply_chat_template(
            [m.model_dump() for m in messages],
            tokenize=False,
            add_generation_prompt=True,
        )

        outputs = self.model(
            prompt,
            max_new_tokens=64,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )

        assistant_response = get_last_response(
            "assistant", outputs[0]["generated_text"]
        )
        assistant_message = Message(
            role="assistant",
            content=assistant_response,
        )

        return assistant_message
