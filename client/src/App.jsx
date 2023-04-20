import React, { useState, useEffect } from "react";
import { socket } from "./socket";
import { ConnectionState } from "./components/ConnectionState";
import { ConnectionManager } from "./components/ConnectionManager";
import { MyForm } from "./components/MyForm";
import { Events } from "./components/Events";
import { fetchFunc } from "./fetch";
function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  // const [fooEvents, setFooEvents] = useState(0);
  const [RecievedData, setRecievedData] = useState();

  useEffect(() => {
    function onConnect() {
      setIsConnected(true);
    }

    function onDisconnect() {
      setIsConnected(false);
    }

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);
    socket.on("dataSent", (data) => {
      setRecievedData(data);
      console.log("data recieved", data);
    });

    return () => {
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
      socket.off("data", (data) => {
        setRecievedData(data);
        console.log("data recieved", data);
      });
    };
  }, []);

  useEffect(() => {}, [RecievedData]);

  return (
    <div className="App">
      <ConnectionState isConnected={isConnected} />

      <ConnectionManager />
      <MyForm />

      <p>
        {" "}
        Recieved Data = {RecievedData ? (
          <Events RecievedData={RecievedData} />
        ) : (
          "no"
        )}{" "}
      </p>
    </div>
  );
}

export default App;
