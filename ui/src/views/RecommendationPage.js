import React, { useEffect, useState } from "react";
import { Typography } from "@mui/material";
import { CustomModal } from "../components/CustomModal";
import { ProfileCreationModal } from "./ProfileCreationModal";
import { Recommendations } from "./Recommendations";
import { LoadingOverlay } from "../components/LoadingOverlay";
import { useContext } from "react";
import { SwaggerContext } from "../App";
import { useLocation } from "react-router-dom";
import { useCookies } from "react-cookie";
import { cookie_name } from "../constants";
export const RecommendationPage = (props) => {
  const [profile, setProfile] = useState(false);
  const [recoData, setRecoData] = useState(null);
  const [loading, setLoading] = useState(false);

  const [cookies, setCookie, removeCookie] = useCookies(cookie_name);

  const swagger = useContext(SwaggerContext);
  useEffect(() => {
    cookies[cookie_name] ? setProfile(cookies[cookie_name]) : null;
  }, []);
  useEffect(() => {
    if (profile) {
      setLoading(true);
      let profile_string = JSON.stringify(profile);
      swagger.recommendations
        .recommendations_read({ profile: profile_string })
        .then((resp) => {
          setRecoData(resp.body);

          setLoading(false);
        });
    }
  }, [profile]);

  return (
    <>
      {!profile ? (
        <ProfileCreationModal
          onClose={(profile) => {
            setCookie("wineMsProfile", profile);
            setProfile(profile);
          }}
        />
      ) : (
        <></>
      )}
      {recoData ? (
        <Recommendations recoData={recoData} profile={profile} />
      ) : (
        <></>
      )}
      {loading ? <LoadingOverlay /> : <></>}
    </>
  );
};
