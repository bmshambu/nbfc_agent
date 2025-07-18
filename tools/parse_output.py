import ast
import json

def safe_parse_llm_suggestions(response):
    try:
        # Handle if response is a list with one big string (like your example)
        if isinstance(response, list) and len(response) == 1:
            raw_string = response[0]

            # Remove unnecessary whitespace
            raw_string = raw_string.strip()

            # 1. Try JSON first (safe if double quotes in list)
            try:
                return json.loads(raw_string)
            except json.JSONDecodeError:
                pass

            # 2. Fallback: Python literal parser
            return ast.literal_eval(raw_string)

        # Already a parsed list
        elif isinstance(response, list):
            return response

        # Fallback: return empty
        return []
    except Exception as e:
        print("Error parsing suggestions:", e)
        return []
