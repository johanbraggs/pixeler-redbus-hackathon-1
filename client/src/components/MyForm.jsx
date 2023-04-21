import React, { useState } from "react";
import { socket } from "../socket";

export function MyForm() {
  const [value, setValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  function onSubmit(event) {
    event.preventDefault();
    setIsLoading(true);
    try {
      const data = parseInt(value);
      socket.timeout(5000).emit("data", data, () => {
        setIsLoading(false);
      });
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <input onChange={(e) => setValue(e.target.value)} />

      <button type="submit" disabled={isLoading}>
        Submit
      </button>
    </form>
  );
}
