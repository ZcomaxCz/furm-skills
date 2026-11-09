import { Composition } from "remotion";
import { Episode, episodeFrames, FPS } from "./Episode";
import { Short, ShortProps, shortFrames } from "./Short";

// shorty z dílu: úseky v sekundách hlavního videa
const SHORTS: Record<string, ShortProps> = {
  "short-1-auto": { title: "V roce 1926 tě v Praze srazí auto ZPRAVA", segments: [{ from: 38.3, to: 74.7 }] },
  "short-2-karta": { title: "Zaplať kartou v Praze roku 1926", segments: [{ from: 142.99, to: 198.24 }] },
  "short-3-zachod": { title: "Jeden záchod pro celé patro", segments: [{ from: 244.65, to: 286.33 }] },
  "short-4-bacily": { title: "Největší zabiják Prahy 1926", segments: [{ from: 326.47, to: 370.55 }] },
  "short-5-mlcet": {
    title: "Dokázal bys mlčet?",
    segments: [
      { from: 0, to: 14.76 },
      { from: 454.6, to: 477.63 },
    ],
  },
};

export const Root: React.FC = () => (
  <>
    <Composition
      id="Praha1926"
      component={Episode}
      durationInFrames={episodeFrames}
      fps={FPS}
      width={1920}
      height={1080}
    />
    {Object.entries(SHORTS).map(([id, props]) => (
      <Composition
        key={id}
        id={id}
        component={Short}
        defaultProps={props}
        durationInFrames={shortFrames(props)}
        fps={FPS}
        width={1080}
        height={1920}
      />
    ))}
  </>
);
