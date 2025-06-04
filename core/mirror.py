 # Простая реализация контекста памяти для промпта

def get_memory_context(memory_text):
    """
    Возвращает форматированный блок памяти для вставки в промпт.
    memory_text — строка с предыдущими важными фразами, выводами, фактами.
    """
    if not memory_text:
        return ""

    # Можно добавить фильтрацию, сокращение, обрезку слишком длинных блоков
    max_length = 500  # ограничение символов для памяти
    if len(memory_text) > max_length:
        memory_text = memory_text[:max_length] + "..."

    return f"Ранее было сказано:\n{memory_text.strip()}"
