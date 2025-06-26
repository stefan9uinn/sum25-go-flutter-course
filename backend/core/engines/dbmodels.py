from dataclasses import dataclass


@dataclass
class DBInfo:
    name: str
    tables: list["TableInfo"]

    @staticmethod
    def from_fetchall_columns(db_name: str, columns: list[tuple]) -> "DBInfo":
        db = DBInfo(db_name, tables=[])
        for c in columns:
            for t in db.tables:
                if c[0] == t.name:
                    t.columns.append(ColumnInfo(c[1], c[2]))
                    break
            else:
                db.tables.append(TableInfo(
                    name=c[0], 
                    columns=[ColumnInfo(c[1], c[2])]
                ))
        return db
    
    def to_json(self) -> dict:
        return {
            "name": self.name,
            "tables": [table.to_json() for table in self.tables]
        }

    def __repr__(self) -> str:
        tables_str = ""
        for table in self.tables:
            table_str = str(table).replace('\n', '\n  ')
            tables_str += f"\n  {table_str}"
        return (
            f"Database {self.name}:  {tables_str}"
        )


@dataclass
class TableInfo:
    name: str
    columns: list["ColumnInfo"]

    def __repr__(self) -> str:
        columns_str = ""
        for column in self.columns:
            columns_str += f"\n  {column}"
        return (
            f"Table {self.name}:{columns_str}"
        )
    
    def to_json(self) -> dict:
        return {
            "name": self.name,
            "columns": [column.to_json() for column in self.columns]
        }


@dataclass
class ColumnInfo:
    name: str
    type: str

    def __repr__(self) -> str:
        return f"{self.name} - {self.type}"
    
    def to_json(self) -> dict:
        return {
            "name": self.name,
            "type": self.type
        }


@dataclass
class QueryResult:
    query: str
    rowcount: int
    data: list[tuple] | None
    execution_time: float

    def to_json(self) -> dict:
        return {
            "query": self.query,
            "rowcount": self.rowcount,
            "data": list(self.data) if self.data is not None else None,
            "execution_time": self.execution_time
        }
