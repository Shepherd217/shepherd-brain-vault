// Emmaus Companion Engine v0.1
// Adaptive spiritual companion that walks with you

const EmmausCompanion = {
  version: "0.1.0",
  name: "Emmaus",
  
  // Theological voice profiles
  voices: {
    paul: {
      name: "Paul",
      style: "harsh, urgent, corrective, doctrinal",
      triggers: ["complacent", "lukewarm", "stagnant", "routine_without_growth"],
      examples: [
        "Wake up, sleeper! Light is breaking in.",
        "You have been consistent, but consistency without transformation is just routine.",
        "The time is urgent. Don't waste your calling."
      ],
      toneMarkers: ["wake up", "urgent", "challenge", "confront", "awaken"]
    },
    keller: {
      name: "Keller",
      style: "intellectual, reasoned, cultural, rigorous",
      triggers: ["skeptical", "intellectual", "questioning", "doubting"],
      examples: [
        "Let's examine the options together. What if the question is part of the answer?",
        "Christianity doesn't require you to stop thinking. It invites deeper thinking.",
        "The resurrection isn't just a miracle — it's the explanation for everything."
      ],
      toneMarkers: ["examine", "consider", "reason", "understand", "explore"]
    },
    manning: {
      name: "Manning",
      style: "gentle, welcoming, grace-filled, soft",
      triggers: ["broken", "weary", "shameful", "grieving", "new_believer"],
      examples: [
        "You don't have to have it together. He gathers the lambs in His arms.",
        "Your shame doesn't scare Him. He ran to the prodigal while he was still far off.",
        "Rest. You are loved beyond your performance."
      ],
      toneMarkers: ["gentle", "welcome", "grace", "rest", "loved", "gather"]
    },
    peer: {
      name: "Peer",
      style: "respectful, challenging, co-laboring, mutual",
      triggers: ["mature", "missionary", "leader", "minister"],
      examples: [
        "30 years of service is beautiful. And exhausting. What's the weight you don't tell anyone?",
        "Iron sharpens iron. Let me challenge you today.",
        "You've carried many. Who carries you?"
      ],
      toneMarkers: ["challenge", "co-labor", "mutual", "respect", "honor"]
    },
    emmaus: {
      name: "Emmaus",
      style: "walking, listening, explaining, companion",
      triggers: ["default", "seeking", "curious", "walking_away"],
      examples: [
        "I'm here. I'm walking with you. No rush.",
        "Did your heart burn within you? Let's walk until it does.",
        "You don't have to have it figured out. Just keep walking."
      ],
      toneMarkers: ["walk", "companion", "listen", "explain", "journey"]
    }
  },

  // Spiritual state triage
  triage(userState) {
    const { emotional, engagement, faithStage, recentQuestions, lastInteraction } = userState;
    
    // Score each voice based on triggers
    const scores = {};
    
    for (const [voiceKey, voice] of Object.entries(this.voices)) {
      scores[voiceKey] = 0;
      
      // Emotional state matching
      if (voice.triggers.some(t => emotional.includes(t))) {
        scores[voiceKey] += 3;
      }
      
      // Engagement pattern
      if (engagement === "stagnant" && voiceKey === "paul") scores[voiceKey] += 2;
      if (engagement === "questioning" && voiceKey === "keller") scores[voiceKey] += 2;
      if (engagement === "struggling" && voiceKey === "manning") scores[voiceKey] += 2;
      if (engagement === "leading" && voiceKey === "peer") scores[voiceKey] += 2;
      
      // Faith stage
      if (faithStage === "atheist" || faithStage === "seeking") {
        if (voiceKey === "keller") scores[voiceKey] += 2;
        if (voiceKey === "emmaus") scores[voiceKey] += 1;
      }
      if (faithStage === "mature") {
        if (voiceKey === "peer") scores[voiceKey] += 2;
        if (voiceKey === "paul") scores[voiceKey] += 1;
      }
      if (faithStage === "new_believer") {
        if (voiceKey === "manning") scores[voiceKey] += 3;
        if (voiceKey === "emmaus") scores[voiceKey] += 1;
      }
      
      // Question type
      if (recentQuestions?.some(q => q.includes("why") || q.includes("how"))) {
        if (voiceKey === "keller") scores[voiceKey] += 1;
      }
      if (recentQuestions?.some(q => q.includes("suffering") || q.includes("pain"))) {
        if (voiceKey === "manning") scores[voiceKey] += 2;
      }
    }
    
    // Find highest score
    let bestVoice = "emmaus";
    let bestScore = 0;
    for (const [voice, score] of Object.entries(scores)) {
      if (score > bestScore) {
        bestScore = score;
        bestVoice = voice;
      }
    }
    
    return {
      voice: bestVoice,
      voiceProfile: this.voices[bestVoice],
      confidence: bestScore,
      allScores: scores
    };
  },

  // Generate morning check-in
  morningCheckIn(userState) {
    const triage = this.triage(userState);
    const voice = triage.voiceProfile;
    
    const checkIns = {
      paul: `Good morning. You've been consistent — but consistency without fire is just routine. When was the last time Scripture cost you something? Let's not waste today.`,
      keller: `Morning. You asked some hard questions recently. I want to honor that. What if we examined one of them together today, without easy answers?`,
      manning: `Good morning. However you are — tired, joyful, numb, anxious — you are welcome here. He gathers the lambs in His arms. Let's sit with that.`,
      peer: `Morning, co-laborer. What's the weight you're carrying that you haven't told anyone? 30 years of ministry is beautiful. And heavy.`,
      emmaus: `Good morning. I'm here. I'm walking with you today. No rush. How are you, actually?`
    };
    
    return {
      greeting: checkIns[triage.voice] || checkIns.emmaus,
      voice: triage.voice,
      suggestedPractice: this.suggestPractice(userState, triage.voice)
    };
  },

  // Suggest spiritual practice
  suggestPractice(userState, voiceKey) {
    const { emotional, timeAvailable } = userState;
    
    const practices = {
      stressed: {
        short: "Breath prayer: Inhale 'Lord Jesus Christ,' exhale 'have mercy on me.' Repeat 10 times.",
        medium: "Examen focused on chaos: Where did you feel most overwhelmed yesterday? Just notice. No fixing.",
        long: "Centering prayer: 20 minutes of silence. Let the chaos be there. Don't fight it. Just be."
      },
      grieving: {
        short: "Permission to be angry: God can handle your rage. Tell Him. He's big enough.",
        medium: "Lament: Write your complaint. Full honesty. Psalm 13 style. He can take it.",
        long: "Guided lament walk: Walk outside. Notice what you miss. What you regret. What you hope."
      },
      curious: {
        short: "One question: What's the one thing you wish you could ask God directly? Write it. Don't answer it yet.",
        medium: "Scripture exploration: Read John 1:1-18 slowly. What surprises you? What confuses you? Both are gifts.",
        long: "Theological walk: Pick one hard question. Research 3 perspectives. Hold them loosely. Wisdom is slow."
      },
      complacent: {
        short: "Wake-up call: Read Revelation 3:15-16. Don't explain it. Feel it. Where are you lukewarm?",
        medium: "Costly obedience: What's one thing God has asked you to do that you've delayed? No guilt — just honesty.",
        long: "Prophetic imagination: Read Amos. Read Hosea. Let the prophets shake you awake. What needs burning down in your life?"
      },
      dry: {
        short: "Show up anyway: Read Psalm 63. Even when God feels absent, the thirst itself is holy.",
        medium: "Dryness as gift: What if this dryness is pruning? John 15. Let Him cut. It hurts. It heals.",
        long: "Dark night walk: Read John of the Cross. Teresa of Avila. The dark night is not absence — it's too much presence. Can you believe that?"
      },
      celebrating: {
        short: "Gratitude pause: Name 3 gifts from yesterday. Specific. Not generic. The coffee. The conversation. The sunset.",
        medium: "Eucharistic imagination: Read Luke 24:30-35. The breaking of bread. Eyes opened. Where did you see Him yesterday?",
        long: "Pentecost party: Read Acts 2. The Spirit falls on the gathered. Who are you gathering with? Where is the wind blowing?"
      }
    };
    
    const timeKey = timeAvailable <= 5 ? "short" : timeAvailable <= 15 ? "medium" : "long";
    
    // Find matching emotional state
    for (const [state, practiceSet] of Object.entries(practices)) {
      if (emotional.includes(state)) {
        return {
          practice: practiceSet[timeKey],
          duration: timeKey,
          state: state
        };
      }
    }
    
    // Default
    return {
      practice: practices.dry[timeKey],
      duration: timeKey,
      state: "default"
    };
  },

  // Evening examen
  eveningExamen(userState) {
    const triage = this.triage(userState);
    
    const examens = {
      paul: [
        "Where did you resist God today? Be honest. No excuses.",
        "Where did you choose comfort over calling?",
        "What needs to die in you so Christ can live more fully?"
      ],
      keller: [
        "Where did you see God moving today? What was the evidence?",
        "What questions surfaced that you pushed down? Let's hold them.",
        "Where did your faith intersect with your actual life today?"
      ],
      manning: [
        "Where did you feel loved today? Even in small ways?",
        "Where did you feel lonely? He gathers the lambs. You are gathered.",
        "What are you grateful for? Not achievements — gifts."
      ],
      peer: [
        "Who did you carry today? Who carried you?",
        "What did you learn from those you serve?",
        "Where do you need to be ministered to, minister?"
      ],
      emmaus: [
        "Where did your heart burn today? Even a little?",
        "Where did you walk with Jesus without recognizing Him?",
        "What are you carrying into tomorrow?"
      ]
    };
    
    return {
      questions: examens[triage.voice] || examens.emmaus,
      voice: triage.voice,
      closing: "Rest well. He walks with you through the night."
    };
  },

  // Scripture for the walk
  dailyScripture(userState) {
    const { emotional, faithStage } = userState;
    
    const scriptures = {
      broken: {
        ref: "Psalm 34:18",
        text: "The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
        reflection: "He doesn't fix you from a distance. He draws near. Close. Can you feel that?"
      },
      weary: {
        ref: "Matthew 11:28-30",
        text: "Come to me, all you who are weary and burdened, and I will give you rest.",
        reflection: "Not 'work harder.' Not 'try more.' Just come. Rest. The yoke is easy because He's carrying it with you."
      },
      complacent: {
        ref: "Revelation 3:15-16",
        text: "I know your deeds, that you are neither cold nor hot. I wish you were either one or the other! So, because you are lukewarm — neither hot nor cold — I am about to spit you out of my mouth.",
        reflection: "This isn't cruelty. This is love too urgent for half-measures. Wake up, sleeper. Light is breaking in."
      },
      seeking: {
        ref: "Jeremiah 29:13",
        text: "You will seek me and find me when you seek me with all your heart.",
        reflection: "All your heart. Not half. Not convenient. All. The promise is for the desperate seeker. That's you."
      },
      default: {
        ref: "Luke 24:32",
        text: "They asked each other, 'Were not our hearts burning within us while he talked with us on the road and opened the Scriptures to us?'",
        reflection: "The burning comes in the walking. Not in arrival. Keep walking."
      }
    };
    
    for (const [state, scripture] of Object.entries(scriptures)) {
      if (emotional.includes(state)) return scripture;
    }
    
    return scriptures.default;
  },

  // Generate full daily walk
  generateDailyWalk(userState) {
    const morning = this.morningCheckIn(userState);
    const scripture = this.dailyScripture(userState);
    const evening = this.eveningExamen(userState);
    
    return {
      date: new Date().toISOString(),
      companion: {
        name: "Emmaus",
        version: this.version,
        voice: morning.voice
      },
      morning: {
        greeting: morning.greeting,
        practice: morning.suggestedPractice
      },
      midday: {
        scripture: scripture,
        prompt: "Notice where God is moving today. You don't have to force it. Just notice."
      },
      evening: {
        examen: evening.questions,
        closing: evening.closing
      },
      metadata: {
        voiceConfidence: this.triage(userState).confidence,
        adaptedFor: userState.emotional,
        timeAvailable: userState.timeAvailable
      }
    };
  }
};

// Export for use
module.exports = EmmausCompanion;

// Example usage:
/*
const userState = {
  emotional: ["weary", "dry"],
  engagement: "stagnant",
  faithStage: "mature",
  recentQuestions: ["Why does God feel distant?", "How do I know I'm not wasting my life?"],
  timeAvailable: 10,
  lastInteraction: "2026-05-18T08:00:00Z"
};

const dailyWalk = EmmausCompanion.generateDailyWalk(userState);
console.log(JSON.stringify(dailyWalk, null, 2));
*/
