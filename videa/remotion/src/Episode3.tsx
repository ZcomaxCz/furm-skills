import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame } from "remotion";
import data3 from "../../03-doba-ledova/scenes.json";
import durations3 from "../../03-doba-ledova/audio/durations.json";
import { makeEpisode } from "./Episode";
import { Buttons, FlashOut, NextEpisode, makeVerdict } from "./Episode2";
import { Caption, INK, ORANGE, PAPER, Title, font, usePop } from "./Overlays";

const DIR = "03-doba-ledova";

// ---------- mapa střední Evropy v době ledové (S04) ----------
// zeměpisné souřadnice -> pixely (rovnoběžková projekce kolem 50° s. š.)
const W = 1920, H = 1080;
const LON0 = 0, LON1 = 30;
const SX = W / (LON1 - LON0); // px na stupeň délky
const SY = SX / 0.64; // stupeň šířky je delší (cos 50° ≈ 0,64)
const LAT0 = 45.0; // spodní okraj
const px = (lon: number, lat: number) => [(lon - LON0) * SX, H - (lat - LAT0) * SY] as const;
const path = (pts: [number, number][], close = true) =>
  pts.map(([lo, la], i) => `${i ? "L" : "M"}${px(lo, la).map((v) => v.toFixed(1)).join(" ")}`).join(" ") + (close ? " Z" : "");

// přibližná hranice Česka
const CZ: [number, number][] = [
  [12.1, 50.3], [12.5, 50.4], [13.0, 50.6], [14.3, 51.05], [14.8, 50.9], [15.0, 51.0], [16.3, 50.7],
  [17.0, 50.4], [17.7, 50.1], [18.6, 49.9], [18.8, 49.5], [18.0, 48.9], [17.2, 48.6], [16.9, 48.7],
  [16.0, 48.75], [15.0, 49.0], [14.7, 48.6], [13.8, 48.8], [13.0, 49.3], [12.4, 49.8],
];
// jižní okraj kontinentálního ledovce při posledním glaciálním maximu (zjednodušeně)
const ICE_EDGE: [number, number][] = [
  [1, 56.2], [4, 55.6], [7, 54.6], [9, 53.8], [10.5, 53.4], [12, 53.0], [13.5, 52.8], [14.5, 52.6],
  [16, 52.4], [17.5, 52.4], [19, 52.9], [20.5, 53.6], [22, 54.0], [24, 54.6], [30, 56.0],
];
const ICE: [number, number][] = [[-1, 56.5], ...ICE_EDGE, [31, 55.8], [31, 60], [-1, 60]];
// Alpy se zaledněním
const ALPS: [number, number][] = [
  [5.8, 45.2], [6.8, 46.4], [8.5, 46.9], [10.5, 47.3], [12.5, 47.5], [14.5, 47.6], [16.0, 47.6],
  [15.5, 46.8], [13.5, 46.5], [11.5, 46.3], [9.5, 46.0], [7.8, 45.6], [7.0, 44.7],
];
const DANUBE: [number, number][] = [
  [8.2, 47.9], [10, 48.5], [11.5, 48.75], [12.6, 48.9], [13.5, 48.55], [15.0, 48.3], [16.4, 48.2],
  [17.1, 48.1], [18.9, 47.8], [19.0, 46.5], [20.0, 45.3], [21.5, 44.8],
];
const ELBE: [number, number][] = [[15.6, 50.6], [15.2, 50.1], [14.5, 50.25], [14.2, 50.6], [13.6, 51.0], [12.5, 51.8], [11.5, 52.6], [10.5, 53.3], [9.8, 53.55]];
const VLTAVA: [number, number][] = [[13.9, 48.9], [14.4, 49.1], [14.35, 49.6], [14.42, 50.05], [14.45, 50.3]];

