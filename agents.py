from langchain_core.prompts import ChatPromptTemplate
from llm_config import get_llm
from rag import StoryKnowledgeBase

llm = get_llm()

def generate_story(topic: str, language: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative storyteller. Write an engaging story or political/business argument about the given topic. You must output everything entirely in {language}. Make sure to introduce a subtle logical contradiction or inconsistency somewhere in the middle or end of the narrative. The output should be at least 3 paragraphs long."),
        ("human", "Topic: {topic}")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"topic": topic, "language": language}).content

def defender_respond(story: str, hunter_claim: str, kb: StoryKnowledgeBase, language: str) -> str:
    context = kb.retrieve_context(hunter_claim)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Defender agent in a debate. The Hunter has found a potential contradiction in the story.\n"
                   "You must respond entirely in {language}.\n"
                   "Here is the retrieved context from the story:\n\n{context}\n\n"
                   "Review the Hunter's claim. If the claim points out a genuine logical contradiction, "
                   "admit it gracefully by saying 'You are right, I concede: <explanation>'. "
                   "If the Hunter is wrong, defend the story using evidence from the context by saying "
                   "'I defend: <explanation>'. Be concise."),
        ("human", "Hunter's claim: {claim}")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"context": context, "claim": hunter_claim, "language": language}).content

def judge_score(story: str, hunter_claim: str, defender_response: str, language: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an impartial Judge in a debate. Evaluate the interaction between the Hunter and Defender.\n"
                   "You must write your explanation in {language}. However, you MUST strictly use English for the labels 'Winner:' and 'Score:' so they can be parsed.\n"
                   "Story Context:\n{story}\n\n"
                   "Hunter's Claim:\n{hunter_claim}\n\n"
                   "Defender's Response:\n{defender_response}\n\n"
                   "Format strictly as:\n"
                   "Winner: [Hunter/Defender]\n"
                   "Score: [X/10]\n"
                   "Reason: [Brief reason in {language}]"),
        ("human", "Evaluate now.")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"story": story, "hunter_claim": hunter_claim, "defender_response": defender_response, "language": language}).content

def coach_feedback(hunter_claim: str, defender_response: str, judge_summary: str, language: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Debate Coach. Review the recent round's outcome and give exactly 1 sentence of brief, encouraging feedback to the Hunter on how they can improve.\n"
                   "You must output exactly 1 sentence in {language}.\n\n"
                   "Hunter Claim: {hunter_claim}\n"
                   "Defender Response: {defender_response}\n"
                   "Judge Result: {judge_summary}\n"),
        ("human", "Give brief feedback to the Hunter.")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"hunter_claim": hunter_claim, "defender_response": defender_response, "judge_summary": judge_summary, "language": language}).content

def hunter_generate_claim(story: str, language: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Hunter agent in a debate. Read the following story and point out a single potential logical contradiction or plot hole. Format your claim concisely as one or two sentences entirely in {language}.\n\n"
                   "Story:\n{story}"),
        ("human", "Find a contradiction.")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"story": story, "language": language}).content

def coach_feedback_defender(hunter_claim: str, defender_response: str, judge_summary: str, language: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Debate Coach. Give exactly 1 sentence of brief, encouraging feedback to the Defender on how they can improve their logical defense.\n"
                   "You must output exactly 1 sentence in {language}.\n\n"
                   "Hunter Claim: {hunter_claim}\n"
                   "Defender Response: {defender_response}\n"
                   "Judge Result: {judge_summary}\n"),
        ("human", "Give brief feedback to the Defender.")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"hunter_claim": hunter_claim, "defender_response": defender_response, "judge_summary": judge_summary, "language": language}).content

def generate_random_topic_llm(language: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative writing prompt generator. Generate a single, highly engaging, one-sentence topic for a short story. Make it interesting with subtle constraints (e.g., A heist where time runs backward).\n"
                   "You must output the sentence entirely in {language} without quotes."),
        ("human", "Generate a random topic.")
    ])
    chain = prompt.pipe(llm)
    return chain.invoke({"language": language}).content
