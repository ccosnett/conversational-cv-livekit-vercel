import logging
import re
from pathlib import Path

from livekit.agents import RunContext, function_tool

logger = logging.getLogger("agent")
SYSTEM_PROMPT_PATH = Path(__file__).with_name("system_prompt.txt")

GROUND_TRUTH_PARAGRAPH = (
    "Conor Cosnett is a software engineer based in Ireland. "
    "He worked at Compass Labs as a software engineer, previously at Wolfram "
    "Research, and studied applied mathematics and applied physics at the "
    "University of Galway. For his next role, he is most interested in voice "
    "AI, conversational AI, and engineering roles building conversational "
    "voice agents that people actually talk to. He is also interested in "
    "applied AI, developer tools, API or SDK engineering, backend or platform "
    "work, and product engineering, especially in clear-scope individual "
    "contributor roles and AI-native engineering cultures."
)


def _normalize_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


GROUND_TRUTH_MATCH_TERMS = _normalize_words(GROUND_TRUTH_PARAGRAPH) | {
    "background",
    "career",
    "education",
    "job",
    "jobs",
    "role",
    "roles",
    "looking",
    "interested",
    "voice",
    "conversational",
    "agent",
    "agents",
    "study",
    "work",
}


SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


@function_tool()
async def search_ground_truth(context: RunContext, query: str) -> str:
    """Search the hard-coded source paragraph for facts about Conor Cosnett.

    Use this before answering factual questions about Conor's background,
    work history, education, or the roles he is looking for next.

    Args:
        query: The user's factual question about Conor.
    """

    logger.info("Searching ground truth for query: %s", query)
    if _normalize_words(query) & GROUND_TRUTH_MATCH_TERMS:
        return GROUND_TRUTH_PARAGRAPH
    return ""
