import React, { useState } from "react";
import {
  ImageList,
  Card,
  CardActionArea,
  ImageListItem,
  ImageListItemBar,
  CardMedia,
  Popover,
  Button,
  IconButton,
} from "@mui/material";
import { Add, WineBar } from "@mui/icons-material";
import { theme } from "../theming";
import { CustomImg } from "./CustomImg";
export const CustomImageList = (props) => {
  return (
    <ImageList cols={props.cols}>
      {props.data.map((dataPoint) => (
        <Card
          style={{ margin: "0.5rem" }}
          key={dataPoint[props.id]}
          elevation={3}
        >
          <CardActionArea onClick={() => props.onClick(dataPoint)}>
            <ImageListItem key={dataPoint[props.id]} style={{ opacity: 2 }}>
              <CustomImg src={dataPoint[props.pictureUrl]} />
              <ImageListItemBar
                subtitle={dataPoint[props.label]}
                actionIcon={
                  props.button ? (
                    <IconButton
                      size="small"
                      variant="contained"
                      style={{
                        color: "white",
                        backgroundColor: "#540804cc",
                        margin: "0.25rem",
                      }}
                    >
                      {props.button}
                    </IconButton>
                  ) : (
                    <></>
                  )
                }
              />
            </ImageListItem>
          </CardActionArea>
        </Card>
      ))}
    </ImageList>
  );
};
