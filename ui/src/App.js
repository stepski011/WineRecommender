import React, { createContext, useEffect, useState } from "react";
import AppBar from "@mui/material/AppBar";
import {
  CircularProgress,
  Container,
  CssBaseline,
  Grid,
  MenuItem,
  Typography,
} from "@mui/material";
import { Toolbar } from "@mui/material";
import WineBarIcon from "@mui/icons-material/WineBar";
import { Paper } from "@mui/material";
import { TrainRounded } from "@mui/icons-material";
import { RecommendationPage } from "./views/RecommendationPage";
import SwaggerClient from "swagger-client";
import { Routes, Route } from "react-router-dom";
import { WineDetailPage } from "./views/WineDetailPage";
import { cookie_name, swagger_url } from "./constants";
import { useNavigate } from "react-router-dom";
import { ThemeProvider } from "@emotion/react";
import { theme } from "./theming";
import { useCookies } from "react-cookie";
import RestartAltIcon from "@mui/icons-material/RestartAlt";

export const SwaggerContext = React.createContext(null);

const CustomAppBar = (props) => {
  const navigate = useNavigate();
  const [cookies, setCookie, removeCookie] = useCookies();

  return (
    <AppBar style={{ backgroundColor: "white" }}>
      <Toolbar variant="regular">
        <Grid container justifyContent={"space-between"}>
          <Grid item>
            <MenuItem onClick={() => navigate("/")}>
              <WineBarIcon color="primary" sx={{ fontSize: 40 }} />
              <Typography color="primary" variant="h3" noWrap>
                Wines.MS
              </Typography>
            </MenuItem>
          </Grid>
          <Grid item>
            <MenuItem
              style={{ height: "100%" }}
              onClick={() => {
                removeCookie(cookie_name);
                setTimeout(() => window.location.reload(false), 1000);
              }}
            >
              <RestartAltIcon color="primary" sx={{ fontSize: 40 }} />
            </MenuItem>
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
};

export const App = (props) => {
  const [swaggerClient, setSwaggerClient] = useState(null);

  useEffect(
    () =>
      new SwaggerClient(swagger_url).then((client) => {
        setSwaggerClient(client.apis);
      }),
    []
  );

  return (
    <ThemeProvider theme={theme}>
      <CustomAppBar />
      <CssBaseline />

      <Toolbar />
      <Container maxWidth="lg">
        {swaggerClient ? (
          <SwaggerContext.Provider value={swaggerClient}>
            <Routes>
              <Route path="/" element={<RecommendationPage />} />
              <Route path="/wine/:id" element={<WineDetailPage />} />
            </Routes>
          </SwaggerContext.Provider>
        ) : (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignContent: "center",
            }}
          >
            <CircularProgress />
          </div>
        )}
      </Container>
    </ThemeProvider>
  );
};
