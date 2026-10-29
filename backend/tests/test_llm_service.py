from types import SimpleNamespace

from app.generation.llm_service import LLMService


def test_generate_answer_passes_context_to_prompt_chain():
    service = LLMService.__new__(LLMService)

    captured = {}

    class FakeChain:
        def invoke(self, values):
            captured.update(values)
            return "jawaban contoh"

    service._get_chain_for_mode = lambda mode: FakeChain()

    result = service.generate_answer("Apa itu subnet?", "Konteks subnet")

    assert result == "jawaban contoh"
    assert captured == {"query": "Apa itu subnet?", "retrieved_context": "Konteks subnet"}


def test_fast_and_thinking_modes_use_different_prompt_instructions():
    service = LLMService()

    fast_prompt = service._build_prompt_for_mode("cepat")
    thinking_prompt = service._build_prompt_for_mode("berpikir")

    assert "singkat" in fast_prompt[0][1].lower()
    assert "ringkas" in fast_prompt[0][1].lower()
    assert "tabel" in thinking_prompt[0][1].lower()
    assert "detail" in thinking_prompt[0][1].lower()
