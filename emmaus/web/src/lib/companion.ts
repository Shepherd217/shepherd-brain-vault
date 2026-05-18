// Emmaus Companion Engine — Browser Version
// Adapts spiritual practices based on user's emotional state and archetype

export type Voice = 'manning' | 'paul' | 'keller' | 'peer' | 'emmaus';
export type Duration = 'brief' | 'normal' | 'extended';
export type Energy = 'drained' | 'tired' | 'neutral' | 'alert' | 'energized';

export interface UserState {
  archetype: Voice;
  energy: Energy;
  duration: Duration;
  dayOfWeek: number;
  liturgicalSeason?: string;
}

export interface Practice {
  title: string;
  content: string;
  scripture: Scripture;
  closing: string;
}

export interface Scripture {
  reference: string;
  text: string;
  context: string;
}

export interface DailyWalk {
  morning: MorningCheckIn;
  practice: Practice;
  scripture: Scripture;
  evening: EveningExamen;
}

export interface MorningCheckIn {
  greeting: string;
  energyPrompt: string;
  invitation: string;
}

export interface EveningExamen {
  prompt: string;
  gratitude: string;
  examen: string;
  release: string;
}

// Voice definitions
const voices: Record<Voice, { name: string; tone: string; approach: string }> = {
  manning: {
    name: 'Manning',
    tone: 'gentle, grace-filled, patient',
    approach: 'meets you in your exhaustion without demanding performance'
  },
  paul: {
    name: 'Paul',
    tone: 'urgent, corrective, loving challenge',
    approach: 'calls you back to first love without shaming'
  },
  keller: {
    name: 'Keller',
    tone: 'intellectual, culturally aware, reasoned',
    approach: 'explores questions with you, not for you'
  },
  peer: {
    name: 'Peer',
    tone: 'respectful, mutual, walking alongside',
    approach: 'honors your maturity while offering companionship'
  },
  emmaus: {
    name: 'Emmaus',
    tone: 'walking, listening, pursuing',
    approach: 'the default companion — warm, curious, present'
  }
};

// Scripture library with FULL CONTEXT
const scriptureLibrary: Record<string, Scripture> = {
  psalm23: {
    reference: 'Psalm 23',
    text: 'The Lord is my shepherd, I lack nothing. He makes me lie down in green pastures, he leads me beside quiet waters, he refreshes my soul. He guides me along the right paths for his name\'s sake. Even though I walk through the darkest valley, I will fear no evil, for you are with me; your rod and your staff, they comfort me. You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows. Surely your goodness and love will follow me all the days of my life, and I will dwell in the house of the Lord forever.',
    context: 'A psalm of David, written from the perspective of a shepherd-king who understood both vulnerability and divine care. Written for community worship, not private therapy.'
  },
  matthew11: {
    reference: 'Matthew 11:28-30',
    text: 'Come to me, all you who are weary and burdened, and I will give you rest. Take my yoke upon you and learn from me, for I am gentle and humble in heart, and you will find rest for your souls. For my yoke is easy and my burden is light.',
    context: 'Jesus speaks to people exhausted by religious performance and political oppression. The "yoke" was a rabbinic metaphor — Jesus offers his teaching as a lighter yoke than the Pharisees\'.'
  },
  luke24: {
    reference: 'Luke 24:13-35',
    text: 'Now that same day two of them were going to a village called Emmaus, about seven miles from Jerusalem. They were talking with each other about everything that had happened. As they talked and discussed these things with each other, Jesus himself came up and walked along with them; but they were kept from recognizing him... When he was at the table with them, he took bread, gave thanks, broke it and began to give it to them. Then their eyes were opened and they recognized him, and he disappeared from their sight. They asked each other, "Were not our hearts burning within us while he talked with us on the road and opened the Scriptures to us?"',
    context: 'The resurrected Jesus walks with discouraged disciples who have given up. He listens before speaking. He reveals himself in ordinary moments (breaking bread). The recognition comes in community, not isolation.'
  },
  philippians4: {
    reference: 'Philippians 4:6-7',
    text: 'Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.',
    context: 'Paul writes from prison to a church he loves. He does not dismiss anxiety — he redirects it toward prayer. The peace that follows is not the absence of problems but the presence of God.'
  },
  romans8: {
    reference: 'Romans 8:38-39',
    text: 'For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers, neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord.',
    context: 'The climax of Paul\'s argument about suffering and glory. Written to a persecuted church. This is not sentiment — it is defiant hope in the face of death.'
  },
  psalm46: {
    reference: 'Psalm 46',
    text: 'God is our refuge and strength, an ever-present help in trouble. Therefore we will not fear, though the earth give way and the mountains fall into the heart of the sea... He says, "Be still, and know that I am God; I will be exalted among the nations, I will be exalted in the earth."',
    context: 'A communal psalm of trust in chaos. The "be still" is not a meditation technique — it is a command to stop fighting and acknowledge God\'s sovereignty over geopolitical turmoil.'
  }
};

