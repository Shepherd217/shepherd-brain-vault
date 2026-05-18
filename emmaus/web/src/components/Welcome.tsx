import { useState, useEffect } from 'react';
import { detectVoice, Voice } from '@/lib/companion';

interface WelcomeProps {
  onStart: (archetype: string, voice: Voice) => void;
}

const archetypes = [
  {
    id: 'seeking',
    label: 'I\'m curious',
    subtitle: 'Not sure what I believe, but I\'m asking questions',
    emoji: '🚶',
    color: 'from-amber-700 to-amber-900'
  },
  {
    id: 'broken',
    label: 'I\'m weary',
    subtitle: 'Tired, grieving, numb — I need gentleness',
    emoji: '🍃',
    color: 'from-stone-600 to-stone-800'
  },
  {
    id: 'complacent',
    label: 'I\'m coasting',
    subtitle: 'Faith feels routine — I need a spark',
    emoji: '🔥',
    color: 'from-orange-700 to-red-900'
  },
  {
    id: 'skeptical',
    label: 'I\'m questioning',
    subtitle: 'Intellectually honest, wrestling with doubts',
    emoji: '💭',
    color: 'from-slate-600 to-slate-800'
  },
  {
    id: 'mature',
    label: 'I\'m walking',
    subtitle: 'Years of faith — I need companionship, not content',
    emoji: '🌿',
    color: 'from-emerald-700 to-emerald-900'
  }
];

export default function Welcome({ onStart }: WelcomeProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);

  const handleStart = () => {
    if (!selected) return;
    const voice = detectVoice(selected);
    onStart(selected, voice);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-stone-950 via-stone-900 to-amber-950 flex flex-col items-center justify-center px-4 py-12">
      {/* Background texture */}
      <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_50%_50%,rgba(251,191,36,0.15),transparent_70%)]" />
      
      <div className="relative z-10 max-w-md w-full text-center space-y-8">
        {/* Logo / Title */}
        <div className="space-y-2">
          <h1 className="text-5xl font-light tracking-tight text-amber-100">
            Emmaus
          </h1>
          <p className="text-lg text-amber-200/60 italic font-light">
            Did not our hearts burn?
          </p>
        </div>

        {/* Greeting */}
        <div className="space-y-4">
          <p className="text-xl text-stone-300 font-light leading-relaxed">
            Hey.
          </p>
          <p className="text-lg text-stone-400 leading-relaxed">
            However you got here — you're welcome.
          </p>
          <p className="text-base text-stone-500">
            Where are you right now?
          </p>
        </div>

        {/* Archetype Buttons */}
        <div className="space-y-3">
          {archetypes.map((a) => (
            <button
              key={a.id}
              onClick={() => setSelected(a.id)}
              onMouseEnter={() => setHovered(a.id)}
              onMouseLeave={() => setHovered(null)}
              className={`w-full p-4 rounded-xl border transition-all duration-300 text-left group
                ${selected === a.id 
                  ? `bg-gradient-to-r ${a.color} border-amber-500/50 shadow-lg shadow-amber-900/20` 
                  : 'bg-stone-800/50 border-stone-700 hover:border-stone-500'
                }
              `}
            >
              <div className="flex items-center gap-4">
                <span className="text-2xl">{a.emoji}</span>
                <div className="flex-1">
                  <div className={`font-medium ${selected === a.id ? 'text-amber-100' : 'text-stone-200'}`}>
                    {a.label}
                  </div>
                  <div className={`text-sm ${selected === a.id ? 'text-amber-200/70' : 'text-stone-500'}`}>
                    {a.subtitle}
                  </div>
                </div>
                {selected === a.id && (
                  <span className="text-amber-400 text-xl">✓</span>
                )}
              </div>
            </button>
          ))}
        </div>

        {/* CTA */}
        <button
          onClick={handleStart}
          disabled={!selected}
          className={`w-full py-4 rounded-xl text-lg font-medium transition-all duration-300
            ${selected 
              ? 'bg-amber-700 hover:bg-amber-600 text-white shadow-lg shadow-amber-900/30' 
              : 'bg-stone-800 text-stone-600 cursor-not-allowed'
            }
          `}
        >
          {selected ? 'Walk with me' : 'Choose where you are'}
        </button>

        {/* Subtle footer */}
        <p className="text-xs text-stone-600">
          No account needed. Your walk is yours.
        </p>
      </div>
    </div>
  );
}
