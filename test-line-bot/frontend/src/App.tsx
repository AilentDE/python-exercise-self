import "./App.css";

import LogoShowing from "./components/LogoShowing";
import LineLoginSection from "./components/LineLoginSection";
import LineLiffSection from "./components/LineLiffSection";

function App() {
  return (
    <>
      <LogoShowing />

      <LineLoginSection />
      <div style={{ height: "2rem" }} />
      <LineLiffSection />
    </>
  );
}

export default App;
