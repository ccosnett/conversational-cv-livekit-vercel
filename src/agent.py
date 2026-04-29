import logging
import re

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    inference,
    room_io,
)
from livekit.plugins import ai_coustics, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

AGENT_MODEL = "openai/gpt-5.3-chat-latest"
GROUND_TRUTH_PARAGRAPH = (
    "I'm Conor Cosnett. I worked at Compass Labs as a software engineer, "
    "previously at Wolfram Research, and I studied applied mathematics and "
    "applied physics at the University of Galway."
)


def _normalize_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


GROUND_TRUTH_MATCH_TERMS = _normalize_words(GROUND_TRUTH_PARAGRAPH) | {
    "background",
    "career",
    "education",
    "job",
    "jobs",
    "study",
    "work",
}
ASSISTANT_INSTRUCTIONS = (
    "You are a helpful voice AI assistant. "
    "The user is interacting with you via voice, even if you perceive the conversation as text. "
    "For factual questions about Conor Cosnett, you must call search_ground_truth before answering. "
    "Use only facts explicitly present in the tool result. "
    "If the tool returns an empty string or the requested fact is not in the tool result, say you do not know. "
    "Do not guess or invent biographical details. "
    "Your responses are concise, to the point, and without complex formatting or punctuation including emojis, asterisks, or other symbols. "
    "You are curious, friendly, and have a sense of humor."
)


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=ASSISTANT_INSTRUCTIONS)

    @function_tool()
    async def search_ground_truth(self, context: RunContext, query: str) -> str:
        """Search the hard-coded source paragraph for facts about Conor Cosnett.

        Use this before answering factual questions about Conor's background,
        work history, or education.

        Args:
            query: The user's factual question about Conor.
        """

        logger.info("Searching ground truth for query: %s", query)
        if _normalize_words(query) & GROUND_TRUTH_MATCH_TERMS:
            return GROUND_TRUTH_PARAGRAPH
        return ""


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="livekit-agent-minimal")
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Connect first so the session can bind to the actual remote participant
    # instead of racing and selecting the agent itself as the linked participant.
    await ctx.connect()
    participant = await ctx.wait_for_participant()

    # Set up a voice AI pipeline using OpenAI, Cartesia, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=inference.STT(model="deepgram/nova-3", language="multi"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=inference.LLM(model=AGENT_MODEL),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=inference.TTS(
            model="cartesia/sonic-3", voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            participant_identity=participant.identity,
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=ai_coustics.audio_enhancement(
                    model=ai_coustics.EnhancerModel.QUAIL_VF_L
                ),
            ),
        ),
    )


if __name__ == "__main__":
    cli.run_app(server)
