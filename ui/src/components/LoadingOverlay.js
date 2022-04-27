import React from "react";
import { Modal, CircularProgress } from "@mui/material";

//Change to Backdrop
export const LoadingOverlay = () => (
  <Modal
    open={true}
    style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}
  >
    <CircularProgress />
  </Modal>
);
