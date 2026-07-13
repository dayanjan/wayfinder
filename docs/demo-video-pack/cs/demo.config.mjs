// CS-native demo — config. Drives file:// slide assets + the LIVE Claude Science UI
// (saved-session auth via STORAGE_STATE), screen-only, scene-timed to Brian narration.
// 1920x1080. New spine: LBD-in-CS to test implicit hypotheses. See ./README.md.
// Supersedes ../demo.config.mjs (the Streamlit cut, kept as fallback recipe).

export const BASE = "http://localhost:8000/";   // CS home — VERIFY the port Friday: `claude-science status`
export const ENV_FILE = process.env.ELEVENLABS_ENV_FILE; // ElevenLabs key
export const VIEWPORT = { width: 1920, height: 1080 };

// CS authenticates via a saved browser session (nonce-minted), NOT a login form.
// record.mjs injects this as the context storageState. Pair with actor.user:"" to skip login.
// PRE-FLIGHT Friday: refresh this by running the drive-claude-science tracer once (auth can expire).
export const STORAGE_STATE = process.env.CS_STORAGE_STATE;

export const VOICE = "en-US-AndrewMultilingualNeural"; // draft edge-tts (unused when TTS.mode=elevenlabs)
export const RATE = "-4%";
export const MODE = "single";

export const ACTORS = { walk: { user: "" } };   // no login; storageState carries CS auth

export const LOGIN = {
  loggedIn: async (page) => /Claude Science/i.test(await page.title().catch(() => "")),
};

// FINAL cut — ElevenLabs "Brian" (draft = { mode:"edge" }).
export const TTS = {
  mode: "elevenlabs",
  elevenVoiceId: "HgYyghnaV40lVlip9yo7",   // author's own cloned voice (first-person narration)
  elevenModelId: "eleven_multilingual_v2",
  elevenVoiceSettings: { stability: 0.5, similarity_boost: 0.75, style: 0.0, use_speaker_boost: true },
  keyEnvFile: ENV_FILE,
  keyVar: "ELLEVENLABS_API_KEY",
};

export const TRANSCRIBE = { mode: "local", localModel: "small.en", openaiModel: "whisper-1", threshold: 0.5 };

export const STITCH = {
  out: "out/pyzobot_arbiter_cs_demo.mp4",
  theme: { bg: "#091314", fg: "#eaf3f1", accent: "#26c6c9" },
  cards: {
    title:  { voiced: true, eyebrow: "Wayfinder",
              title: "The library and the lab, on one bench",
              sub: "Literature-based discovery, built inside Claude Science" },
    endcap: { voiced: true, eyebrow: "Wayfinder",
              title: "Generate a hypothesis. Test it. One platform.",
              sub: "Dr. Shanaka Wijesinghe · VCU School of Pharmacy · linkedin.com/in/dayanjanwijesinghe" },
  },
  order: [
    { card: "title" },
    { turn: "walk" },
    { card: "endcap" },
  ],
};
