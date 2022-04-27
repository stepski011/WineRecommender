import React, { useState } from "react";
import {
  Button,
  Dialog,
  DialogContent,
  Divider,
  inputAdornmentClasses,
  Typography,
} from "@mui/material";
import { TextField } from "@mui/material";
import { SearchResultModal } from "./SearchResultsModal";
import { CustomImageList } from "../../components/CustomImageList";
import { Delete } from "@mui/icons-material";

export const WineSelection = (props) => {
  const [searchString, setSearchString] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  return (
    <>
      <TextField
        focused
        style={{ marginTop: "1rem" }}
        label="Search field"
        type="search"
        label="Wine Search"
        placeholder="Search for a wine you like"
        fullWidth
        onKeyDown={(event) =>
          event.keyCode == 13 && searchString.length > 3
            ? setDialogOpen(true)
            : null
        }
        onChange={(event) => setSearchString(event.target.value)}
      />
      {dialogOpen ? (
        <SearchResultModal
          searchString={searchString}
          onClose={(elem) => {
            setDialogOpen(false);
            if (elem && !props.selectedWines.includes(elem)) {
              let newSelectedWines = [...props.selectedWines];
              newSelectedWines.push(elem);

              props.setSelectedWines(newSelectedWines);
            }
          }}
        />
      ) : (
        <></>
      )}
      <Divider style={{ marginBlock: "1rem" }} />

      {props.selectedWines.length > 0 ? (
        <CustomImageList
          button={<Delete />}
          cols={3}
          data={props.selectedWines}
          id={"id"}
          pictureUrl={"picture_url"}
          label={"name"}
          onClick={(elem) => {
            let newSelectedWines = [
              ...props.selectedWines.filter((value) => value != elem),
            ];
            props.setSelectedWines(newSelectedWines);
          }}
        />
      ) : (
        <Typography variant="body1">
          You have not selected any wines. <br />
          Please select at least one wine to continue!
        </Typography>
      )}
    </>
  );
};
