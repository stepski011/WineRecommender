import React from "react";
import { Typography, Card, CardContent, CardHeader } from "@mui/material";
import GoogleMapReact from "google-map-react";
import { CustomImageList } from "../components/CustomImageList";
import { createMarker } from "../components/CustomMarker";
import { useLocation, useNavigate } from "react-router-dom";
import { gmaps_api_key } from "../constants";
import { theme } from "../theming";

export const Recommendations = (props) => {
  const navigate = useNavigate();
  console.log(props);
  const defaultProps = {
    center: {
      lat: 51.96,
      lng: 7.65,
    },
    zoom: 10,
  };
  return (
    <>
      <Card
        elevation={5}
        style={{
          marginTop: "1rem",
        }}
      >
        <CardContent>
          <CardHeader title="Wines you might like" />
          <CustomImageList
            data={props.recoData.wines}
            id={"id"}
            pictureUrl={"picture_url"}
            label={"label"}
            cols={4}
            onClick={(elem) => open("/wine/" + elem.id, "_blank")}
          />
        </CardContent>
      </Card>
      <Card
        elevation={5}
        style={{
          marginTop: "1rem",
        }}
      >
        <CardContent>
          <CardHeader title="Winesellers you might like" />
          <div style={{ height: "30vh", width: "100%" }}>
            <GoogleMapReact
              bootstrapURLKeys={{
                key: gmaps_api_key,
              }}
              defaultCenter={defaultProps.center}
              defaultZoom={defaultProps.zoom}
            >
              {props.recoData.sellers.map((elem) => {
                return createMarker(
                  elem.rank,
                  elem.lat,
                  elem.lon,
                  elem.name,
                  elem.url
                );
              })}
            </GoogleMapReact>
          </div>
        </CardContent>
      </Card>
    </>
  );
};
