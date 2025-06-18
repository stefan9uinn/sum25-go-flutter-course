import styles from "./TableSchema.module.css";

/**
 * @typedef {Object} Column
 * @property {string} name
 * @property {string} type
 * @property {string} attrs
 */

/**
 * @typedef {Object} Props
 * @property {string} name
 * @property {Column[]} columns
 */

/**
 * @param {{ schema: Props }} props
 */
export default function TableSchema({ schema }) {
  return (
    <div className={styles.wrapper}>
      {schema.columns.map((col) => (
        <div className={styles.item} key={col.name}>
          {col.name} {col.type} {col.attrs}
        </div>
      ))}
    </div>
  );
}
