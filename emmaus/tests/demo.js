// Emmaus Companion — Interactive Demo
// Shows how the companion adapts to different spiritual states

const EmmausCompanion = require("../engine/companion");

console.log("\n" + "=".repeat(70));
console.log("  EMMAUS COMPANION — ADAPTIVE SPIRITUAL DIRECTION DEMO");
console.log("  " + "=".repeat(70) + "\n");

// Demo 1: The Broken
console.log("🕊️  DEMO 1: The Broken (Weary, grieving)\n");
const brokenUser = {
  emotional: ["broken", "weary"],
  engagement: "struggling",
  faithStage: "seeking",
  recentQuestions: ["Why does God allow suffering?", "Where is He in my pain?"],
  timeAvailable: 5,
  lastInteraction: "2026-05-17T08:00:00Z"
};

const brokenWalk = EmmausCompanion.generateDailyWalk(brokenUser);
console.log(`Companion Voice: ${brokenWalk.companion.voice.toUpperCase()}`);
console.log(`\n🌅 MORNING:`);
console.log(brokenWalk.morning.greeting);
console.log(`\n🙏 PRACTICE (${brokenWalk.morning.practice.duration}):`);
console.log(brokenWalk.morning.practice.practice);
console.log(`\n📖 MIDDAY SCRIPTURE:`);
console.log(`${brokenWalk.midday.scripture.ref}: "${brokenWalk.midday.scripture.text}"`);
console.log(`Reflection: ${brokenWalk.midday.scripture.reflection}`);
console.log(`\n🌙 EVENING EXAMEN:`);
brokenWalk.evening.examen.forEach((q, i) => console.log(`  ${i + 1}. ${q}`));
console.log(`\nClosing: ${brokenWalk.evening.closing}`);

// Demo 2: The Complacent
console.log("\n" + "=".repeat(70));
console.log("🔥 DEMO 2: The Complacent (Lukewarm, stagnant)\n");
const complacentUser = {
  emotional: ["complacent", "stagnant"],
  engagement: "routine",
  faithStage: "mature",
  recentQuestions: ["I read my Bible every day but I'm not growing"],
  timeAvailable: 10,
  lastInteraction: "2026-05-17T08:00:00Z"
};

const complacentWalk = EmmausCompanion.generateDailyWalk(complacentUser);
console.log(`Companion Voice: ${complacentWalk.companion.voice.toUpperCase()}`);
console.log(`\n🌅 MORNING:`);
console.log(complacentWalk.morning.greeting);
console.log(`\n🙏 PRACTICE (${complacentWalk.morning.practice.duration}):`);
console.log(complacentWalk.morning.practice.practice);
console.log(`\n📖 MIDDAY SCRIPTURE:`);
console.log(`${complacentWalk.midday.scripture.ref}: "${complacentWalk.midday.scripture.text}"`);
console.log(`Reflection: ${complacentWalk.midday.scripture.reflection}`);
console.log(`\n🌙 EVENING EXAMEN:`);
complacentWalk.evening.examen.forEach((q, i) => console.log(`  ${i + 1}. ${q}`));

// Demo 3: The Skeptic
console.log("\n" + "=".repeat(70));
console.log("🤔 DEMO 3: The Skeptic (Questioning, intellectual)\n");
const skepticUser = {
  emotional: ["curious", "questioning"],
  engagement: "questioning",
  faithStage: "atheist",
  recentQuestions: ["How can a good God exist with so much evil?", "What about other religions?"],
  timeAvailable: 15,
  lastInteraction: "2026-05-17T08:00:00Z"
};

const skepticWalk = EmmausCompanion.generateDailyWalk(skepticUser);
console.log(`Companion Voice: ${skepticWalk.companion.voice.toUpperCase()}`);
console.log(`\n🌅 MORNING:`);
console.log(skepticWalk.morning.greeting);
console.log(`\n🙏 PRACTICE (${skepticWalk.morning.practice.duration}):`);
console.log(skepticWalk.morning.practice.practice);
console.log(`\n📖 MIDDAY SCRIPTURE:`);
console.log(`${skepticWalk.midday.scripture.ref}: "${skepticWalk.midday.scripture.text}"`);
console.log(`Reflection: ${skepticWalk.midday.scripture.reflection}`);
console.log(`\n🌙 EVENING EXAMEN:`);
skepticWalk.evening.examen.forEach((q, i) => console.log(`  ${i + 1}. ${q}`));

// Demo 4: The Missionary
console.log("\n" + "=".repeat(70));
console.log("🌍 DEMO 4: The Veteran Missionary (Mature, exhausted)\n");
const missionaryUser = {
  emotional: ["tired", "heavy"],
  engagement: "leading",
  faithStage: "mature",
  recentQuestions: ["How do I keep going after 30 years?"],
  timeAvailable: 5,
  lastInteraction: "2026-05-17T08:00:00Z"
};

const missionaryWalk = EmmausCompanion.generateDailyWalk(missionaryUser);
console.log(`Companion Voice: ${missionaryWalk.companion.voice.toUpperCase()}`);
console.log(`\n🌅 MORNING:`);
console.log(missionaryWalk.morning.greeting);
console.log(`\n🙏 PRACTICE (${missionaryWalk.morning.practice.duration}):`);
console.log(missionaryWalk.morning.practice.practice);
console.log(`\n📖 MIDDAY SCRIPTURE:`);
console.log(`${missionaryWalk.midday.scripture.ref}: "${missionaryWalk.midday.scripture.text}"`);
console.log(`Reflection: ${missionaryWalk.midday.scripture.reflection}`);
console.log(`\n🌙 EVENING EXAMEN:`);
missionaryWalk.evening.examen.forEach((q, i) => console.log(`  ${i + 1}. ${q}`));

console.log("\n" + "=".repeat(70));
console.log("  Emmaus v0.1.0 — Formation, not information.");
console.log("  " + "=".repeat(70) + "\n");
