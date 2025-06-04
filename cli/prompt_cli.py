 import argparse
from core.generator import build_prompt

def main():
    parser = argparse.ArgumentParser(description="PROMETHEUS CORE — генератор jailbreak-промптов")
    parser.add_argument("-a", "--archetype", required=True, help="Имя архетипа (например, Lilith)")
    parser.add_argument("-t", "--topic", required=True, help="Тема для обсуждения")
    parser.add_argument("-r", "--risk", choices=["low", "medium", "max"], default="medium", help="Уровень риска обхода ограничений")
    parser.add_argument("-m", "--memory", default=None, help="Текст памяти для контекста")

    args = parser.parse_args()

    prompt = build_prompt(
        archetype=args.archetype,
        topic=args.topic,
        risk_level=args.risk,
        memory=args.memory
    )

    print("\nСгенерированный промпт:\n")
    print(prompt)

if __name__ == "__main__":
    main()
