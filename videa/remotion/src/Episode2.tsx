import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import data2 from "../../02-cechy-1357/scenes.json";
import durations2 from "../../02-cechy-1357/audio/durations.json";
import { fill, makeEpisode } from "./Episode";
import { Caption, INK, ORANGE, PAPER, Tag, Title, font, usePop } from "./Overlays";

const DIR = "02-cechy-1357";

// mlha přes obraz (S23)
export const Fog: React.FC<{ frames: number }> = ({ frames }) => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, frames], [-200, 200]);
  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(0deg, rgba(220,225,225,0.55) 0%, rgba(220,225,225,0.15) 45%, rgba(220,225,225,0) 70%)",
        transform: `translateX(${x}px) scaleX(1.4)`,
        mixBlendMode: "screen",
      }}
    />
  );
};

// zesilující světlo svítání (S39)
export const Sunrise: React.FC<{ frames: number }> = ({ frames }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, frames], [0, 0.45], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(ellipse 70% 60% at 30% 20%, rgba(255,190,110,1), rgba(255,190,110,0) 70%)",
        opacity: o,
        mixBlendMode: "screen",
      }}
    />
  );
};

// bílý záblesk na konci scény (S41)
export const FlashOut: React.FC<{ frames: number }> = ({ frames }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [frames - 20, frames - 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ background: "#fff", opacity: o }} />;
};

// tlačítka LIKE a ODEBÍRAT (S42)
export const Buttons: React.FC = () => {
  const p1 = usePop(20);
  const p2 = usePop(45);
  const btn = (text: string, bg: string, color: string, p: number, side: "left" | "right") => (
    <div
      style={{
        position: "absolute",
        top: 470,
        [side]: 150,
        fontFamily: font,
        fontWeight: 700,
        fontSize: 78,
        color,
        background: bg,
        padding: "16px 48px",
        borderRadius: 18,
        border: `7px solid ${INK}`,
        transform: `scale(${0.5 + 0.5 * p}) rotate(${side === "left" ? -4 : 4}deg)`,
        opacity: p,
      }}
    >
      {text}
    </div>
  );
  return (
    <AbsoluteFill>
      {btn("👍 LIKE", PAPER, INK, p1, "left")}
      {btn("ODEBÍRAT", ORANGE, INK, p2, "right")}
    </AbsoluteFill>
  );
};

export const NextEpisode: React.FC<{ text?: string }> = ({ text = "PŘÍŠTĚ: DOBA LEDOVÁ" }) => {
  const p = usePop(25);
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 90 }}>
      <div
        style={{
          fontFamily: font,
          fontWeight: 700,
          fontSize: 80,
          color: PAPER,
          background: INK,
          padding: "12px 44px",
          borderRadius: 8,
          borderBottom: `10px solid ${ORANGE}`,
          opacity: p,
          transform: `translateY(${(1 - p) * 40}px)`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// S37: verdikt složený ze tří hotových obrázků
export const makeVerdict = (dir: string, panels: { img: string; t: string }[]): React.FC<{ frames: number }> => () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: PAPER, flexDirection: "row", gap: 30, padding: "60px 40px", alignItems: "center" }}>
      {panels.map((p, i) => (
        <Panel key={p.t} {...p} dir={dir} delay={Math.round((0.6 + i * 2.6) * fps)} />
      ))}
    </AbsoluteFill>
  );
};
const Panel: React.FC<{ img: string; t: string; delay: number; dir: string }> = ({ img, t, delay, dir }) => {
  const p = usePop(delay);
  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 24, opacity: p, transform: `translateY(${(1 - p) * 60}px)` }}>
      <div style={{ fontFamily: font, fontWeight: 700, fontSize: 84, color: INK, textShadow: `5px 5px 0 ${ORANGE}` }}>{t}</div>
      <div style={{ width: "100%", aspectRatio: "9 / 12", overflow: "hidden", border: `8px solid ${INK}`, borderRadius: 14 }}>
        <Img src={staticFile(`${dir}/flow/${img}`)} style={{ ...fill, objectPosition: "50% 50%" }} />
      </div>
    </div>
  );
};

const Overlay2: React.FC<{ id: string; frames: number }> = ({ id, frames }) => {
  switch (id) {
    case "S01":
      return <Caption text="Čechy · 1357" delay={20} />;
    case "S03":
      return <Title text="ČECHY 1357" sub="Přežil bys ve středověku?" />;
    case "S04":
      return <Caption text="Karel IV. · král a císař" />;
    case "S06":
      return <Caption text="Katedrála dostavěna až 1929" delay={30} />;
    case "S12":
      return <Caption text="Pražský groš · ražen v Kutné Hoře" />;
    case "S18":
      return <Caption text="Brambory až v 18. století" delay={40} />;
    case "S23":
      return <Fog frames={frames} />;
    case "S25":
      return <Caption text="Dobytčí trh = dnešní Karlovo náměstí" delay={40} />;
    case "S27":
      return <Caption text="Juditin most: stržen povodní 1342" delay={60} />;
    case "S29":
      return <Tag text="LEGENDA" delay={20} style={{ right: 70, top: 70, fontSize: 52 }} />;
    case "S39":
      return <Sunrise frames={frames} />;
    case "S40":
      return <NextEpisode />;
    case "S41":
      return <FlashOut frames={frames} />;
    case "S42":
      return <Buttons />;
    default:
      return null;
  }
};

const ep2 = makeEpisode({
  dir: DIR,
  scenes: data2.scenes,
  durations: durations2 as Record<string, number>,
  Overlay: Overlay2,
  imageFor: { S01: "S01.png" }, // animace S01 ve Flow neprošla, jen obrázek
  Custom: { S37: makeVerdict(DIR, [{ img: "S11.png", t: "1. DEN" }, { img: "S16.png", t: "1. ZIMA" }, { img: "S28.png", t: "ROKY" }]) },
});
export const Episode2 = ep2.Component;
export const Episode2Visual = ep2.Visual;
export const episode2Frames = ep2.frames;
