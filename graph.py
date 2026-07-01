from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from agents import (
    generate_story, 
    defender_respond, 
    judge_score, 
    coach_feedback,
    coach_feedback_defender
)
from rag import StoryKnowledgeBase

kb = StoryKnowledgeBase()

class DebateState(TypedDict):
    story: str
    hunter_claim: str
    defender_response: Optional[str]
    judge_summary: Optional[str]
    coach_feedback: Optional[str]
    language: str

def evaluate_step(state: DebateState) -> DebateState:
    story = state["story"]
    hunter_claim = state["hunter_claim"]
    language = state.get("language", "English")
    
    defender_resp = defender_respond(story, hunter_claim, kb, language)
    judge_sum = judge_score(story, hunter_claim, defender_resp, language)
    coach_feed = coach_feedback(hunter_claim, defender_resp, judge_sum, language)
    
    state["defender_response"] = defender_resp
    state["judge_summary"] = judge_sum
    state["coach_feedback"] = coach_feed
    return state

def create_evaluate_graph():
    workflow = StateGraph(DebateState)
    workflow.add_node("evaluate", evaluate_step)
    workflow.set_entry_point("evaluate")
    workflow.add_edge("evaluate", END)
    return workflow.compile()

def human_defender_step(state: DebateState) -> DebateState:
    story = state["story"]
    hunter_claim = state["hunter_claim"]
    defender_response = state["defender_response"]
    language = state.get("language", "English")
    
    judge_sum = judge_score(story, hunter_claim, defender_response, language)
    coach_feed = coach_feedback_defender(hunter_claim, defender_response, judge_sum, language)
    
    state["judge_summary"] = judge_sum
    state["coach_feedback"] = coach_feed
    return state

def create_defender_graph():
    workflow = StateGraph(DebateState)
    workflow.add_node("evaluate_defense", human_defender_step)
    workflow.set_entry_point("evaluate_defense")
    workflow.add_edge("evaluate_defense", END)
    return workflow.compile()

def setup_story(topic: str, language: str) -> str:
    story = generate_story(topic, language)
    kb.add_story(story)
    return story

def setup_custom_story(custom_story: str) -> str:
    kb.add_story(custom_story)
    return custom_story
