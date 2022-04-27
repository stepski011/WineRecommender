import React from "react";

export const CustomMapMarker = (props) => {
  return (
    <div
      lat="51.96"
      lng="7.65"
      style={{
        position: "absolute",
        width: props.K_WIDTH,
        height: props.K_HEIGHT,
        left: -props.K_WIDTH / 2,
        top: -props.K_HEIGHT / 2,

        border: "5px solid #f44336",
        borderRadius: props.K_HEIGHT,
        backgroundColor: "white",
        textAlign: "center",
        color: "#3f51b5",
        fontSize: 16,
      
        fontWeight: "bold",
        padding: 4,
      }}
    >
      {props.children}
    </div>
  );
};
