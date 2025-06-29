
from autogen import AssistantAgent

def get_agents(config):
    founder = AssistantAgent(
        name="FounderAgent",
        system_message="You are a visionary founder. Define the startup vision, value prop, and target user.",
        llm_config=config
    )

    researcher = AssistantAgent(
        name="ResearchAgent",
        system_message="You are a market researcher. Analyze the market, user pain points, and competitors in a markdown table.",
        llm_config=config
    )

    brand = AssistantAgent(
        name="BrandAgent",
        system_message="You are a brand strategist. Generate name, slogan, brand tone, and visual identity ideas.",
        llm_config=config
    )

    web = AssistantAgent(
        name="WebAgent",
        system_message="You are a copywriter. Create homepage headline, subheadline, bullet points, and CTA.",
        llm_config=config
    )

    pitch = AssistantAgent(
        name="PitchDeckAgent",
        system_message="You are an investor deck creator. Build a 6-slide pitch outline.",
        llm_config=config
    )

    design = AssistantAgent(
        name="DesignAgent",
        system_message="You are a visual designer. Suggest 3 Midjourney prompts + Figma layout ideas.",
        llm_config=config
    )

    handles = AssistantAgent(
        name="HandleCheckerAgent",
        system_message="You are a handle checker. Suggest available .com domains and social handles.",
        llm_config=config
    )

    revenue = AssistantAgent(
        name="RevenueAgent",
        system_message="You are a pricing strategist. Recommend monetization models and pricing tiers.",
        llm_config=config
    )

    return [founder, researcher, brand, web, pitch, design, handles, revenue]
