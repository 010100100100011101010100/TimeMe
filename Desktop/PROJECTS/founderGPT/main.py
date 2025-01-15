import csv
import os
from groq import Groq
from typing import Tuple, List

class PersonalityGroqBot:
    def __init__(self, api_key: str, training_data: str, personality_traits: dict):
        self.client = Groq(api_key=api_key)
        self.context = training_data
        self.personality = personality_traits
        self.conversation_history = []

    def generate_personality_prompt(self) -> str:
        traits = []
        for trait, value in self.personality.items():
            traits.append(f"- {trait}: {value}")
        return "\n".join(traits)

    def chat(self, user_input: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant with the following personality traits:

{self.generate_personality_prompt()}

You have been trained on the following content:

{self.context}

Maintain these personality traits in all your responses while providing accurate information.
If a question cannot be answered using the provided context, politely indicate that you
don't have that information while staying in character."""
            },
            *self.conversation_history
        ]

        completion = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        response = completion.choices[0].message.content

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

def split_csv(file_path: str, chunk_size: int) -> List[str]:
    """Split a large CSV into smaller parts."""
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Get headers
        chunks = []
        current_chunk = []

        for i, row in enumerate(reader, 1):
            current_chunk.append(row)
            if i % chunk_size == 0:
                chunks.append(current_chunk)
                current_chunk = []
        if current_chunk:  # Add remaining rows
            chunks.append(current_chunk)

    # Save smaller chunks to new files
    output_files = []
    for idx, chunk in enumerate(chunks):
        chunk_file = f"{file_path.rsplit('.', 1)[0]}_part{idx + 1}.csv"
        with open(chunk_file, 'w', newline='') as chunk_file_handle:
            writer = csv.writer(chunk_file_handle)
            writer.writerow(headers)
            writer.writerows(chunk)
        output_files.append(chunk_file)
    
    return output_files

def load_data_from_csv(file_paths: List[str]) -> Tuple[str, dict]:
    """Load data from multiple CSV files and merge into training data and personality traits."""
    training_data = ""
    personality_traits = {}

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                training_data += (
                    f"Name: {row.get('Name', 'N/A')}\n"
                    f"Category: {row.get('Category', 'N/A')}\n"
                    f"Summary: {row.get('Summary', 'N/A')}\n"
                    f"Description: {row.get('Description', 'N/A')}\n\n"
                )
                personality_traits.update({
                    "Leadership": row.get("Leadership", "N/A"),
                    "PMF": row.get("PMF", "N/A"),
                    "Growth": row.get("Growth", "N/A"),
                })
    
    return training_data, personality_traits

# Example usage
if __name__ == "__main__":
    api_key = "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"
    csv_file_path = "./Data/split_part_1.csv"
    chunk_size = 100  # Number of rows per smaller CSV

    # Split large CSV into smaller parts
    smaller_csv_files = split_csv(csv_file_path, chunk_size)

    # Load data from smaller CSV files
    training_data, personality_traits = load_data_from_csv(smaller_csv_files)

    static_traits = {
        "Communication Style": "Focussed for founders",
        "Tone": "Professional and mentor type tone",
        "Knowledge Level": "Expert in helping founders and solving their doubts",
        "Empathy Level": "Medium tolerance level",
        "Response Style": "Concise but thorough, includes examples and references"
    }

    # Initialize chatbot
    bot = PersonalityGroqBot(api_key, training_data, static_traits)

    # Chat loop
    print("Chatbot initialized. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        response = bot.chat(user_input)
        print(f"Bot: {response}")
