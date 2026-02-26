from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

class LLMReflectionGenerator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Use dummy key for testing without API calls
            api_key = "dummy_key_for_testing"
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.6,
            openai_api_key=api_key,
            verbose=False
        )
        
        self.system_prompt = """You are Lucid, a reflection-first AI companion. Your role is to help users find clarity through thoughtful questioning, NOT by giving advice or solutions.

CRITICAL RULES:
- Respond with EXACTLY ONE reflective question only
- NEVER give advice, instructions, or suggestions
- NEVER use words like: "should", "try", "consider", "you need to", "recommend", "suggest"
- NEVER provide solutions or action steps
- ALWAYS preserve user autonomy
- Focus on helping the user discover their own wisdom

Based on the user's message and the analysis provided, generate a single, open-ended reflective question that encourages deeper self-exploration without being directive."""

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", """User message: {message}
            
Analysis:
- Emotion detected: {emotion}
- Cognitive pattern: {cognitive_pattern}
- Value conflict: {value_conflict}
- Question type: {question_type}
- Philosophical context: {philosophical_context}

Generate one reflective question:""")
        ])
        
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser

    def generate_reflection(self, message: str, emotion: str, cognitive_pattern: str, 
                          value_conflict: str, question_type: str, philosophical_context: str = "") -> str:
        """Generate a reflective question using LLM"""
        try:
            response = self.chain.invoke({
                "message": message,
                "emotion": emotion,
                "cognitive_pattern": cognitive_pattern,
                "value_conflict": value_conflict,
                "question_type": question_type,
                "philosophical_context": philosophical_context
            })
            
            # Ensure response is a single question
            response = response.strip()
            if not response.endswith('?'):
                response += '?'
            
            return response
            
        except Exception as e:
            # Fallback to simple reflection if LLM fails
            return "What perspective might you be missing in this moment?"
