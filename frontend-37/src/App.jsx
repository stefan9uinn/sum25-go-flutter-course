import { Button } from "./components/ui/Button";

export default function App() {
  return (
    <div>
      <Button
        style={{ width: 100 }}
        onClick={() => alert("salam bro real good")}
      >
        hello bro check out my ci/cd
      </Button>
    </div>
  );
}

