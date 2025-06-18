import { useState } from "react";
import Schema from "./Schema";
import Tab from "./Tab";
import styles from "./SchemaWrapper.module.css";

export default function SchemaWrapper({ schemas }) {
  const [activeSchema, setActiveSchema] = useState(schemas[0]);
  return (
    <div>
      <div className={styles.tabs}>
        {schemas.map((schema) => (
          <Tab
            schema={schema}
            selected={schema == activeSchema}
            onClick={() => setActiveSchema(schema)}
          />
        ))}
      </div>
      <Schema schema={activeSchema} />
    </div>
  );
}
