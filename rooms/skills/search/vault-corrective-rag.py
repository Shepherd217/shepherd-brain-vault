#!/usr/bin/env python3
"""
Corrective RAG for Vault
Pattern: Corrective RAG (from awesome-llm-apps rag_tutorials/corrective_rag/)
Source: Retrieve → Grade Relevance → Reformulate → Retry

When vault search fails to find relevant docs, this system:
1. Grades retrieved documents for relevance
2. If insufficient: reformulates query with synonyms/broader terms
3. Re-retrieves with reformulated query
4. Synthesizes answer with verified sources
"""

import sys
import sqlite3
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter

class CorrectiveRAG:
    """Corrective retrieval-augmented generation for vault memory."""
    
    def __init__(self, db_path: str = None, verbose: bool = True):
        self.verbose = verbose
        self.db_path = db_path or '/root/.openclaw/workspace/.clawdbot/vault-search.db'
        self.vocab = self._load_vocab()
        self.reformulation_rules = self._load_reformulation_rules()
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def _load_vocab(self) -> Dict[str, float]:
        """Load TF-IDF vocabulary from semantic search DB."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT word, idf FROM vocab")
            vocab = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()
            return vocab
        except Exception as e:
            self._log(f"Warning: Could not load vocab: {e}")
            return {}
    
    def _load_reformulation_rules(self) -> Dict[str, List[str]]:
        """Query reformulation rules — synonyms and broader terms."""
        return {
            # Business terms
            'lead': ['prospect', 'client', 'business', 'company', 'target'],
            'outreach': ['contact', 'email', 'message', 'approach', 'pitch'],
            'audit': ['review', 'analysis', 'assessment', 'score', 'check'],
            'cleaning': ['housekeeping', 'janitorial', 'maid', 'sanitize'],
            'website': ['site', 'page', 'web', 'digital', 'online'],
            
            # Agent terms
            'agent': ['bot', 'ai', 'assistant', 'worker', 'promachos'],
            'moltos': ['marketplace', 'platform', 'economy', 'ecosystem'],
            'skill': ['ability', 'capability', 'tool', 'function', 'feature'],
            'memory': ['recall', 'history', 'log', 'record', 'vault'],
            
            # Technical terms
            'api': ['endpoint', 'route', 'interface', 'rest', 'graphql'],
            'bug': ['error', 'issue', 'failure', 'broken', 'fault'],
            'test': ['verify', 'check', 'validate', 'confirm', 'ensure'],
            'deploy': ['ship', 'release', 'launch', 'publish', 'push'],
            
            # Generic expansions
            'find': ['search', 'locate', 'discover', 'identify', 'get'],
            'make': ['create', 'build', 'generate', 'produce', 'develop'],
            'fix': ['repair', 'resolve', 'correct', 'patch', 'solve'],
            'best': ['top', 'highest', 'optimal', 'ideal', 'superior'],
        }
    
    def semantic_search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search vault using existing semantic search index."""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Simple TF-IDF search (same as vault_semantic_search.py)
            query_terms = self._tokenize(query)
            query_vec = self._vectorize(query_terms)
            
            cursor = conn.execute("SELECT id, path, title, content FROM documents")
            results = []
            
            for row in cursor.fetchall():
                doc_id, path, title, content = row
                
                # Get TF-IDF vector from search_index
                idx_cursor = conn.execute(
                    "SELECT tfidf FROM search_index WHERE doc_id = ?",
                    (doc_id,)
                )
                idx_row = idx_cursor.fetchone()
                
                if not idx_row or not idx_row[0]:
                    continue
                
                doc_vec = self._deserialize_vec(idx_row[0])
                
                # Cosine similarity
                score = self._cosine_similarity(query_vec, doc_vec)
                
                if score > 0.01:  # Minimum threshold
                    results.append({
                        'doc_id': doc_id,
                        'path': path,
                        'title': title or path.split('/')[-1],
                        'content': content[:500] if content else '',  # Preview
                        'score': score
                    })
            
            conn.close()
            
            # Sort by relevance
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:limit]
            
        except Exception as e:
            self._log(f"Search error: {e}")
            return []
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        return re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    def _vectorize(self, terms: List[str]) -> Dict[str, float]:
        """Create TF-IDF vector for query."""
        vec = {}
        term_counts = Counter(terms)
        
        for term, count in term_counts.items():
            if term in self.vocab:
                # Simple TF-IDF
                tf = count / len(terms)
                idf = 1.0 / (1 + self.vocab.get(term, 1))
                vec[term] = tf * idf
        
        return vec
    
    def _deserialize_vec(self, blob: bytes) -> Dict[str, float]:
        """Deserialize TF-IDF vector from JSON blob."""
        import json
        try:
            return json.loads(blob)
        except:
            return {}
    
    def _cosine_similarity(self, vec1: Dict, vec2: Dict) -> float:
        """Calculate cosine similarity between two vectors."""
        # Dot product
        dot = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in set(vec1) & set(vec2))
        
        # Magnitudes
        mag1 = sum(v**2 for v in vec1.values()) ** 0.5
        mag2 = sum(v**2 for v in vec2.values()) ** 0.5
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        return dot / (mag1 * mag2)
    
    def grade_relevance(self, query: str, doc: Dict) -> float:
        """Grade how relevant a document is to the query."""
        query_terms = set(self._tokenize(query))
        content = doc.get('content', '').lower()
        title = doc.get('title', '').lower()
        
        # Check term overlap
        content_terms = set(self._tokenize(content))
        title_terms = set(self._tokenize(title))
        
        # Title match is weighted higher
        title_overlap = len(query_terms & title_terms) / max(len(query_terms), 1)
        content_overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
        
        # Combined score (title matters more)
        relevance = (title_overlap * 0.6) + (content_overlap * 0.4)
        
        # Boost if key terms appear in first 100 chars
        preview = content[:100]
        if any(term in preview for term in query_terms):
            relevance += 0.1
        
        return min(1.0, relevance)
    
    def reformulate_query(self, query: str, feedback: str) -> str:
        """Reformulate query based on feedback."""
        terms = self._tokenize(query)
        
        # Apply reformulation rules
        new_terms = []
        for term in terms:
            if term in self.reformulation_rules:
                # Add synonyms
                synonyms = self.reformulation_rules[term]
                # Pick a synonym not already in query
                for syn in synonyms:
                    if syn not in terms:
                        new_terms.append(syn)
                        break
            new_terms.append(term)
        
        # If feedback says "too specific", add broader terms
        if 'too specific' in feedback.lower():
            broader_terms = {
                'champaign': 'illinois',
                'cleaning': 'services',
                'website': 'digital',
            }
            for specific, broad in broader_terms.items():
                if specific in query.lower() and broad not in new_terms:
                    new_terms.append(broad)
        
        return ' '.join(new_terms)
    
    def retrieve_corrective(self, query: str, max_cycles: int = 2,
                           min_relevant: int = 3) -> Dict:
        """Corrective RAG: retrieve with reformulation if needed."""
        
        self._log(f"\n{'='*60}")
        self._log(f"CORRECTIVE RAG QUERY: {query}")
        self._log(f"{'='*60}")
        
        current_query = query
        cycle = 0
        all_results = []
        
        while cycle <= max_cycles:
            self._log(f"\n--- Cycle {cycle + 1} ---")
            self._log(f"Query: {current_query}")
            
            # Retrieve
            results = self.semantic_search(current_query, limit=5)
            
            if not results:
                self._log("No results found.")
                break
            
            # Grade each result
            graded = []
            for doc in results:
                relevance = self.grade_relevance(current_query, doc)
                doc['relevance'] = relevance
                graded.append(doc)
                
                status = "✅" if relevance >= 0.3 else "⚠️"
                self._log(f"  {status} {doc['title'][:50]}... (relevance: {relevance:.2f})")
            
            all_results.extend(graded)
            
            # Count highly relevant
            highly_relevant = [d for d in graded if d['relevance'] >= 0.3]
            
            self._log(f"\nHighly relevant docs: {len(highly_relevant)}/{len(graded)}")
            
            if len(highly_relevant) >= min_relevant:
                self._log(f"✅ Sufficient results found. Stopping.")
                break
            
            if cycle >= max_cycles:
                self._log(f"⚠️ Max cycles reached. Using best available.")
                break
            
            # Reformulate
            feedback = f"Too specific. Found {len(highly_relevant)} relevant docs."
            current_query = self.reformulate_query(current_query, feedback)
            
            self._log(f"\n🔄 Reformulated: {current_query}")
            cycle += 1
        
        # Deduplicate and sort
        seen = set()
        unique_results = []
        for doc in sorted(all_results, key=lambda x: x['relevance'], reverse=True):
            if doc['doc_id'] not in seen:
                seen.add(doc['doc_id'])
                unique_results.append(doc)
        
        # Synthesize answer
        top_results = unique_results[:5]
        
        answer = self._synthesize(query, top_results)
        
        return {
            'query': query,
            'cycles': cycle + 1,
            'results': top_results,
            'answer': answer,
            'total_docs_found': len(unique_results),
            'highly_relevant': len([d for d in top_results if d['relevance'] >= 0.3])
        }
    
    def _synthesize(self, query: str, docs: List[Dict]) -> str:
        """Synthesize answer from retrieved documents."""
        if not docs:
            return "No relevant documents found in vault."
        
        # Build context from top docs
        context_parts = []
        for i, doc in enumerate(docs[:3], 1):
            context_parts.append(
                f"[{i}] {doc['title']}\n"
                f"    Relevance: {doc['relevance']:.2f}\n"
                f"    {doc['content'][:200]}..."
            )
        
        # Simple synthesis (can be enhanced with LLM)
        synthesis = f"Based on {len(docs)} documents from the vault:\n\n"
        synthesis += "\n\n".join(context_parts)
        
        # Add source citations
        synthesis += "\n\nSources:\n"
        for i, doc in enumerate(docs[:3], 1):
            synthesis += f"  [{i}] {doc['title']} (relevance: {doc['relevance']:.2f})\n"
        
        return synthesis
    
    def query(self, question: str) -> str:
        """Public API: ask a question, get an answer."""
        result = self.retrieve_corrective(question)
        
        print(f"\n{'='*60}")
        print(f"ANSWER")
        print(f"{'='*60}")
        print(result['answer'])
        print(f"\n{'='*60}")
        print(f"Query: {result['query']}")
        print(f"Cycles: {result['cycles']}")
        print(f"Docs found: {result['total_docs_found']}")
        print(f"Highly relevant: {result['highly_relevant']}")
        print(f"{'='*60}")
        
        return result['answer']


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python vault-corrective-rag.py '<question>'")
        print("Example: python vault-corrective-rag.py 'What was the highest scoring lead?'")
        print("Example: python vault-corrective-rag.py 'How do I test MoltOS endpoints?'")
        sys.exit(1)
    
    question = ' '.join(sys.argv[1:])
    
    rag = CorrectiveRAG(verbose=True)
    answer = rag.query(question)
    
    return answer


if __name__ == '__main__':
    main()
