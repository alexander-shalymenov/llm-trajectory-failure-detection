from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


@dataclass
class GenerationResult:
    prompt: str
    generated_response: str
    generated_tokens: list[str]
    generated_token_ids: list[int]
    output_token_count: int
    generation_time_seconds: float
    logits: np.ndarray
    hidden_states: np.ndarray


class GPT2Runner:
    def __init__(self, model_name: str = "gpt2", device: str | None = None) -> None:
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    @torch.no_grad()
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 48,
        temperature: float = 0.7,
        top_k: int | None = 50,
        do_sample: bool = True,
    ) -> GenerationResult:
        encoded = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        input_length = int(encoded["input_ids"].shape[1])

        generation_kwargs: dict[str, Any] = {
            "max_new_tokens": max_new_tokens,
            "return_dict_in_generate": True,
            "output_scores": True,
            "output_hidden_states": True,
            "pad_token_id": self.tokenizer.eos_token_id,
        }

        if do_sample:
            generation_kwargs.update(
                {
                    "do_sample": True,
                    "temperature": temperature,
                }
            )
            if top_k is not None and top_k > 0:
                generation_kwargs["top_k"] = top_k
        else:
            generation_kwargs["do_sample"] = False

        start_time = time.perf_counter()
        output = self.model.generate(**encoded, **generation_kwargs)
        generation_time = time.perf_counter() - start_time

        sequence = output.sequences[0]
        generated_ids = sequence[input_length:]
        generated_token_ids = [int(token_id) for token_id in generated_ids.detach().cpu().tolist()]
        generated_tokens = self.tokenizer.convert_ids_to_tokens(generated_token_ids)
        generated_response = self.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

        logits = self._scores_to_logits(output.scores)
        hidden_states = self._extract_last_layer_generated_hidden_states(output.hidden_states)

        return GenerationResult(
            prompt=prompt,
            generated_response=generated_response,
            generated_tokens=generated_tokens,
            generated_token_ids=generated_token_ids,
            output_token_count=len(generated_token_ids),
            generation_time_seconds=float(generation_time),
            logits=logits,
            hidden_states=hidden_states,
        )

    @staticmethod
    def _scores_to_logits(scores: tuple[torch.Tensor, ...] | None) -> np.ndarray:
        if not scores:
            return np.empty((0, 0), dtype=np.float32)
        return torch.stack([score[0].detach().cpu() for score in scores], dim=0).numpy()

    @staticmethod
    def _extract_last_layer_generated_hidden_states(
        hidden_states_by_step: tuple[tuple[torch.Tensor, ...], ...] | None,
    ) -> np.ndarray:
        if not hidden_states_by_step:
            return np.empty((0, 0), dtype=np.float32)

        generated_last_layer_states = []
        for step_hidden_states in hidden_states_by_step:
            last_layer = step_hidden_states[-1][0, -1, :].detach().cpu().numpy()
            generated_last_layer_states.append(last_layer)

        return np.stack(generated_last_layer_states, axis=0).astype(np.float32)