const IceMap: React.FC<{ frames: number }> = () => {
  const f = useCurrentFrame();
  const iceY = interpolate(f, [10, 70], [-700, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const cz = interpolate(f, [80, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const label = usePop(120);
  const peaks = usePop(170);
  const [kx, ky] = px(15.7, 50.75); // Krkonoše
  const [sx2, sy2] = px(13.5, 48.95); // Šumava
  const [ex, ey] = px(14.6, 52.6);
  const [cx, cy] = px(15.4, 49.75);
  return (
    <AbsoluteFill style={{ background: "#e8e3d3" }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%">
        <defs>
          <pattern id="grass" width="22" height="22" patternUnits="userSpaceOnUse">
            <circle cx="5" cy="6" r="1.6" fill="#b9b48f" />
            <circle cx="16" cy="15" r="1.3" fill="#c3be9b" />
          </pattern>
        </defs>
        <rect width={W} height={H} fill="#d9d3b6" />
        <rect width={W} height={H} fill="url(#grass)" />
        <path d={path(DANUBE, false)} stroke="#7fa6b4" strokeWidth={6} fill="none" strokeLinecap="round" />
        <path d={path(ELBE, false)} stroke="#7fa6b4" strokeWidth={5} fill="none" strokeLinecap="round" />
        <path d={path(VLTAVA, false)} stroke="#7fa6b4" strokeWidth={4} fill="none" strokeLinecap="round" />
        <path d={path(ALPS)} fill="#f4f8fa" stroke="#9fb8c2" strokeWidth={4} strokeLinejoin="round" />
        <path d={path(CZ)} fill={`rgba(255,122,26,${0.28 * cz})`} stroke={ORANGE} strokeWidth={7} strokeOpacity={cz} strokeLinejoin="round" />
        <g transform={`translate(0 ${iceY})`}>
          <path d={path(ICE)} fill="#fbfdff" stroke="#8fb3c4" strokeWidth={6} strokeLinejoin="round" />
          <path d={path(ICE_EDGE, false)} stroke="#c9dde6" strokeWidth={22} fill="none" strokeOpacity={0.6} />
        </g>
        {[[kx, ky], [sx2, sy2]].map(([x, y], i) => (
          <g key={i} transform={`translate(${x} ${y}) scale(${peaks})`}>
            <path d="M-34 18 L0 -30 L34 18 Z" fill="#fbfdff" stroke="#8fb3c4" strokeWidth={4} />
          </g>
        ))}
      </svg>
      <MapLabel x={px(15, 54.9)[0]} y={px(15, 54.9)[1]} text="LEDOVEC" p={interpolate(f, [60, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} big />
      <MapLabel x={cx} y={cy} text="ČECHY" p={cz} />
      <MapLabel x={px(10.5, 46.6)[0]} y={px(10.5, 46.6)[1]} text="ALPY" p={cz} small />
      <div style={{ position: "absolute", left: ex - 360, top: ey + 28, opacity: label, transform: `translateY(${(1 - label) * 20}px)` }}>
        <div style={{ fontFamily: font, fontWeight: 700, fontSize: 44, color: PAPER, background: INK, padding: "6px 20px", borderRadius: 6, borderLeft: `10px solid ${ORANGE}` }}>
          ▲ Tady ledovec končil
        </div>
      </div>
      <div style={{ position: "absolute", left: kx + 40, top: ky - 70, opacity: peaks, fontFamily: font, fontWeight: 500, fontSize: 34, color: INK }}>Krkonoše</div>
      <div style={{ position: "absolute", left: sx2 - 210, top: sy2 + 10, opacity: peaks, fontFamily: font, fontWeight: 500, fontSize: 34, color: INK }}>Šumava</div>
    </AbsoluteFill>
  );
};
const MapLabel: React.FC<{ x: number; y: number; text: string; p: number; big?: boolean; small?: boolean }> = ({ x, y, text, p, big, small }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      transform: `translate(-50%, -50%) scale(${0.8 + 0.2 * p})`,
      opacity: p,
      fontFamily: font,
      fontWeight: 700,
      fontSize: big ? 96 : small ? 40 : 58,
      letterSpacing: big ? 12 : 4,
      color: big ? "#6f97a8" : INK,
    }}
  >
    {text}
  </div>
);

// ---------- efekty ----------
const Snow: React.FC<{ frames: number; heavy?: boolean }> = ({ heavy }) => {
  const f = useCurrentFrame();
  const n = heavy ? 140 : 70;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {Array.from({ length: n }).map((_, i) => {
        const x0 = random(`x${i}`) * 2100 - 90;
        const speed = (heavy ? 7 : 3) + random(`s${i}`) * (heavy ? 6 : 3);
        const drift = heavy ? 9 : 2;
        const size = 4 + random(`r${i}`) * (heavy ? 9 : 6);
        const y = ((random(`y${i}`) * 1200 + f * speed) % 1200) - 60;
        const x = x0 + (f * drift) % 2100 - (heavy ? 300 : 0) + Math.sin((f + i * 13) / 18) * 12;
        return <div key={i} style={{ position: "absolute", left: ((x % 2100) + 2100) % 2100 - 90, top: y, width: size, height: size, borderRadius: "50%", background: "rgba(255,255,255,0.85)" }} />;
      })}
    </AbsoluteFill>
  );
};

const FireGlow: React.FC = () => {
  const f = useCurrentFrame();
  const o = 0.22 + 0.1 * Math.sin(f / 4) + 0.06 * Math.sin(f / 1.7);
  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(ellipse 35% 40% at 52% 72%, rgba(255,150,60,1), rgba(255,150,60,0) 70%)",
        opacity: o,
        mixBlendMode: "screen",
      }}
    />
  );
};

const DarkenOut: React.FC<{ frames: number }> = ({ frames }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [frames * 0.4, frames], [0, 0.35], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ background: "#061424", opacity: o }} />;
};

