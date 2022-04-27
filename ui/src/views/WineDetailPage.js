import {
  CardContent,
  Card,
  Typography,
  Link,
  CardActionArea,
  CardActions,
  Button,
  ImageList,
} from "@mui/material";
import React, { useEffect, useState, useContext } from "react";
import {
  useLocation,
  useNavigate,
  useParams,
  useRoutes,
} from "react-router-dom";
import { LoadingOverlay } from "../components/LoadingOverlay";
import { ImageListItem, ImageListItemBar } from "@mui/material";
import { Grid } from "@mui/material";
import { CardHeader } from "@mui/material";

import { SwaggerContext, CustomAppBar } from "../App";
import { ShoppingBasket } from "@mui/icons-material";
import { WineBar } from "@mui/icons-material";
import { TasteDataWidget } from "../components/TasteDataWidget";
import { maxWidth, width } from "@mui/system";

export const WineDetailPage = (props) => {
  const params = useParams();

  const swagger = useContext(SwaggerContext);
  const [data, setData] = useState(null);
  const [backupVisible, setBackupVisible] = useState(false);

  useEffect(() => {
    swagger.details.details_read({ id: params.id }).then((resp) => {
      setData(resp.body);
    });
  }, []);

  if (!data) {
    return <LoadingOverlay />;
  }

  console.log(data);
  return (
    <>
      <Card elevation={5} style={{ marginTop: "1rem" }}>
        <CardContent>
          <Grid container spacing={1}>
            <Grid item xs={12} sm={3}>
              <ImageList sx={{ width: "100%", height: "500px" }} cols={1}>
                <ImageListItem style={{ overflow: "hidden" }}>
                  <img
                    style={{
                      flex: 1,
                      height: "100%",
                      maxWidth: "100%",
                      alignSelf: "center",
                      objectFit: "contain",
                    }}
                    src={
                      !backupVisible
                        ? data.picture_url + "?w=161&fit=clamp&auto=format"
                        : "http://localhost:8080/backup_bottle.jpeg"
                    }
                    onError={() => setBackupVisible(true)}
                  />

                  <ImageListItemBar subtitle={data.name} />
                </ImageListItem>
              </ImageList>
            </Grid>
            <Grid item sm={9}>
              <Card>
                <CardHeader title="Description" />
                <CardContent>
                  {data.description
                    ? data.description
                    : "no description available"}
                </CardContent>
              </Card>
              <Grid item container spacing={1} style={{ marginTop: "0.25rem" }}>
                <Grid item md={6} xs={12}>
                  <Card>
                    <CardHeader title="Facts" />
                    <CardContent>
                      <Grid container>
                        {data.facts.map((elem) => (
                          <>
                            {elem.content ? (
                              <Grid
                                container
                                item
                                justifyContent={"space-between"}
                                style={{ textTransform: "capitalize" }}
                              >
                                <Grid item>
                                  <Typography variant="body1">
                                    {elem.label}
                                  </Typography>
                                </Grid>
                                <Grid item>
                                  <Typography variant="body1">
                                    {elem.content}
                                  </Typography>
                                </Grid>
                              </Grid>
                            ) : (
                              <></>
                            )}
                          </>
                        ))}
                      </Grid>
                      <Button
                        style={{ marginTop: "1rem" }}
                        variant="contained"
                        endIcon={<ShoppingBasket />}
                        href={data.link}
                      >
                        Buy here
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item md={6} xs={12}>
                  <TasteDataWidget data={data} />
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </>
  );
};
