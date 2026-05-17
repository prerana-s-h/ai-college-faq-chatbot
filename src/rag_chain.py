"""
Conversational RAG chain module.
Combines FAISS retrieval with Groq LLM and conversation memory.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import config
from src.indexer import get_or_build_index
from src.fallback import detect_intent, get_fallback_message, log_unanswered
from src.translator import (
    translate_to_english,
    translate_from_english,
    TRANSLATION_AVAILABLE,
)


class CollegeChatbot:
    """Conversational RAG chatbot for college FAQ queries."""

    def __init__(self):
        """Initialize the chatbot with LLM, vector store, and memory."""
        # Initialize Groq LLM
        if not config.GROQ_API_KEY or config.GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY not set! Please add your key to the .env file."
            )

        self.llm = ChatGroq(
            api_key=config.GROQ_API_KEY,
            model=config.GROQ_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )

        # Initialize vector store
        self.vector_store = get_or_build_index()
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": config.TOP_K},
        )

        # Conversation memory (simple list-based)
        self.chat_history = []
        self.max_history = config.MEMORY_WINDOW

        # Build the prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", config.SYSTEM_PROMPT),
                ("human", "{question}"),
            ]
        )

        # Build the chain
        self.chain = self.prompt | self.llm | StrOutputParser()

    def _format_history(self) -> str:
        """Format chat history into a string for the prompt."""
        if not self.chat_history:
            return "No previous conversation."

        history_lines = []
        for msg in self.chat_history[-(self.max_history * 2):]:
            if isinstance(msg, HumanMessage):
                history_lines.append(f"Student: {msg.content}")
            elif isinstance(msg, AIMessage):
                history_lines.append(f"Assistant: {msg.content}")

        return "\n".join(history_lines)

    def _retrieve_context(self, query: str) -> str:
        """Retrieve relevant documents from the vector store."""
        # Combine query with recent history for better retrieval
        enhanced_query = query
        if self.chat_history:
            last_msgs = self.chat_history[-2:]
            context_parts = [msg.content for msg in last_msgs]
            enhanced_query = " ".join(context_parts) + " " + query

        docs = self.retriever.invoke(enhanced_query)

        if not docs:
            return ""

        context_parts = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "unknown")
            category = doc.metadata.get("category", "")
            header = f"[Source: {source}"
            if category:
                header += f" | Category: {category}"
            header += "]"
            context_parts.append(f"{header}\n{doc.page_content}")

        return "\n\n---\n\n".join(context_parts)

    def _check_relevance(self, query: str) -> bool:
        """Check if retrieved documents are relevant enough."""
        results = self.vector_store.similarity_search_with_score(query, k=1)
        if not results:
            return False
        _, score = results[0]
        # For normalized embeddings with FAISS L2 distance:
        # Lower score = more similar. Threshold ~1.0 for relevance.
        return score < 1.2

    def ask(self, question: str, language: str = "en") -> str:
        """
        Process a student question and return an answer.

        Args:
            question: The student's question
            language: Language code for the response (e.g., 'en', 'hi')

        Returns:
            The chatbot's response string
        """
        original_question = question

        # Translate if not English
        if language != "en" and TRANSLATION_AVAILABLE:
            question = translate_to_english(question, source_lang=language)

        # Detect intent
        intent = detect_intent(question)

        # Check relevance
        is_relevant = self._check_relevance(question)

        if not is_relevant:
            log_unanswered(original_question, intent)
            fallback = get_fallback_message(intent)
            if language != "en" and TRANSLATION_AVAILABLE:
                fallback = translate_from_english(fallback, language)
            return fallback

        # Retrieve context
        context = self._retrieve_context(question)
        chat_history = self._format_history()

        # Generate response
        try:
            response = self.chain.invoke(
                {
                    "context": context,
                    "chat_history": chat_history,
                    "question": question,
                }
            )
        except Exception as e:
            print(f"[RAG Chain] Error generating response: {e}")
            return f"I'm having trouble processing your question right now. Please try again. Error: {str(e)}"

        # Update memory
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response))

        # Trim memory if needed
        if len(self.chat_history) > self.max_history * 2:
            self.chat_history = self.chat_history[-(self.max_history * 2):]

        # Translate response back if needed
        if language != "en" and TRANSLATION_AVAILABLE:
            response = translate_from_english(response, language)

        return response

    def clear_memory(self):
        """Clear conversation history."""
        self.chat_history = []

    def rebuild_index(self):
        """Rebuild the FAISS index from all sources."""
        from src.indexer import build_index, save_index

        self.vector_store = build_index()
        save_index(self.vector_store)
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": config.TOP_K},
        )

    def get_stats(self) -> dict:
        """Get chatbot statistics."""
        index_path = os.path.join(config.FAISS_INDEX_DIR, "index.faiss")
        last_updated = "Never"
        if os.path.exists(index_path):
            import time
            mtime = os.path.getmtime(index_path)
            last_updated = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))

        return {
            "total_documents": self.vector_store.index.ntotal,
            "conversation_turns": len(self.chat_history) // 2,
            "last_index_update": last_updated,
            "model": config.GROQ_MODEL,
        }
