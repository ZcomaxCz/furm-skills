import { Composition } from "remotion";
import { Episode, episodeFrames, FPS } from "./Episode";

export const Root: React.FC = () => (
  <Composition
    id="Praha1926"
    component={Episode}
    durationInFrames={episodeFrames}
    fps={FPS}
    width={1920}
    height={1080}
  />
);
