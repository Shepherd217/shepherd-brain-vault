#!/usr/bin/env python3
"""
Conversation State Machine
Pattern: Conversation State Machine (from awesome-llm-apps ai_personal_assistants/)

Tracks conversation state, handles context switching, resumes interrupted flows.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ConversationStateMachine:
    """Manages conversation context and state transitions."""
    
    STATES = {
        'idle': 'Waiting for input',
        'researching': 'Gathering information',
        'auditing': 'Analyzing websites or data',
        'drafting': 'Creating content or outreach',
        'reviewing': 'Checking or validating output',
        'building': 'Writing code or implementations',
        'debugging': 'Fixing errors or issues',
        'explaining': 'Answering questions or teaching',
    }
    
    INTENT_PATTERNS = {
        'research': ['find', 'search', 'look up', 'research', 'discover', 'scrape'],
        'audit': ['audit', 'analyze', 'review', 'score', 'check'],
        'draft': ['write', 'draft', 'create', 'generate', 'compose'],
        'review': ['review', 'check', 'validate', 'verify', 'look at'],
        'build': ['build', 'implement', 'code', 'write script', 'create'],
        'debug': ['fix', 'debug', 'repair', 'solve', 'error'],
        'explain': ['explain', 'what is', 'how does', 'why', 'tell me'],
        'resume': ['resume', 'continue', 'go back', 'what about', 'that'],
        'interrupt': ['actually', 'wait', 'hold on', 'instead', 'switch to'],
    }
    
    def __init__(self, state_dir: str = None, verbose: bool = True):
        self.verbose = verbose
        self.state_dir = Path(state_dir or '/root/.openclaw/workspace/vault/rooms/state')
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.current_state = self._load_current_state()
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def _load_current_state(self) -> Dict:
        """Load current conversation state from disk."""
        state_file = self.state_dir / 'current.json'
        if state_file.exists():
            return json.loads(state_file.read_text())
        return {
            'state': 'idle',
            'context': {},
            'history': [],
            'stack': [],  # For nested contexts
            'last_updated': datetime.now().isoformat()
        }
    
    def _save_state(self):
        """Save current state to disk."""
        state_file = self.state_dir / 'current.json'
        self.current_state['last_updated'] = datetime.now().isoformat()
        state_file.write_text(json.dumps(self.current_state, indent=2))
    
    def detect_intent(self, message: str) -> str:
        """Classify user intent from message."""
        message_lower = message.lower()
        
        scores = {}
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = sum(1 for p in patterns if p in message_lower)
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return 'explain'  # Default
        
        return max(scores, key=scores.get)
    
    def transition(self, new_state: str, context: Dict = None):
        """Transition to a new state, saving previous."""
        old_state = self.current_state['state']
        
        # Push current to stack
        self.current_state['stack'].append({
            'state': old_state,
            'context': self.current_state['context'].copy(),
            'timestamp': datetime.now().isoformat()
        })
        
        # Limit stack depth
        if len(self.current_state['stack']) > 10:
            self.current_state['stack'].pop(0)
        
        # Update state
        self.current_state['state'] = new_state
        if context:
            self.current_state['context'] = context
        
        # Log transition
        self.current_state['history'].append({
            'from': old_state,
            'to': new_state,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_state()
        
        self._log(f"🔄 State: {old_state} → {new_state}")
        if context:
            self._log(f"   Context: {list(context.keys())}")
    
    def handle_interrupt(self, new_intent: str, new_context: Dict = None) -> Tuple[str, str]:
        """Handle context switch (interrupt). Returns (old_state, new_state)."""
        old_state = self.current_state['state']
        self._log(f"⏸️  INTERRUPT: Switching from {old_state} to {new_intent}")
        
        # Save current to stack
        self.current_state['stack'].append({
            'state': old_state,
            'context': self.current_state['context'].copy(),
            'timestamp': datetime.now().isoformat(),
            'note': 'interrupted'
        })
        
        # Limit stack depth
        if len(self.current_state['stack']) > 10:
            self.current_state['stack'].pop(0)
        
        # Switch to new state
        self.current_state['state'] = new_intent
        if new_context:
            self.current_state['context'] = new_context
        
        self._save_state()
        
        self._log(f"   Saved previous context. Can resume with 'resume' or 'go back'")
        return old_state, new_intent
    
    def resume_previous(self) -> Optional[Dict]:
        """Resume previous context from stack."""
        if not self.current_state['stack']:
            self._log("⚠️  No previous context to resume")
            return None
        
        previous = self.current_state['stack'].pop()
        
        self.current_state['state'] = previous['state']
        self.current_state['context'] = previous['context']
        
        self._save_state()
        
        self._log(f"▶️  RESUMED: {previous['state']}")
        self._log(f"   Context: {list(previous['context'].keys())}")
        
        return previous
    
    def process_message(self, message: str, current_context: Dict = None) -> Dict:
        """Process a user message and determine action."""
        intent = self.detect_intent(message)
        
        self._log(f"\n{'='*50}")
        self._log(f"MESSAGE: {message[:60]}...")
        self._log(f"DETECTED INTENT: {intent}")
        self._log(f"CURRENT STATE: {self.current_state['state']}")
        self._log(f"{'='*50}")
        
        # Handle resume
        if intent == 'resume':
            previous = self.resume_previous()
            return {
                'action': 'resume',
                'state': previous['state'] if previous else self.current_state['state'],
                'context': self.current_state['context'],
                'message': f"Resuming {previous['state']}" if previous else "Nothing to resume"
            }
        
        # Handle interrupt
        if intent == 'interrupt':
            self.handle_interrupt('idle', current_context)
            return {
                'action': 'interrupt',
                'state': 'idle',
                'context': current_context,
                'message': "Context saved. What would you like to switch to?"
            }
        
        # Same intent = continue
        if intent == self.current_state['state'] or self.current_state['state'] == 'idle':
            if self.current_state['state'] == 'idle':
                self.transition(intent, current_context)
            else:
                # Update context
                if current_context:
                    self.current_state['context'].update(current_context)
                    self._save_state()
            
            return {
                'action': 'continue',
                'state': self.current_state['state'],
                'context': self.current_state['context'],
                'message': f"Continuing {self.current_state['state']}"
            }
        
        # Different intent = interrupt and switch
        old_state, new_state = self.handle_interrupt(intent, current_context)
        
        return {
            'action': 'switch',
            'state': new_state,
            'previous_state': old_state,
            'new_state': new_state,
            'context': current_context,
            'message': f"Switching from {old_state} to {intent}"
        }
    
    def get_status(self) -> Dict:
        """Get current state status."""
        return {
            'state': self.current_state['state'],
            'context_keys': list(self.current_state['context'].keys()),
            'stack_depth': len(self.current_state['stack']),
            'history_count': len(self.current_state['history']),
            'last_updated': self.current_state['last_updated']
        }
    
    def reset(self):
        """Reset to idle state."""
        self.current_state = {
            'state': 'idle',
            'context': {},
            'history': [],
            'stack': [],
            'last_updated': datetime.now().isoformat()
        }
        self._save_state()
        self._log("🔄 State reset to idle")


def main():
    """CLI demo of state machine."""
    csm = ConversationStateMachine(verbose=True)
    
    print("Conversation State Machine Demo")
    print("Commands: status, reset, or type a message")
    print("-" * 50)
    
    # Simulate some interactions
    test_messages = [
        "Find me cleaning companies in Champaign",
        "Audit the first one",
        "Actually wait, check this tweet first",
        "What about that cleaning company we found?",
        "Resume",
        "Draft outreach for Lisa Cleaning",
    ]
    
    for msg in test_messages:
        result = csm.process_message(msg)
        print(f"\nResult: {result['action']} → {result['state']}")
        print(f"Message: {result['message']}")
        print(f"Stack depth: {csm.get_status()['stack_depth']}")
        print("-" * 50)
    
    print("\nFinal Status:")
    print(json.dumps(csm.get_status(), indent=2))


if __name__ == '__main__':
    main()
