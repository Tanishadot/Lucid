from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import settings
from core.utils.logger import logger
from knowledge.embeddings.embedder import Embedder
from knowledge.vector_store.store import VectorStore
from core.memory.memory_manager import MemoryManager
from core.prompt_manager.prompt_builder import PromptBuilder, PromptContext
from core.constraint_validator.validator import ConstraintValidator
from core.reflection_engine.questioning_strategies import QuestioningStrategies, QuestionStrategy


class ReflectionEngine:
    """Core reflection generation engine for LUCID"""
    
    def __init__(self):
        self.llm = None
        self.prompt_builder = PromptBuilder()
        self.constraint_validator = ConstraintValidator()
        self.vector_store = VectorStore()
        self.memory_manager = MemoryManager()
        self.questioning_strategies = QuestioningStrategies()
        
        # Initialize LLM
        self._initialize_llm()
        
        # Initialize vector store with sample data if empty
        self._initialize_knowledge_base()
        
        logger.info("ReflectionEngine initialized")
    
    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            self.llm = ChatOpenAI(
                model=settings.openai_model,
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
                openai_api_key=settings.openai_api_key,
                verbose=False
            )
            logger.info(f"LLM initialized: {settings.openai_model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None
    
    def _initialize_knowledge_base(self):
        """Initialize vector store with sample knowledge"""
        try:
            # Check if store is empty by attempting a search
            test_docs = self.vector_store.similarity_search("test", k=1)
            if not test_docs:
                logger.info("Initializing empty vector store with sample data")
                self.vector_store.initialize_sample_data()
        except Exception as e:
            logger.warning(f"Could not check vector store status: {e}")
    
    def generate_reflection(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Generate a reflective response"""
        try:
            # Validate input
            input_validation = self.constraint_validator.validate_input(user_message)
            if not input_validation.is_valid:
                return {
                    "success": False,
                    "error": "Invalid input",
                    "violations": input_validation.violations
                }
            
            # Get conversation context
            conversation_context = self.memory_manager.get_conversation_context(session_id)
            
            # Extract metadata for prompt building
            prompt_context = self.prompt_builder.extract_metadata_for_context(conversation_context)
            prompt_context.user_message = user_message
            
            # Retrieve philosophical context
            philosophical_context = self.vector_store.get_relevant_context(user_message)
            prompt_context.philosophical_context = philosophical_context
            
            # Generate reflection
            if settings.test_mode:
                response = self._generate_test_reflection(prompt_context)
            else:
                response = self._generate_llm_reflection(prompt_context)
            
            # Validate output
            output_validation = self.constraint_validator.validate_output(response)
            
            # If validation fails, try fallback
            if not output_validation.is_valid:
                logger.warning(f"LLM response failed validation: {output_validation.violations}")
                response = self._generate_fallback_reflection(prompt_context)
                # Re-validate fallback
                output_validation = self.constraint_validator.validate_output(response)
            
            # Store interaction in memory
            self.memory_manager.add_message(session_id, user_message, is_user=True)
            self.memory_manager.add_message(session_id, response, is_user=False, 
                                          metadata={"validation": output_validation.__dict__})
            
            return {
                "success": True,
                "response": response,
                "validation": output_validation.__dict__,
                "session_id": session_id,
                "metadata": {
                    "strategy": self.questioning_strategies.select_strategy(prompt_context.__dict__).value,
                    "philosophical_context_used": bool(philosophical_context),
                    "test_mode": settings.test_mode
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating reflection: {e}")
            return {
                "success": False,
                "error": "Reflection generation failed",
                "details": str(e)
            }
    
    def _generate_llm_reflection(self, context: PromptContext) -> str:
        """Generate reflection using LLM"""
        if not self.llm:
            raise Exception("LLM not initialized")
        
        # Build prompt
        prompt = self.prompt_builder.build_reflection_prompt(context)
        
        # Generate response
        messages = [
            SystemMessage(content=prompt),
            HumanMessage(content=f"User message: {context.user_message}")
        ]
        
        response = self.llm(messages)
        return response.content.strip()
    
    def _generate_test_reflection(self, context: PromptContext) -> str:
        """Generate reflection in test mode without LLM"""
        # Use strategy-based approach for test mode
        strategy_response = self.questioning_strategies.generate_strategy_question(context.__dict__)
        
        # Fallback static question if strategy fails
        if not strategy_response:
            return "What feels most important to explore right now?"
        
        return strategy_response
    
    def _generate_fallback_reflection(self, context: PromptContext) -> str:
        """Generate fallback reflection when LLM fails validation"""
        # Use questioning strategies as fallback
        return self.questioning_strategies.generate_strategy_question(context.__dict__)
    
    def analyze_message(self, message: str) -> Dict[str, Any]:
        """Analyze user message for metadata"""
        # Simple analysis - can be enhanced with more sophisticated NLP
        emotions = self._detect_emotions(message)
        cognitive_patterns = self._detect_cognitive_patterns(message)
        question_type = self._classify_message(message)
        
        return {
            "emotions": emotions,
            "cognitive_patterns": cognitive_patterns,
            "question_type": question_type,
            "complexity": len(message.split()),
            "sentiment": self._analyze_sentiment(message)
        }
    
    def _detect_emotions(self, message: str) -> List[str]:
        """Detect emotional indicators in message"""
        emotion_keywords = {
            "confusion": ["confused", "unclear", "don't know", "unsure", "puzzled"],
            "frustration": ["frustrated", "stuck", "annoyed", "difficult", "hard"],
            "curiosity": ["curious", "interested", "wonder", "explore", "want to know"],
            "uncertainty": ["uncertain", "maybe", "perhaps", "not sure", "might"],
            "reflection": ["think", "feel", "believe", "consider", "reflect"],
            "hope": ["hope", "wish", "optimistic", "looking forward"],
            "anxiety": ["worried", "anxious", "concerned", "nervous"]
        }
        
        detected = []
        message_lower = message.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected.append(emotion)
        
        return detected
    
    def _detect_cognitive_patterns(self, message: str) -> List[str]:
        """Detect cognitive patterns in message"""
        patterns = {
            "pattern_recognition": ["pattern", "always", "never", "every time"],
            "obligation_thinking": ["should", "must", "need to", "have to"],
            "hypothetical_thinking": ["if only", "wish", "hope", "what if"],
            "all_or_nothing": ["always", "never", "perfect", "failure"],
            "overgeneralization": ["always", "never", "everyone", "no one"],
            "catastrophizing": ["terrible", "awful", "disaster", "worst"]
        }
        
        detected = []
        message_lower = message.lower()
        
        for pattern, keywords in patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                detected.append(pattern)
        
        return detected
    
    def _classify_message(self, message: str) -> str:
        """Classify the type of user message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["help", "advice", "should", "recommend"]):
            return "seeking_advice"
        elif any(word in message_lower for word in ["confused", "unclear", "don't understand"]):
            return "seeking_clarity"
        elif any(word in message_lower for word in ["feel", "feeling", "emotion"]):
            return "emotional_exploration"
        elif any(word in message_lower for word in ["think", "believe", "opinion"]):
            return "cognitive_exploration"
        elif "?" in message:
            return "direct_question"
        else:
            return "general_reflection"
    
    def _analyze_sentiment(self, message: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "happy", "excited", "hopeful", "optimistic"]
        negative_words = ["bad", "terrible", "sad", "angry", "frustrated", "worried"]
        
        message_lower = message.lower()
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of session for analysis"""
        session_data = self.memory_manager.export_session(session_id)
        if not session_data:
            return None
        
        messages = session_data["messages"]
        user_messages = [msg for msg in messages if msg["is_user"]]
        
        # Analyze patterns across conversation
        all_emotions = []
        all_patterns = []
        
        for msg in user_messages:
            analysis = self.analyze_message(msg["text"])
            all_emotions.extend(analysis["emotions"])
            all_patterns.extend(analysis["cognitive_patterns"])
        
        return {
            "session_id": session_id,
            "message_count": len(messages),
            "user_message_count": len(user_messages),
            "duration_minutes": (session_data["last_activity"], session_data["created_at"]),
            "common_emotions": list(set(all_emotions)),
            "common_patterns": list(set(all_patterns)),
            "session_data": session_data
        }
