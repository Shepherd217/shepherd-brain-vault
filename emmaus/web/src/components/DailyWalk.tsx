import { useState } from 'react';
import { DailyWalk, Voice } from '@/lib/companion';

interface DailyWalkProps {
  walk: DailyWalk;
  voice: Voice;
  onSettings: () => void;
}

type Phase = 'morning' | 'practice' | 'scripture' | 'evening' | 'complete';

export default function DailyWalkView({ walk, voice, onSettings }: DailyWalkProps) {
  const [phase, setPhase] = useState<Phase>('morning');
  const [energy, setEnergy] = useState(3);
  const [reflection, setReflection] = useState('');
  const [gratitude, setGratitude] = useState('');
  const [burden, setBurden] = useState('');

  const phases: { id: Phase; label: string; icon: string }[] = [
    { id: 'morning', label: 'Morning', icon: '🌅' },
    { id: 'practice', label: 'Practice', icon: '📖' },
    { id: 'scripture', label: 'Scripture', icon: '✨' },
    { id: 'evening', label: 'Evening', icon: '🌙' },
  ];

  const currentPhaseIndex = phases.findIndex(p => p.id === phase);

  const handleNext = () => {
    const nextIndex = currentPhaseIndex + 1;
    if (nextIndex < phases.length) {
      setPhase(phases[nextIndex].id);
    } else {
      setPhase('complete');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-stone-950 via-stone-900 to-stone-950">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-stone-950/80 backdrop-blur-md border-b border-stone-800">
        <div className="max-w-lg mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-amber-500 font-light text-lg">Emmaus</span>
          </div>
          <button 
            onClick={onSettings}
            className="text-stone-400 hover:text-amber-400 transition-colors"
          >
            ⚙️
          </button>
        </div>
      </header>

      <div className="max-w-lg mx-auto px-4 py-8 space-y-8">
        {/* Progress */}
        <div className="flex gap-2">
          {phases.map((p, i) => (
            <div
              key={p.id}
              className={`flex-1 h-1 rounded-full transition-all duration-500 ${
                i <= currentPhaseIndex ? 'bg-amber-600' : 'bg-stone-800'
              }`}
            />
          ))}
        </div>

        {/* Phase Label */}
        <div className="flex items-center gap-2 text-amber-500/70">
          <span className="text-2xl">{phases[currentPhaseIndex]?.icon || '✨'}</span>
          <span className="text-sm uppercase tracking-widest">{phases[currentPhaseIndex]?.label || 'Complete'}</span>
        </div>

        {/* MORNING PHASE */}
        {phase === 'morning' && (
          <div className="space-y-8">
            <div className="space-y-4">
              <p className="text-2xl text-stone-200 font-light">{walk.morning.greeting}</p>
              <p className="text-lg text-stone-400">{walk.morning.energyPrompt}</p>
            </div>

            <div className="space-y-4">
              <p className="text-stone-300">How are you arriving today? Slide to where you are:</p>
              <div className="space-y-3">
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={energy}
                  onChange={(e) => setEnergy(parseInt(e.target.value))}
                  className="w-full h-2 bg-stone-800 rounded-lg appearance-none cursor-pointer accent-amber-600"
                />
                <div className="flex justify-between text-xs text-stone-500">
                  <span>Drained</span>
                  <span>Tired</span>
                  <span>Steady</span>
                  <span>Alert</span>
                  <span>Energized</span>
                </div>
              </div>
            </div>

            <button
              onClick={handleNext}
              className="w-full py-4 bg-amber-700 hover:bg-amber-600 text-white rounded-xl font-medium transition-all shadow-lg shadow-amber-900/20"
            >
              {walk.morning.invitation} →
            </button>
          </div>
        )}

        {/* PRACTICE PHASE */}
        {phase === 'practice' && (
          <div className="space-y-8">
            <div className="space-y-2">
              <h2 className="text-2xl text-amber-200 font-light">{walk.practice.title}</h2>
            </div>

            <div className="bg-stone-900/50 border border-stone-800 rounded-xl p-6 space-y-4">
              {walk.practice.content.split('\n\n').map((paragraph, i) => (
                <p key={i} className="text-stone-300 leading-relaxed">{paragraph}</p>
              ))}
            </div>

            <div className="bg-amber-950/30 border border-amber-900/30 rounded-xl p-4">
              <p className="text-amber-200/80 italic">{walk.practice.closing}</p>
            </div>

            <button
              onClick={handleNext}
              className="w-full py-4 bg-amber-700 hover:bg-amber-600 text-white rounded-xl font-medium transition-all shadow-lg shadow-amber-900/20"
            >
              Continue to Scripture →
            </button>
          </div>
        )}

        {/* SCRIPTURE PHASE */}
        {phase === 'scripture' && (
          <div className="space-y-8">
            <div className="space-y-2">
              <h2 className="text-xl text-amber-200 font-light">{walk.scripture.reference}</h2>
            </div>

            <div className="bg-stone-900/50 border border-stone-800 rounded-xl p-6 space-y-4">
              <blockquote className="text-lg text-stone-200 leading-relaxed italic border-l-4 border-amber-600 pl-4">
                {walk.scripture.text}
              </blockquote>
            </div>

            <div className="bg-stone-800/50 rounded-xl p-4">
              <p className="text-sm text-stone-400"><span className="text-amber-500">Context: </span>{walk.scripture.context}</p>
            </div>

            <div className="bg-amber-950/30 border border-amber-900/30 rounded-xl p-4">
              <p className="text-amber-200/80 italic">"Did not our hearts burn?"</p>
            </div>

            <button
              onClick={handleNext}
              className="w-full py-4 bg-amber-700 hover:bg-amber-600 text-white rounded-xl font-medium transition-all shadow-lg shadow-amber-900/20"
            >
              Evening Reflection →
            </button>
          </div>
        )}

        {/* EVENING PHASE */}
        {phase === 'evening' && (
          <div className="space-y-8">
            <div className="space-y-4">
              <p className="text-xl text-stone-200 font-light">{walk.evening.prompt}</p>
            </div>

            <div className="space-y-4">
              <label className="block text-stone-300">{walk.evening.gratitude}</label>
              <textarea
                value={gratitude}
                onChange={(e) => setGratitude(e.target.value)}
                placeholder="Even if it's small..."
                className="w-full bg-stone-900 border border-stone-700 rounded-xl p-4 text-stone-200 placeholder-stone-600 focus:outline-none focus:border-amber-600 transition-colors min-h-[100px]"
              />
            </div>

            <div className="space-y-4">
              <label className="block text-stone-300">{walk.evening.examen}</label>
              <textarea
                value={burden}
                onChange={(e) => setBurden(e.target.value)}
                placeholder="Name it. Don't fix it..."
                className="w-full bg-stone-900 border border-stone-700 rounded-xl p-4 text-stone-200 placeholder-stone-600 focus:outline-none focus:border-amber-600 transition-colors min-h-[100px]"
              />
            </div>

            <div className="bg-stone-900/50 border border-stone-800 rounded-xl p-6">
              <p className="text-stone-300 leading-relaxed whitespace-pre-line">{walk.evening.release}</p>
            </div>

            <button
              onClick={handleNext}
              className="w-full py-4 bg-amber-700 hover:bg-amber-600 text-white rounded-xl font-medium transition-all shadow-lg shadow-amber-900/20"
            >
              Rest well 🌙
            </button>
          </div>
        )}

        {/* COMPLETE PHASE */}
        {phase === 'complete' && (
          <div className="space-y-8 text-center">
            <div className="space-y-4">
              <span className="text-6xl">🌅</span>
              <h2 className="text-2xl text-amber-200 font-light">Well walked.</h2>
              <p className="text-stone-400">
                The burning comes in the walking. And you walked today.
              </p>
            </div>

            <div className="bg-stone-900/50 border border-stone-800 rounded-xl p-6 space-y-3 text-left">
              <p className="text-sm text-stone-500 uppercase tracking-widest">Today's Walk</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-stone-400">Practice</span>
                  <span className="text-amber-200">{walk.practice.title}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-stone-400">Scripture</span>
                  <span className="text-amber-200">{walk.scripture.reference}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-stone-400">Gratitude</span>
                  <span className="text-amber-200">{gratitude || 'Not recorded'}</span>
                </div>
              </div>
            </div>

            <button
              onClick={() => window.location.reload()}
              className="w-full py-4 bg-stone-800 hover:bg-stone-700 text-stone-300 rounded-xl font-medium transition-all border border-stone-700"
            >
              Walk Again Tomorrow
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
