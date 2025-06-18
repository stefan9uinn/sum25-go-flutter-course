import { PlaygroundBar } from "../components/PlaygroundBar";
import TableSchema from "../components/TableSchema";

export default function Playground() {
  const schema = {
    name: "test",
    columns: [
      {
        name: "id",
        type: "SERIAL",
        attrs: "PRIMARY KEY",
      },
      {
        name: "name",
        type: "VARCHAR(30)",
        attrs: "NOT NULL",
      },
      {
        name: "age",
        type: "INTEGER",
        attrs: "DEFAULT 18",
      },
    ],
  };

  return (
    <div>
      <PlaygroundBar />
      <div className="mono">
        <TableSchema schema={schema} />
      </div>
    </div>
  );
}
