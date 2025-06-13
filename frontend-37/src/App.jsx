import { Button } from "./components/ui/Button";

export default function App() {
  return (
    <div>
      <Button style={{ width: 200 }} onClick={() => alert("salam bro")}>
        hello bro (ci/cd test)
      </Button>
    </div>
  );
}