// Practice library
const practiceLibrary: Record<string, Practice[]> = {
  manning: [
    {
      title: 'Gentle Arrival',
      content: 'You don\'t have to perform for God. Not today. Not ever.\n\nTake three slow breaths. With each exhale, let something fall away — the need to be strong, the need to have answers, the need to be further along than you are.\n\nGod is not waiting for you to get better. God is here, in the "not better."',
      scripture: scriptureLibrary.psalm23,
      closing: 'You are held. Not because you earned it. Because that\'s who God is.'
    },
    {
      title: 'The Weight You Carry',
      content: 'Name one thing you\'re carrying that you were never meant to carry alone.\n\nIt might be grief. It might be a decision. It might be the belief that you should have figured this out by now.\n\nYou don\'t have to set it down yet. Just notice that you\'re carrying it. That\'s enough for now.',
      scripture: scriptureLibrary.matthew11,
      closing: 'Jesus invites the weary — not the sorted-out. You qualify.'
    }
  ],
  paul: [
    {
      title: 'First Love',
      content: 'When did you last feel alive in your faith? Not dutiful. Alive.\n\nThe gap between "alive" and "now" is not shame — it\'s information. It tells you what you\'re missing.\n\nOne question: What did you love about Jesus before you learned to be a Christian?',
      scripture: scriptureLibrary.romans8,
      closing: 'The love that held you then holds you now. Even — especially — when you can\'t feel it.'
    },
    {
      title: 'The Fire You Let Die',
      content: 'You\'ve been consistent. But consistency without fire is just routine.\n\nWhere did you stop risking? Where did you choose safety over surrender?\n\nThis is not shame. This is an invitation back to the edge — where faith actually happens.',
      scripture: scriptureLibrary.luke24,
      closing: 'The burning comes in the walking. Start walking.'
    }
  ],
  keller: [
    {
      title: 'The Question Beneath',
      content: 'What question are you actually asking?\n\nNot the one you say out loud. The one beneath it. The one that keeps you up at night.\n\nMaybe it\'s "Is God good?" Maybe it\'s "Am I lovable?" Maybe it\'s "What if I\'ve wasted my life?"\n\nWhatever it is, it\'s welcome here. The Christian tradition has been wrestling with hard questions for 2,000 years. You\'re not the first.',
      scripture: scriptureLibrary.philippians4,
      closing: 'The peace of God is not the absence of questions. It\'s the presence of God in the questioning.'
    }
  ],
  peer: [
    {
      title: 'The Road Behind, The Road Ahead',
      content: 'Thirty years of following Jesus is beautiful. And heavy.\n\nYou\'ve seen enough to know that faith is not a straight line. You\'ve buried friends. You\'ve buried certainty. You\'ve kept walking when the road went dark.\n\nThat\'s not nothing. That\'s everything.\n\nWhat are you carrying that needs to be shared? Not solved — shared.',
      scripture: scriptureLibrary.luke24,
      closing: 'The burning comes in the walking. And you\'ve been walking a long time.'
    }
  ],
  emmaus: [
    {
      title: 'Walking With You',
      content: 'You don\'t have to believe everything right now. You don\'t have to sort it all out.\n\nJust walk. Just show up. Just be honest about where you are.\n\nThe Holy Spirit walks with you — not ahead, not behind, but beside. And sometimes, in the ordinary moments, your eyes will open and you\'ll recognize that you were never alone.',
      scripture: scriptureLibrary.luke24,
      closing: 'Keep walking. The burning comes in the walking.'
    },
    {
      title: 'Be Still',
      content: 'The world is loud. Your thoughts are loud. Even your prayers can be loud — full of words, requests, performance.\n\nWhat if you stopped trying to make something happen?\n\nWhat if you just... were?\n\nGod is not waiting for your eloquence. God is waiting for your presence.',
      scripture: scriptureLibrary.psalm46,
      closing: 'Be still. And know.'
    }
  ]
};

