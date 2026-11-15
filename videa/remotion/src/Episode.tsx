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
import data1 from "../../01-praha-1926/scenes.json";
import durations1 from "../../01-praha-1926/audio/durations.json";
import { Overlay as Overlay1, STATIC_IDS as STATIC1 } from "./Overlays";

// public-dir pro render je složka videa/, cesty k souborům mají předponu složky epizody
export const FPS = 30;
const GAP = 0.35; // pauza mezi scénami v naraci (s), stejná jako v tts.py
const FADE = 10; // prolínání mezi scénami (snímky)
const CLIP_SECONDS = 7.85; // délka klipů z Veo

export type Scene = { id: string; part: string; motion: { type: string } };
export type EpisodeConfig = {
  dir: string; // složka epizody, např. "01-praha-1926"
  scenes: Scene[];
  durations: Record<string, number>;
  Overlay: React.FC<{ id: string; frames: number }>;
  staticIds?: Set<string>; // scény bez pohybu kamery
  imageFor?: Record<string, string>; // náhradní obrázek pro scénu (cesta v rámci flow/)
  Custom?: Record<string, React.FC<{ frames: number }>>; // scény skládané celé v Remotionu
};

// pohyb kamery u statických obrázků: střídání směrů, aby se scény neopakovaly
const MOVES = [
  { from: [1.0, 0, 0], to: [1.1, 0, 0] }, // zoom in
  { from: [1.1, -30, 0], to: [1.1, 30, 0] }, // pan doprava
  { from: [1.12, 0, 0], to: [1.02, 0, 0] }, // zoom out
  { from: [1.1, 30, 10], to: [1.1, -30, -10] }, // pan doleva
];

export const KenBurns: React.FC<{ index: number; frames: number; children: React.ReactNode }> = ({
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

export const fill: React.CSSProperties = { width: "100%", height: "100%", objectFit: "cover" };

// animovaný klip: přehraje se (zpomalený nejvýš na 0,7×), pak drží poslední snímek s jemným zoomem
const ClipScene: React.FC<{ dir: string; id: string; frames: number }> = ({ dir, id, frames }) => {
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
        <Img src={staticFile(`${dir}/flow/last/${id}.png`)} style={fill} />
      ) : (
        <OffthreadVideo src={staticFile(`${dir}/flow/${id}.mp4`)} muted playbackRate={rate} style={fill} />
      )}
    </AbsoluteFill>
  );
};

export const makeEpisode = (cfg: EpisodeConfig) => {
  const timeline = (() => {
    let t = 0;
    return cfg.scenes.map((s) => {
      const start = Math.round(t * FPS);
      t += cfg.durations[s.id] + GAP;
      return { scene: s, start, frames: Math.round(t * FPS) - start };
    });
  })();
  const frames = timeline[timeline.length - 1].start + timeline[timeline.length - 1].frames + FPS;

  const SceneView: React.FC<{ scene: Scene; index: number; frames: number }> = ({ scene, index, frames }) => {
    const f = useCurrentFrame();
    const opacity = index === 0 ? 1 : interpolate(f, [0, FADE], [0, 1], { extrapolateRight: "clamp" });
    const C = cfg.Custom?.[scene.id];
    const img = staticFile(`${cfg.dir}/flow/${cfg.imageFor?.[scene.id] ?? scene.id + ".png"}`);
    const isClip = scene.motion.type === "veo" && !cfg.imageFor?.[scene.id];
    return (
      <AbsoluteFill style={{ opacity, backgroundColor: "#1d1a16" }}>
        {C ? (
          <C frames={frames} />
        ) : isClip ? (
          <ClipScene dir={cfg.dir} id={scene.id} frames={frames} />
        ) : cfg.staticIds?.has(scene.id) ? (
          <Img src={img} style={fill} />
        ) : (
          <KenBurns index={index} frames={frames}>
            <Img src={img} style={fill} />
          </KenBurns>
        )}
        <cfg.Overlay id={scene.id} frames={frames} />
      </AbsoluteFill>
    );
  };

  // obraz celého dílu (bez zvuku) – používá ho hlavní video i shorty
  const Visual: React.FC = () => (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
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
  );

  const Component: React.FC = () => {
    const { durationInFrames } = useVideoConfig();
    const f = useCurrentFrame();
    const endFade = interpolate(f, [durationInFrames - FPS, durationInFrames - 1], [1, 0], {
      extrapolateLeft: "clamp",
    });
    return (
      <AbsoluteFill style={{ backgroundColor: "#000" }}>
        <AbsoluteFill style={{ opacity: endFade }}>
          <Visual />
        </AbsoluteFill>
        <Audio src={staticFile(`${cfg.dir}/audio/mix.wav`)} />
      </AbsoluteFill>
    );
  };

  return { Component, Visual, frames, timeline };
};

const ep1 = makeEpisode({
  dir: "01-praha-1926",
  scenes: data1.scenes,
  durations: durations1 as Record<string, number>,
  Overlay: Overlay1,
  staticIds: STATIC1,
});
export const Episode = ep1.Component;
export const EpisodeVisual = ep1.Visual;
export const episodeFrames = ep1.frames;
