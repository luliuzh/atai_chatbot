


def generate_humanized_response(question: str, answer: str) -> str:
    """
    Generates a humanized response based on the given question and answer.

    Parameters:
        question (str): The question to be answered.
        answer (str): The answer to the question.

    Returns:
        str: A detailed, full sentence response.
    """
    # Define the prompt
    prompt = f"""Generate a natural, conversational response based on the provided question and answer. If the answer seems incorrect, do not attempt to correct it; instead, create a response that aligns with the provided answer. Ensure the response is in full sentences and sounds human-like.

    Question: {question}
    Answer: {answer}

    Example responses:
    1. Question: "Who is the director of Star Wars: Episode VI - Return of the Jedi?"
       Response: "I believe the director is Richard Marquand."

    2. Question: "Who is the screenwriter of The Masked Gang: Cyprus?"
       Response: "Based on my knowledge, it is Cengiz Küçükayvaz."

    3. Question: "When was 'The Godfather' released?"
       Response: "It was released in 1972."

    Please generate a response in a similar tone and style. Do not include the question"""
    # Generate the response using GPT-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    # Extract and return the generated reply
    reply = response['choices'][0]['message']['content'].strip()
    return reply

# question = "What is the MPAA film rating of Weathering with You?"
# answer = "PG-13"
# print("Generated Reply:", generate_humanized_response(question, answer))