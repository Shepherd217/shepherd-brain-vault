import { Voice, Duration } from '@/lib/companion';

interface SettingsProps {
  voice: Voice;
  duration: Duration;
  onVoiceChange: (voice: Voice) => void;
  onDurationChange: (duration: Duration) => void;
  onBack: () => void;
  onReset: () => void;
}

const voiceOptions: { id: Voice; label: string; description: string }[] = [
  { id: 'emmaus', label: 'Emmaus (Default)', description: 'Warm, curious, walking with you' },
  { id: 'manning', label: 'Manning', description: 'Gentle, grace-filled, for the weary' },
  { id: 'paul', label: 'Paul', description: 'Urgent, corrective, for the complacent' },
  { id: 'keller', label: 'Keller', description: 'Intellectual, for the questioning' },
  { id: 'peer', label: 'Peer', description: 'Respectful, for the mature walker' },
];

const durationOptions: { id: Duration; label: string; description: string }[] = [
  { id: 'brief', label: '5 minutes', description: 'One breath, one word, one step' },
  { id: 'normal', label: '15 minutes', description: 'Morning, practice, scripture, evening' },
  { id: 'extended', label: '30 minutes', description: 'Deep formation, full liturgy' },
];

export default function Settings({ 
  voice, 
  duration, 
  onVoiceChange, 
  onDurationChange, 
  onBack,
  onReset 
}: SettingsProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-stone-950 via-stone-900 to-stone-950">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-stone-950/80 backdrop-blur-md border-b border-stone-800">
        <div className="max-w-lg mx-auto px-4 py-3 flex items-center justify-between">
          <button 
            onClick={onBack}
            className="text-stone-400 hover:text-amber-400 transition-colors"
          >
            ← Back
          </button>
          <span className="text-amber-500 font-light">Settings</span>
          <div className="w-8" /> {/* Spacer for alignment */}
        </div>
      </header>

      <div className="max-w-lg mx-auto px-4 py-8 space-y-8">
        {/* Voice Selection */}
        <div className="space-y-4">
          <div>
            <h2 className="text-xl text-stone-200 font-light">Companion Voice</h2>
            <p className="text-sm text-stone-500">Who walks with you?</p>
          </div>
          
          <div className="space-y-2">
            {voiceOptions.map((v) => (
              <button
                key={v.id}
                onClick={() => onVoiceChange(v.id)}
                className={`w-full p-4 rounded-xl border transition-all text-left
                  ${voice === v.id 
                    ? 'bg-amber-950/50 border-amber-600/50' 
                    : 'bg-stone-900/50 border-stone-800 hover:border-stone-600'
                  }
                `}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className={`font-medium ${voice === v.id ? 'text-amber-200' : 'text-stone-300'}`}>
                      {v.label}
                    </div>
                    <div className="text-sm text-stone-500">
                      {v.description}
                    </div>
                  </div>
                  {voice === v.id && (
                    <span className="text-amber-500">✓</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Duration Selection */}
        <div className="space-y-4">
          <div>
            <h2 className="text-xl text-stone-200 font-light">Walk Duration</h2>
            <p className="text-sm text-stone-500">How long is your daily walk?</p>
          </div>
          
          <div className="space-y-2">
            {durationOptions.map((d) => (
              <button
                key={d.id}
                onClick={() => onDurationChange(d.id)}
                className={`w-full p-4 rounded-xl border transition-all text-left
                  ${duration === d.id 
                    ? 'bg-amber-950/50 border-amber-600/50' 
                    : 'bg-stone-900/50 border-stone-800 hover:border-stone-600'
                  }
                `}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className={`font-medium ${duration === d.id ? 'text-amber-200' : 'text-stone-300'}`}>
                      {d.label}
                    </div>
                    <div className="text-sm text-stone-500">
                      {d.description}
                    </div>
                  </div>
                  {duration === d.id && (
                    <span className="text-amber-500">✓</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Data Export */}
        <div className="space-y-4">
          <div>
            <h2 className="text-xl text-stone-200 font-light">Your Data</h2>
            <p className="text-sm text-stone-500">Everything stays on your device. Export anytime.</p>
          </div>
          
          <button
            onClick={() => {
              const data = localStorage.getItem('emmaus-state');
              if (data) {
                const blob = new Blob([data], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `emmaus-export-${new Date().toISOString().split('T')[0]}.json`;
                a.click();
              }
            }}
            className="w-full py-3 bg-stone-800 hover:bg-stone-700 text-stone-300 rounded-xl font-medium transition-all border border-stone-700"
          >
            Export My Walk Data (JSON)
          </button>
        </div>

        {/* Reset */}
        <div className="pt-8 border-t border-stone-800">
          <button
            onClick={onReset}
            className="w-full py-3 text-red-400 hover:text-red-300 transition-colors text-sm"
          >
            Start Over — Clear My Walk
          </button>
        </div>
      </div>
    </div>
  );
}
