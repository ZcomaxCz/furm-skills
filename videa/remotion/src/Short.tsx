import {
  AbsoluteFill,
  Audio,
  Series,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import cues1 from "../../01-praha-1926/titulky.json";
import cues2 from "../../02-cechy-1357/titulky.json";
import { EpisodeVisual, FPS } from "./Episode";
import { Episode2Visual } from "./Episode2";

type Cue = { start: number; end: number; text: string };
const EPISODES: Record<number, { Visual: React.FC; cues: Cue[]; dir: string; label: string }> = {
  1: { Visual: EpisodeVisual, cues: cues1 as Cue[], dir: "01-praha-1926", label: "PRAHA 1926" },
  2: { Visual: Episode2Visual, cues: cues2 as Cue[], dir: "02-cechy-1357", label: "ČECHY 1357" },
};

// úseky v sekundách času hlavního videa
export type Segment = { from: number; to: number };
export type ShortProps = { title: string; segments: Segment[]; episode?: number };

const INK = "#2a221a";
const PAPER = "#f3e9d6";
const ORANGE = "#ff7a1a";
const font = "'Oswald', 'Arial Narrow', sans-serif";
const PAD = 0.25; // přesah na začátku a konci úseku (s)
const END_CARD = 2; // s

const segStart = (s: Segment) => Math.max(0, s.from - PAD);
const segFrames = (s: Segment) => Math.round((s.to + PAD - segStart(s)) * FPS);
export const shortFrames = (p: ShortProps) =>
  p.segments.reduce((a, s) => a + segFrames(s), 0) + END_CARD * FPS;

// 16:9 obraz uprostřed (mírně oříznutý do stran), za ním rozmazaná kopie přes celou výšku
const FG_W = 1400; // šířka popředí (zbytek se ořízne)
const FG_H = Math.round((FG_W * 9) / 16);
const FG_TOP = 560;

const Frame: React.FC<{ seg: Segment; ep: number }> = ({ seg, ep }) => {
  const E = EPISODES[ep];
  const offset = Math.round(segStart(seg) * FPS);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ filter: "blur(40px) brightness(0.55)", transform: "scale(1.2)" }}>
        <div style={{ position: "absolute", width: 1920, height: 1080, left: (1080 - 3413) / 2, top: 0, transform: "scale(1.778)", transformOrigin: "top left" }}>
          <Sequence from={-offset} layout="none">
            <E.Visual />
          </Sequence>
        </div>
      </AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: (1080 - FG_W) / 2,
          top: FG_TOP,
          width: FG_W,
          height: FG_H,
          overflow: "hidden",
          boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
        }}
      >
        <div style={{ width: 1920, height: 1080, transform: `scale(${FG_W / 1920})`, transformOrigin: "top left", ["--inset" as string]: "230px" } as React.CSSProperties}>
          <Sequence from={-offset} layout="none">
            <E.Visual />
          </Sequence>
        </div>
      </div>
      <Audio src={staticFile(`${E.dir}/audio/mix.wav`)} trimBefore={offset} />
      <Captions seg={seg} cues={E.cues} />
    </AbsoluteFill>
  );
};

// titulky pod obrazem, jen ty, které patří do úseku
const Captions: React.FC<{ seg: Segment; cues: Cue[] }> = ({ seg, cues }) => {
  const f = useCurrentFrame();
  const t = segStart(seg) + f / FPS;
  const cue = cues.find(
    (c) => t >= c.start && t <= c.end + 0.04 && c.end > seg.from && c.start < seg.to
  );
  if (!cue) return null;
  const local = (t - cue.start) * FPS;
  const pop = interpolate(local, [0, 5], [0.9, 1], { extrapolateRight: "clamp" });
  return (
    <div
      style={{
        position: "absolute",
        top: FG_TOP + FG_H + 70,
        left: 60,
        right: 60,
        textAlign: "center",
        fontFamily: font,
        fontWeight: 700,
        fontSize: 66,
        lineHeight: 1.18,
        color: PAPER,
        textShadow: `0 4px 0 ${INK}, 0 0 18px rgba(0,0,0,0.8)`,
        transform: `scale(${pop})`,
      }}
    >
      {cue.text}
    </div>
  );
};

const Title: React.FC<{ text: string }> = ({ text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: f - 3, fps, config: { damping: 14 } });
  return (
    <div style={{ position: "absolute", top: 150, left: 50, right: 50, display: "flex", justifyContent: "center" }}>
      <div
        style={{
          fontFamily: font,
          fontWeight: 700,
          fontSize: 78,
          lineHeight: 1.12,
          textAlign: "center",
          color: INK,
          background: PAPER,
          padding: "18px 36px",
          borderRadius: 10,
          borderBottom: `12px solid ${ORANGE}`,
          transform: `scale(${0.8 + 0.2 * p})`,
          opacity: p,
        }}
      >
        {text}
      </div>
    </div>
  );
};

const EndCard: React.FC<{ label: string }> = ({ label }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: INK, opacity: o, justifyContent: "center", alignItems: "center", gap: 30 }}>
      <div style={{ fontFamily: font, fontWeight: 700, fontSize: 120, color: PAPER, textShadow: `6px 6px 0 ${ORANGE}` }}>{label}</div>
      <div style={{ fontFamily: font, fontWeight: 500, fontSize: 60, color: PAPER }}>Celé video na kanálu ▶</div>
    </AbsoluteFill>
  );
};

export const Short: React.FC<ShortProps> = ({ title, segments, episode = 1 }) => (
  <AbsoluteFill style={{ backgroundColor: INK }}>
    <Series>
      {segments.map((s, i) => (
        <Series.Sequence key={i} durationInFrames={segFrames(s)}>
          <Frame seg={s} ep={episode} />
        </Series.Sequence>
      ))}
      <Series.Sequence durationInFrames={END_CARD * FPS}>
        <EndCard label={EPISODES[episode].label} />
      </Series.Sequence>
    </Series>
    <Sequence durationInFrames={shortFrames({ title, segments }) - END_CARD * FPS} layout="none">
      <Title text={title} />
    </Sequence>
  </AbsoluteFill>
);
