import { act } from "react";

const BASE_URL = process.env.REACT_APP_API_URL || "";

export async function getCode(text, id) {
  const res = await fetch(`${BASE_URL}/db/chroma/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code: text, user_id: id, action: 'execute' }),
  });
  if (!res.ok) {
    return "Error";
  };
  return res.json();
}

export async function getIState(id) {
  const res = await fetch(`${BASE_URL}/db/chroma/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: id, action: 'state' }),
  });
  if (!res.ok) throw new Error("API call failed");
  return res.json();
}

export async function getPostgresTable(id) {
  const res = await fetch(`${BASE_URL}/db/schema/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: id }),
  });
  if (!res.ok) throw new Error("API call failed");
  return res.json();
}

export async function createPostgresTable(id) {
  const res = await fetch(`${BASE_URL}/db/put/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: id }),
  });
  if (!res.ok) throw new Error("API call failed");
  return res.json();
}

export async function queryPostgres(text, id) {
  const res = await fetch(`${BASE_URL}/db/query/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: id, code: text }),
  });
  if (!res.ok) throw new Error("API call failed");
  return res.json();
}


export async function createUser(username, password, role = "student") {
  const res = await fetch(`${BASE_URL}/app/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, role }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}


export async function getClassromsById(user_id) {
  const res = await fetch(`${BASE_URL}/app/classrooms/my?user_id=${user_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) throw new Error("API call failed");
  return res.json();
}