import { Autocomplete, TextField, Grid, Typography } from "@mui/material";
import React, { useEffect } from "react";

export const SearchMultiSelect = (props) => {
  let selectedValues = props.options.filter((elem) => elem.selected);

  return (
    <Grid
      container
      justifyContent={"space-between"}
      alignItems="center"
      marginTop="1rem"
    >
      <Grid item xs="auto">
        <Typography variant="body">{props.label}</Typography>
      </Grid>
      <Grid item xs={9}>
        <Autocomplete
          title={null}
          multiple
          fullWidth
          options={props.options}
          value={selectedValues}
          onChange={(event, value) => {
            let changedValue = props.options.map((option) => {
              let newOption = option;
              if (value.includes(option)) {
                newOption.selected = true;
              } else {
                newOption.selected = false;
              }
              return newOption;
            });
            props.onChange(changedValue);
          }}
          getOptionLabel={props.getOptionLabel}
          renderInput={(params) => <TextField {...params} />}
        />
      </Grid>
    </Grid>
  );
};
