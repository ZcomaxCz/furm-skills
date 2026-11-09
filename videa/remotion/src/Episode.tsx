import "@fontsource/oswald/500.css";
import "@fontsource/oswald/700.css";
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import data from "../../01-praha-1926/scenes.json";
import durations from "../../01-praha-1926/audio/durations.json";
import { Overlay, STATIC_IDS } from "./Overlays";

export const FPS = 30;
const GAP = 0.35; // pauza mezi scénami v naraci (s), stejná jako v tts.py
const FADE = 10; // prolínání mezi scénami (snímky)
const CLIP_SECONDS = 7.85; // délka klipů z Veo

type Scene = (typeof data.scenes)[number];
const durs = durations as Record<string, number>;

// začátky a délky scén ve snímcích podle narace
const timeline = (() => {
  let t = 0;
  return data.scenes.map((s) => {
    const start = Math.round(t * FPS);
    t += durs[s.id] + GAP;
    return { scene: s, start, frames: Math.round(t * FPS) - start };
  });
})();
export const episodeFrames = timeline.at(-1)!.start + timeline.at(-1)!.frames + FPS; // +1 s na konec

// pohyb kamery u statických obrázků: střídání směrů, aby se scény neopakovaly
const MOVES = [
  { from: [1.0, 0, 0], to: [1.1, 0, 0] }, // zoom in
  { from: [1.1, -30, 0], to: [1.1, 30, 0] }, // pan doprava
  { from: [1.12, 0, 0], to: [1.02, 0, 0] }, // zoom out
  { from: [1.1, 30, 10], to: [1.1, -30, -10] }, // pan doleva
];

const KenBurns: React.FC<{ index: number; frames: number; children: React.ReactNode }> = ({
  index,
  frames,
  children,
}) => {
  const f = useCurrentFrame();
  const m = MOVES[index % MOVES.length];
  const p = interpolate(f, [0, frames], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  const s = m.from[0] + (m.to[0] - m.from[0]) * p;
  const x = m.from[1] + (m.to[1] - m.from[1]) * p;
  const y = m.from[2] + (m.to[2] - m.from[2]) * p;
  return (
    <AbsoluteFill style={{ transform: `scale(${s}) translate(${x}px, ${y}px)` }}>{children}</AbsoluteFill>
  );
};

const fill: React.CSSProperties = { width: "100%", height: "100%", objectFit: "cover" };

// animovaný klip: přehraje se (zpomalený nejvýš na 0,7×), pak drží poslední snímek s jemným zoomem
const ClipScene: React.FC<{ id: string; frames: number }> = ({ id, frames }) => {
  const f = useCurrentFrame();
  const sceneSec = frames / FPS;
  const rate = Math.max(0.7, Math.min(1, CLIP_SECONDS / sceneSec));
  const clipFrames = Math.floor((CLIP_SECONDS / rate) * FPS) - 2;
  const hold = f >= clipFrames;
  const zoom = hold
    ? interpolate(f, [clipFrames, frames], [1, 1.06], { extrapolateRight: "clamp" })
    : 1;
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
      {hold ? (
        <Img src={staticFile(`flow/last/${id}.png`)} style={fill} />
      ) : (
        <OffthreadVideo src={staticFile(`flow/${id}.mp4`)} muted playbackRate={rate} style={fill} />
      )}
    </AbsoluteFill>
  );
};

const SceneView: React.FC<{ scene: Scene; index: number; frames: number }> = ({
  scene,
  index,
  frames,
}) => {
  const f = useCurrentFrame();
  const opacity = index === 0 ? 1 : interpolate(f, [0, FADE], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity, backgroundColor: "#1d1a16" }}>
      {scene.motion.type === "veo" ? (
        <ClipScene id={scene.id} frames={frames} />
      ) : STATIC_IDS.has(scene.id) ? (
        <Img src={staticFile(`flow/${scene.id}.png`)} style={fill} />
      ) : (
        <KenBurns index={index} frames={frames}>
          <Img src={staticFile(`flow/${scene.id}.png`)} style={fill} />
        </KenBurns>
      )}
      <Overlay id={scene.id} frames={frames} />
    </AbsoluteFill>
  );
};

export const Episode: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  const f = useCurrentFrame();
  const endFade = interpolate(f, [durationInFrames - FPS, durationInFrames - 1], [1, 0], {
    extrapolateLeft: "clamp",
  });
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill style={{ opacity: endFade }}>
        {timeline.map(({ scene, start, frames }, i) => {
          const from = i === 0 ? 0 : start - FADE;
          const len = frames + (i === 0 ? 0 : FADE) + (i === timeline.length - 1 ? FPS : 0);
          return (
            <Sequence key={scene.id} from={from} durationInFrames={len} name={scene.id}>
              <SceneView scene={scene} index={i} frames={len} />
            </Sequence>
          );
        })}
      </AbsoluteFill>
      <Audio src={staticFile("audio/mix.wav")} />
    </AbsoluteFill>
  );
};
