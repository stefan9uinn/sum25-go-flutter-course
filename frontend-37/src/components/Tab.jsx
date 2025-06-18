import styles from "./Tab.module.css";

export default function Tab({ schema, selected, onClick }) {
  return (
    <div className={selected && styles.selected} onClick={onClick}>
      {schema.name}
    </div>
  );
}
