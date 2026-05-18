'use client';

import { useState, useEffect } from 'react';
import Welcome from '@/components/Welcome';
import DailyWalkView from '@/components/DailyWalk';
import Settings from '@/components/Settings';
import { generateDailyWalk, detectVoice, Voice, Duration, UserState } from '@/lib/companion';

type Screen = 'welcome' | 'walk' | 'settings';

interface AppState {
  archetype: string;
  voice: Voice;
  duration: Duration;
  hasStarted: boolean;
}

const STORAGE_KEY = 'emmaus-state';

function loadState(): AppState | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {
    console.error('Failed to load state:', e);
  }
  return null;
}

function saveState(state: AppState) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save state:', e);
  }
}

export default function Home() {
  const [screen, setScreen] = useState<Screen>('welcome');
  const [state, setState] = useState<AppState>({
    archetype: 'seeking',
    voice: 'emmaus',
    duration: 'normal',
    hasStarted: false,
  });
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = loadState();
    if (saved) {
      setState(saved);
      if (saved.hasStarted) {
        setScreen('walk');
      }
    }
    setIsLoaded(true);
  }, []);

  // Save to localStorage on change
  useEffect(() => {
    if (isLoaded) {
      saveState(state);
    }
  }, [state, isLoaded]);

  const handleStart = (archetype: string, voice: Voice) => {
    const newState = { ...state, archetype, voice, hasStarted: true };
    setState(newState);
    setScreen('walk');
  };

  const handleSettings = () => setScreen('settings');
  const handleBack = () => setScreen('walk');

  const handleVoiceChange = (voice: Voice) => {
    setState(prev => ({ ...prev, voice }));
  };

  const handleDurationChange = (duration: Duration) => {
    setState(prev => ({ ...prev, duration }));
  };

  const handleReset = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
    }
    setState({
      archetype: 'seeking',
      voice: 'emmaus',
      duration: 'normal',
      hasStarted: false,
    });
    setScreen('welcome');
  };

  // Generate today's walk
  const userState: UserState = {
    archetype: state.voice,
    energy: 'neutral',
    duration: state.duration,
    dayOfWeek: new Date().getDay(),
  };
  const walk = generateDailyWalk(userState);

  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-stone-950 flex items-center justify-center">
        <div className="text-amber-500 text-xl font-light animate-pulse">
          Emmaus
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-stone-950 text-stone-200">
      {screen === 'welcome' && (
        <Welcome onStart={handleStart} />
      )}
      
      {screen === 'walk' && (
        <DailyWalkView 
          walk={walk} 
          voice={state.voice} 
          onSettings={handleSettings} 
        />
      )}
      
      {screen === 'settings' && (
        <Settings
          voice={state.voice}
          duration={state.duration}
          onVoiceChange={handleVoiceChange}
          onDurationChange={handleDurationChange}
          onBack={handleBack}
          onReset={handleReset}
        />
      )}
    </main>
  );
}