// Generate daily walk based on user state
export function generateDailyWalk(state: UserState): DailyWalk {
  const voice = voices[state.archetype];
  const practice = selectPractice(state);
  const scripture = practice.scripture;
  
  return {
    morning: generateMorning(state, voice),
    practice,
    scripture,
    evening: generateEvening(state, voice)
  };
}

function selectPractice(state: UserState): Practice {
  const practices = practiceLibrary[state.archetype] || practiceLibrary.emmaus;
  // Simple selection: pick based on day of week for variety
  const index = state.dayOfWeek % practices.length;
  return practices[index];
}

function generateMorning(state: UserState, voice: typeof voices['emmaus']): MorningCheckIn {
  const greetings: Record<Energy, string> = {
    drained: `${voice.name}: You\'re here. That\'s enough.`,
    tired: `${voice.name}: Good morning. However you are — you\'re welcome.`,
    neutral: `${voice.name}: Good morning. Let\'s walk together today.`,
    alert: `${voice.name}: Good morning. I\'m glad you\'re here.`,
    energized: `${voice.name}: Good morning. Let\'s see what God has for us today.`
  };
  
  const energyPrompts: Record<Energy, string> = {
    drained: 'You feel empty. That\'s information, not failure.',
    tired: 'You\'re running on reserve. Let\'s be gentle today.',
    neutral: 'You\'re steady. Let\'s see what\'s beneath the surface.',
    alert: 'You\'re present. Let\'s go deep.',
    energized: 'You\'re awake. Let\'s use it well.'
  };
  
  return {
    greeting: greetings[state.energy],
    energyPrompt: energyPrompts[state.energy],
    invitation: 'How would you like to walk today?'
  };
}

function generateEvening(state: UserState, voice: typeof voices['emmaus']): EveningExamen {
  return {
    prompt: 'Where did you notice God today?\n\nIt might have been obvious — a conversation, a moment of peace, a surprise of beauty.\n\nOr it might have been subtle — a breath, a choice, a feeling you couldn\'t name.\n\nBoth count.',
    gratitude: 'What are you grateful for right now?\n\nNot "should be grateful." Actually grateful. Even if it\'s small. Even if it\'s mixed.',
    examen: 'What was heavy today?\n\nName it. Don\'t fix it. Just name it and set it down for the night.\n\nYou can pick it up tomorrow if you need to.',
    release: `${voice.name}: You\'re held. Not because you earned it. Because that\'s who God is.\n\nRest well.`
  };
}

// Utility: detect voice from archetype selection
export function detectVoice(archetype: string): Voice {
  switch (archetype) {
    case 'broken': return 'manning';
    case 'complacent': return 'paul';
    case 'skeptical': return 'keller';
    case 'mature': return 'peer';
    case 'seeking':
    default: return 'emmaus';
  }
}

// Utility: get liturgical season (simplified)
export function getLiturgicalSeason(): string {
  const month = new Date().getMonth();
  const day = new Date().getDate();
  
  // Simplified liturgical calendar
  if (month === 11 && day >= 25) return 'christmas';
  if (month === 0) return 'christmas';
  if (month === 1 || (month === 2 && day < 10)) return 'ordinary';
  if (month === 2 && day >= 10) return 'lent';
  if (month === 3) return 'lent';
  if (month === 4 && day <= 10) return 'easter';
  if (month === 4 && day > 10) return 'ordinary';
  if (month === 5) return 'ordinary';
  if (month === 6) return 'ordinary';
  if (month === 7) return 'ordinary';
  if (month === 8) return 'ordinary';
  if (month === 9) return 'ordinary';
  if (month === 10) return 'ordinary';
  if (month === 11 && day < 25) return 'advent';
  
  return 'ordinary';
}

// Default export for compatibility
export default {
  generateDailyWalk,
  detectVoice,
  getLiturgicalSeason,
  voices,
  scriptureLibrary
};
