"""Build standard prompts for the small multiple-choice benchmark."""

from __future__ import annotations


CHOICE_LABELS = ("A", "B", "C", "D")


def validate_question_item(question_item: dict) -> None:
    """
    Soru nesnesinin prompt üretimi için gerekli alanlara sahip olup olmadığını kontrol eder.
    Eksik veya hatalı alan varsa ValueError üretir.
    """
    if not isinstance(question_item, dict):
        raise ValueError("Soru nesnesi dict formatında olmalıdır.")

    required_fields = ("id", "question", "choices")
    for field in required_fields:
        if field not in question_item:
            raise ValueError(f"Soru nesnesinde '{field}' alanı eksik.")

    question_text = question_item["question"]
    if not isinstance(question_text, str) or not question_text.strip():
        raise ValueError("'question' alanı boş olmayan bir string olmalıdır.")

    choices = question_item["choices"]
    if not isinstance(choices, dict):
        raise ValueError("'choices' alanı dict formatında olmalıdır.")

    if set(choices.keys()) != set(CHOICE_LABELS):
        raise ValueError("choices alanında A, B, C ve D seçenekleri bulunmalıdır.")

    for label in CHOICE_LABELS:
        choice_text = choices[label]
        if not isinstance(choice_text, str) or not choice_text.strip():
            raise ValueError(f"'{label}' seçeneği boş olmayan bir string olmalıdır.")


def build_prompt(question_item: dict) -> str:
    """
    Tek bir çoktan seçmeli soru nesnesini LLM'e verilecek standart prompt metnine dönüştürür.
    Modelden yalnızca A, B, C veya D seçenek harflerinden biriyle cevap vermesi istenir.
    """
    validate_question_item(question_item)

    choices = question_item["choices"]
    prompt_lines = [
        "Aşağıdaki çoktan seçmeli soruyu cevapla.",
        "",
        "Soru:",
        question_item["question"].strip(),
        "",
        "Seçenekler:",
        f"A) {choices['A'].strip()}",
        f"B) {choices['B'].strip()}",
        f"C) {choices['C'].strip()}",
        f"D) {choices['D'].strip()}",
        "",
        "Yanıtını yalnızca A, B, C veya D harflerinden biri olarak ver.",
    ]

    return "\n".join(prompt_lines)


def build_prompts(question_items: list[dict]) -> list[dict]:
    """
    Birden fazla soru nesnesi için prompt üretir.
    Her çıktı id ve prompt alanlarını içerir.
    """
    if not isinstance(question_items, list):
        raise ValueError("question_items list formatında olmalıdır.")

    prompts = []
    for question_item in question_items:
        validate_question_item(question_item)
        prompts.append(
            {
                "id": question_item["id"],
                "prompt": build_prompt(question_item),
            }
        )

    return prompts


if __name__ == "__main__":
    sample_question = {
        "id": "q001",
        "question": "Türkiye'nin başkenti neresidir?",
        "choices": {
            "A": "İstanbul",
            "B": "Ankara",
            "C": "İzmir",
            "D": "Bursa",
        },
        "answer": "B",
        "category": "genel_bilgi",
        "difficulty": "easy",
    }

    print(build_prompt(sample_question))