const Overlay3: React.FC<{ id: string; frames: number }> = ({ id, frames }) => {
  switch (id) {
    case "S01":
      return <Caption text="Doba ledová · před 27 000 lety" delay={20} />;
    case "S03":
      return <Title text="DOBA LEDOVÁ" sub="" />;
    case "S06":
      return <Caption text="Tady bude jednou Praha" delay={40} />;
    case "S12":
      return <Caption text="Neandrtálci vymřeli před 40 000 lety" delay={40} />;
    case "S18":
      return <FireGlow />;
    case "S27":
      return <Snow frames={frames} heavy />;
    case "S31":
      return <Caption text="Dolní Věstonice · Pavlov" delay={30} />;
    case "S32":
      return <Caption text="Věstonická venuše · cca 29 000 let" delay={60} />;
    case "S35":
      return <Caption text="Eduard Štorch: Lovci mamutů (1918)" delay={40} />;
    case "S36":
      return <DarkenOut frames={frames} />;
    case "S39":
      return <NextEpisode text="PŘÍŠTĚ: KELTOVÉ" />;
    case "S40":
      return <FlashOut frames={frames} />;
    case "S41":
      return <Buttons />;
    case "S02":
    case "S07":
      return <Snow frames={frames} />;
    default:
      return null;
  }
};

const ep3 = makeEpisode({
  dir: DIR,
  scenes: data3.scenes,
  durations: durations3 as Record<string, number>,
  Overlay: Overlay3,
  imageFor: { S18: "S18.png", S27: "S27.png", S34: "S30.png" }, // animace chybí / obsahuje chybu
  Custom: {
    S04: IceMap,
    S37: makeVerdict(DIR, [
      { img: "S36.png", t: "1. NOC" },
      { img: "S24.png", t: "1. LOV" },
      { img: "S27.png", t: "1. ZIMA" },
    ]),
  },
});
export const Episode3 = ep3.Component;
export const Episode3Visual = ep3.Visual;
export const episode3Frames = ep3.frames;
