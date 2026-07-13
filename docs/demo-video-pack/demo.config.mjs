// demo-video PACK — demo.config.mjs  (PyZoBot Arbiter — the Researcher's Workbench)
// Single actor, NO auth (the app is open on localhost). user:"" => login is skipped.

export const BASE = "http://localhost:8501/";
export const ENV_FILE = process.env.ELEVENLABS_ENV_FILE; // ElevenLabs key (final pass)
export const VIEWPORT = { width: 1920, height: 1080 };

// draft voice (edge-tts); flip TTS.mode to elevenlabs for the final cut
export const VOICE = "en-US-AndrewMultilingualNeural";
export const RATE = "-4%";

export const MODE = "single";

export const ACTORS = {
  walk: { user: "" },   // no login — the scene navigates to BASE itself
};

// login is skipped (user:""), but keep a sane landmark check
export const LOGIN = {
  loggedIn: async (page) =>
    (await page.getByRole("button", { name: "Adjudicate", exact: true }).count().catch(() => 0)) > 0,
};

// TTS backend: FINAL cut — ElevenLabs "Brian". (Draft was { mode: "edge" }.)
export const TTS = {
  mode: "elevenlabs",
  elevenVoiceId: "nPczCjzI2devNBz1zQrb",   // Brian — deep, resonant narrator
  elevenModelId: "eleven_multilingual_v2",
  elevenVoiceSettings: { stability: 0.5, similarity_boost: 0.75, style: 0.0, use_speaker_boost: true },
  keyEnvFile: ENV_FILE,
  keyVar: "ELLEVENLABS_API_KEY",
};

export const TRANSCRIBE = { mode: "local", localModel: "small.en", openaiModel: "whisper-1", threshold: 0.5 };

export const STITCH = {
  out: "out/pyzobot_arbiter_demo.mp4",
  theme: { bg: "#091314", fg: "#eaf3f1", accent: "#26c6c9" },
  cards: {
    title:  { voiced: true, eyebrow: "PyZoBot Arbiter", title: "The Hypothesis Referee",
              sub: "Receipt-backed. Willing to refute." },
    endcap: { voiced: true, eyebrow: "PyZoBot Arbiter", title: "A confident, receipt-backed verdict",
              sub: "Reproducible from public Perturb-seq data" },
  },
  order: [
    { card: "title" },
    { turn: "walk" },
    { card: "endcap" },
  ],
};
