import { useEffect } from "react";
import { Streamlit } from "streamlit-component-lib";

function App() {
  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(0);

    const handleKeyDown = (event: KeyboardEvent) => {
      Streamlit.setComponentValue({
        key: event.key,
        meta: event.metaKey,
        ctrl: event.ctrlKey,
        shift: event.shiftKey,
      });
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return null;
}

export default App;