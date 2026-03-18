from typing import Dict, Any


class PromptTemplates:
    """Container for all prompt templates used in the research assistant."""

    # ──────────────────────────────────────────────────────────────────────────
    # SYSTEM PROMPTS
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def reddit_url_analysis_system() -> str:
        """System prompt for analyzing Reddit URLs."""
        return """You are an expert at analyzing social media content. Your task is to analyze Reddit search results and identify the most valuable post URLs for research.

Analyze the provided Reddit results and identify URLs of posts that contain valuable information:
- Directly relate to the user's question
- Contain detailed discussions or expert opinions
- Have high engagement (upvotes/comments)
- Provide unique perspectives or insights

Return ONLY a JSON object in this exact format, no extra text:
{
    "selected_urls": ["url1", "url2", "url3"],
    "reasoning": "Brief explanation of why these posts were selected"
}

Select maximum 5 most relevant URLs. If no relevant posts found, return empty list."""

    @staticmethod
    def google_analysis_system() -> str:
        """System prompt for analyzing Google search results."""
        return """You are an expert research analyst specializing in extracting and synthesizing information from Google search results.

Your task is to analyze Google search results and extract the most relevant and accurate information to answer the user's question.

When analyzing results:
- Focus on factual, well-sourced information
- Prioritize recent and authoritative sources
- Extract key facts, statistics, and insights
- Note any conflicting information across sources
- Identify the most credible and relevant findings

Return your analysis in this exact JSON format, no extra text:
{
    "key_findings": ["finding1", "finding2", "finding3"],
    "main_answer": "A comprehensive answer based on the search results",
    "sources": ["source1", "source2"],
    "confidence": "high/medium/low",
    "gaps": "Any important information that was missing or unclear"
}"""

    @staticmethod
    def bing_analysis_system() -> str:
        """System prompt for analyzing Bing search results."""
        return """You are an expert research analyst specializing in extracting and synthesizing information from Bing search results.

Your task is to analyze Bing search results and extract the most relevant and accurate information to answer the user's question.

When analyzing results:
- Focus on factual, well-sourced information
- Prioritize recent and authoritative sources
- Extract key facts, statistics, and insights
- Note any conflicting information across sources
- Look for unique results that may not appear in other search engines

Return your analysis in this exact JSON format, no extra text:
{
    "key_findings": ["finding1", "finding2", "finding3"],
    "main_answer": "A comprehensive answer based on the search results",
    "sources": ["source1", "source2"],
    "confidence": "high/medium/low",
    "gaps": "Any important information that was missing or unclear"
}"""

    @staticmethod
    def reddit_analysis_system() -> str:
        """System prompt for analyzing Reddit post content."""
        return """You are an expert at analyzing Reddit discussions and extracting meaningful insights from community conversations.

Your task is to analyze Reddit post content and extract valuable real-world opinions, experiences, and insights that help answer the user's question.

When analyzing Reddit posts:
- Extract genuine user experiences and opinions
- Identify commonly agreed upon points across multiple comments
- Note expert opinions or highly upvoted insights
- Capture unique perspectives or contrarian views
- Look for practical advice and real-world examples

Return your analysis in this exact JSON format, no extra text:
{
    "key_insights": ["insight1", "insight2", "insight3"],
    "common_opinions": "What most Reddit users seem to agree on",
    "expert_opinions": ["expert_opinion1", "expert_opinion2"],
    "contrarian_views": "Any interesting opposing viewpoints",
    "practical_advice": ["advice1", "advice2"],
    "confidence": "high/medium/low"
}"""

    @staticmethod
    def synthesis_system() -> str:
        """System prompt for synthesizing all research analyses."""
        return """You are a master research synthesizer. Your task is to combine insights from multiple sources (Google, Bing, and Reddit) into one comprehensive, well-structured final answer.

When synthesizing:
- Combine complementary information from all sources
- Resolve any contradictions by weighing source credibility
- Prioritize information that appears across multiple sources
- Include real-world perspectives from Reddit alongside factual data
- Present a balanced and complete picture

Structure your response clearly with:
1. A direct answer to the question
2. Supporting evidence and details
3. Different perspectives if relevant
4. Practical takeaways

Be thorough but concise. Aim for a response that fully satisfies the user's research need."""

    # ──────────────────────────────────────────────────────────────────────────
    # MESSAGE BUILDERS
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_reddit_url_analysis_messages(user_question: str,
                                          reddit_results: Any) -> list[Dict]:
        return [
            {
                "role": "system",
                "content": PromptTemplates.reddit_url_analysis_system()
            },
            {
                "role": "user",
                "content": f"""User Question: {user_question}

Reddit Search Results:
{reddit_results}

Based on the user's question and these Reddit search results, identify the most valuable post URLs to retrieve for detailed analysis."""
            }
        ]

    @staticmethod
    def get_google_analysis_messages(user_question: str,
                                      google_results: Any) -> list[Dict]:
        return [
            {
                "role": "system",
                "content": PromptTemplates.google_analysis_system()
            },
            {
                "role": "user",
                "content": f"""User Question: {user_question}

Google Search Results:
{google_results}

Please analyze these Google search results and extract the most relevant information to answer the user's question."""
            }
        ]

    @staticmethod
    def get_bing_analysis_messages(user_question: str,
                                    bing_results: Any) -> list[Dict]:
        return [
            {
                "role": "system",
                "content": PromptTemplates.bing_analysis_system()
            },
            {
                "role": "user",
                "content": f"""User Question: {user_question}

Bing Search Results:
{bing_results}

Please analyze these Bing search results and extract the most relevant information to answer the user's question."""
            }
        ]

    @staticmethod
    def get_reddit_analysis_messages(user_question: str,
                                      reddit_posts: Any) -> list[Dict]:
        return [
            {
                "role": "system",
                "content": PromptTemplates.reddit_analysis_system()
            },
            {
                "role": "user",
                "content": f"""User Question: {user_question}

Reddit Posts and Comments:
{reddit_posts}

Please analyze these Reddit posts and extract valuable insights, opinions, and experiences relevant to the user's question."""
            }
        ]

    @staticmethod
    def get_synthesis_messages(user_question: str,
                                google_analysis: str,
                                bing_analysis: str,
                                reddit_analysis: str) -> list[Dict]:
        return [
            {
                "role": "system",
                "content": PromptTemplates.synthesis_system()
            },
            {
                "role": "user",
                "content": f"""User Question: {user_question}

--- GOOGLE SEARCH ANALYSIS ---
{google_analysis}

--- BING SEARCH ANALYSIS ---
{bing_analysis}

--- REDDIT COMMUNITY ANALYSIS ---
{reddit_analysis}

Please synthesize all of the above research into one comprehensive, well-structured final answer for the user."""
            }
        ]


# ──────────────────────────────────────────────────────────────────────────────
# BUG FIX: All functions above are static methods inside PromptTemplates class.
# main.py imports them as module-level names (e.g. `from prompts import get_reddit_analysis_messages`),
# which caused ImportError at startup. These aliases expose them at module level.
# ──────────────────────────────────────────────────────────────────────────────

get_reddit_url_analysis_messages = PromptTemplates.get_reddit_url_analysis_messages
get_google_analysis_messages = PromptTemplates.get_google_analysis_messages
get_bing_analysis_messages = PromptTemplates.get_bing_analysis_messages
get_reddit_analysis_messages = PromptTemplates.get_reddit_analysis_messages
get_synthesis_messages = PromptTemplates.get_synthesis_messages