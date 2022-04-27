import React, { useState } from "react";
import { Tooltip } from "@mui/material";
import { Popover } from "@mui/material";
import { Paper } from "@mui/material";
import { propTypes } from "google-map-react";
import { theme } from "../theming";
export const createMarker = (nr, lat, lng, info, url) => {
  return (
    <div
      key={nr}
      lat={lat}
      lng={lng}
      style={{
        position: "absolute",
        width: 30,
        height: 30,

        border: "5px solid" + theme.palette.primary.main,
        borderRadius: 20,
        textAlign: "center",
        backgroundColor: "white",
        fontSize: 16,
        fontWeight: "bold",
        padding: 4,
        cursor: "pointer",
      }}
      onClick={() => open(url)}
    >
      <Tooltip placement="right" title={info}>
        <div style={{ marginTop: "-3px" }}>{nr}</div>
      </Tooltip>
    </div>
  );
};
