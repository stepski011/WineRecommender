import React, { useEffect, useState } from "react";
import { WineBar } from "@mui/icons-material";

export const CustomImg = (props) => {
  useEffect(() => (props.src ? null : setBackupVisible(true)), []);
  let [backupVisible, setBackupVisible] = useState(false);
  return (
    <>
      {!backupVisible ? (
        <img
          style={{
            width: "10rem",
            height: "10rem",
            alignSelf: "center",
            objectFit: "contain",
          }}
          onError={() => {
            setBackupVisible(true);
          }}
          src={props.src}
        />
      ) : (
        <WineBar
          height={200}
          width={100}
          style={{
            flex: 1,
            width: 100,
            height: 100,
            alignSelf: "center",
            resizeMode: "contain",
          }}
        />
      )}
    </>
  );
};
