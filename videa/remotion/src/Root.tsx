import { Composition } from "remotion";
import { Episode, episodeFrames, FPS } from "./Episode";
import { Short, ShortProps, shortFrames } from "./Short";
import { Episode2, episode2Frames } from "./Episode2";
import { Episode3, episode3Frames } from "./Episode3";

// shorty z dílu: úseky v sekundách hlavního videa
const SHORTS: Record<string, ShortProps> = {
  "short-1-auto": { title: "V roce 1926 tě v Praze srazí auto ZPRAVA", segments: [{ from: 38.3, to: 74.7 }] },
  "short-2-karta": { title: "Zaplať kartou v Praze roku 1926", segments: [{ from: 142.99, to: 198.24 }] },
  "short-3-zachod": { title: "Jeden záchod pro celé patro", segments: [{ from: 244.65, to: 286.33 }] },
  "short-4-bacily": { title: "Největší zabiják Prahy 1926", segments: [{ from: 326.47, to: 370.55 }] },
  "e2-short-1-carodej": { episode: 2, title: "Ve středověku by tě měli za čaroděje", segments: [{ from: 79.54, to: 124.47 }] },
  "e2-short-2-brambory": { episode: 2, title: "Ve středověku nebyly brambory", segments: [{ from: 197.19, to: 231.54 }] },
  "e2-short-3-lazebnik": { episode: 2, title: "Středověký doktor? Lazebník.", segments: [{ from: 231.89, to: 283.75 }] },
  "e2-short-4-most": { episode: 2, title: "Karlův most a vejce v maltě?", segments: [{ from: 310.03, to: 345.58 }] },
  "e2-short-5-zabava": { episode: 2, title: "Středověký Netflix", segments: [{ from: 345.93, to: 387.94 }] },
  "e2-short-6-katedrala": { episode: 2, title: "Katedrálu sv. Víta stavěli 585 let", segments: [{ from: 39.45, to: 69.93 }] },
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
    <Composition
      id="Cechy1357"
      component={Episode2}
      durationInFrames={episode2Frames}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="DobaLedova"
      component={Episode3}
      durationInFrames={episode3Frames}
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
