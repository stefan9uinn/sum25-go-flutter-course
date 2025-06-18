const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function getHello() {
  const res = await fetch(`${BASE_URL}/api/hello/`);
  if (!res.ok) throw new Error("API call failed");
  return res.json();
}
