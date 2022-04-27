import { Typography, Grid, ToggleButton } from "@mui/material";
import React, { Fragment } from "react";

export const MultiSelect = (props) => {
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
      <Grid container item xs={9} spacing={1} justifyContent={"flex-end"}>
        {props.options.map((option, index) => (
          <Fragment key={index}>
            <Grid item>
              <ToggleButton
                value={option}
                selected={option.selected}
                style={{
                  width: "100px",
                  height: "50px",
                  whiteSpace: "nowrap",
                  textTransform: "capitalize",
                }}
                onChange={(event, value) => {
                  console.log(value);
                  let changedValue = props.options.map((option) => {
                    let newOption = option;
                    if (value.option == newOption.option) {
                      newOption.selected = !newOption.selected;
                    }
                    return newOption;
                  });
                  props.onChange(changedValue);
                }}
              >
                {option.option}
              </ToggleButton>
            </Grid>
          </Fragment>
        ))}
      </Grid>
    </Grid>
  );
};
