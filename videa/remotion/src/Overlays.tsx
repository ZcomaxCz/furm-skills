import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

const INK = "#2a221a";
const PAPER = "#f3e9d6";
const ORANGE = "#ff7a1a";
const font = "'Oswald', 'Arial Narrow', sans-serif";

const usePop = (delay: number) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: f - delay, fps, config: { damping: 14, stiffness: 140 } });
};

const Title: React.FC = () => {
  const p = usePop(8);
  const p2 = usePop(22);
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 34 }}>
      <div
        style={{
          fontFamily: font,
          fontWeight: 700,
          fontSize: 150,
          letterSpacing: 6,
          color: INK,
          lineHeight: 1,
          transform: `scale(${0.6 + 0.4 * p})`,
          opacity: p,
          textShadow: `6px 6px 0 ${ORANGE}`,
        }}
      >
        PRAHA 1926
      </div>
      <div
        style={{
          fontFamily: font,
          fontWeight: 500,
          fontSize: 46,
          color: INK,
          marginTop: 8,
          opacity: p2,
          transform: `translateY(${(1 - p2) * 20}px)`,
        }}
      >
        Jak dlouho bys vydržel?
      </div>
    </AbsoluteFill>
  );
};

const Tag: React.FC<{ text: string; delay: number; style?: React.CSSProperties }> = ({
  text,
  delay,
  style,
}) => {
  const p = usePop(delay);
  return (
    <div
      style={{
        position: "absolute",
        fontFamily: font,
        fontWeight: 700,
        fontSize: 46,
        color: PAPER,
        background: INK,
        padding: "8px 26px",
        borderRadius: 6,
        borderLeft: `10px solid ${ORANGE}`,
        opacity: p,
        transform: `scale(${0.7 + 0.3 * p})`,
        ...style,
      }}
    >
      {text}
    </div>
  );
};

const MapLabels: React.FC = () => {
  const districts = ["Vinohrady", "Žižkov", "Smíchov", "Karlín"];
  return (
    <AbsoluteFill>
      <Tag text="VELKÁ PRAHA · 1922" delay={6} style={{ left: "calc(70px + var(--inset, 0px))", bottom: 150 }} />
      {districts.map((d, i) => (
        <Tag
          key={d}
          text={`+ ${d}`}
          delay={40 + i * 22}
          style={{ right: "calc(70px + var(--inset, 0px))", top: 120 + i * 95, fontSize: 40, fontWeight: 500 }}
        />
      ))}
    </AbsoluteFill>
  );
};

// S32: tři panely, čísla do horních pruhů (obrázek se v této scéně nehýbe)
const Verdict: React.FC = () => {
  const items = [
    { t: "1. DEN", x: 23, w: 602 },
    { t: "1. MĚSÍC", x: 653, w: 614 },
    { t: "ROKY", x: 1293, w: 605 },
  ];
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      {items.map((it, i) => (
        <VerdictLabel key={it.t} {...it} delay={Math.round((1.2 + i * 2.6) * fps)} />
      ))}
    </AbsoluteFill>
  );
};
const VerdictLabel: React.FC<{ t: string; x: number; w: number; delay: number }> = ({ t, x, w, delay }) => {
  const p = usePop(delay);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        width: w,
        top: 31,
        height: 117,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: font,
        fontWeight: 700,
        fontSize: 76,
        color: INK,
        opacity: p,
        transform: `scale(${0.6 + 0.4 * p})`,
      }}
    >
      {t}
    </div>
  );
};

const Caption: React.FC<{ text: string; delay?: number }> = ({ text, delay = 12 }) => (
  <Tag text={text} delay={delay} style={{ left: "calc(70px + var(--inset, 0px))", top: 70, fontSize: 40, fontWeight: 500 }} />
);

const NextEpisode: React.FC = () => {
  const p = usePop(20);
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
        PŘÍŠTĚ: STŘEDOVĚKÉ ČECHY
      </div>
    </AbsoluteFill>
  );
};

export const STATIC_IDS = new Set(["S32"]); // scény bez pohybu kamery (texty sedí na obrázek)

export const Overlay: React.FC<{ id: string; frames: number }> = ({ id }) => {
  switch (id) {
    case "S01":
      return <Caption text="Praha · 1926" delay={20} />;
    case "S03":
      return <Title />;
    case "S04":
      return <Caption text="Do roku 1939 se jezdí vlevo" delay={150} />;
    case "S07":
      return <Caption text="Československo · 8 let" />;
    case "S08":
      return <MapLabels />;
    case "S24":
      return <Caption text="Penicilin: až 1928" delay={30} />;
    case "S31":
      return <Caption text="VIII. všesokolský slet · 1926" delay={20} />;
    case "S32":
      return <Verdict />;
    case "S35":
      return <NextEpisode />;
    default:
      return null;
  }
};
