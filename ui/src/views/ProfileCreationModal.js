import React, { useEffect, useState } from "react";
import { CustomModal } from "../components/CustomModal";
import { WineSelection } from "./profileCreationScreens/WineSelection";
import { TasteCustomization } from "./profileCreationScreens/TasteCustomization";
import { ProfileCustomization } from "./profileCreationScreens/ProfileCustomization";
import { LoadingOverlay } from "../components/LoadingOverlay";
import { useContext } from "react";
import { SwaggerContext } from "../App";

export const ProfileCreationModal = (props) => {
  const swagger = useContext(SwaggerContext);

  const [step, setStep] = useState(0);
  const [title, setTitle] = useState("");
  const [selectedWines, setSelectedWines] = useState([]);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (step == 0) {
      setTitle("Wine Selection");
    } else if (step == 1 || step == 2) {
      setTitle("Wine Profile");
    } else if (step == 2) {
      setTitle("Taste Profile");
    }
  }, [step]);

  const onPrevious = () => {
    if (step == 1) {
      setStep(0);
    } else if (step == 2) {
      setStep(1);
    }
  };
  const onNext = () => {
    if (step == 0) {
      setStep(1);
      setLoading(true);

      let wine_ids = selectedWines.map((wine) => wine.id);
      if (wine_ids.length > 0) {
        swagger.profile
          .profile_read({ wine_ids: JSON.stringify(wine_ids) })
          .then((resp) => {
            setProfile(resp.body);
            setLoading(false);
          });
      }
    } else if (step == 1) {
      setStep(2);
    } else if (step == 2) {
      props.onClose(profile);
    }
  };
  if (loading) {
    return <LoadingOverlay />;
  }

  return (
    <CustomModal
      title={title}
      onNext={onNext}
      onPrevious={onPrevious}
      nextDisabled={selectedWines.length < 1}
      previousDisabled={step <= 0}
    >
      {step == 0 ? (
        <WineSelection
          selectedWines={selectedWines}
          setSelectedWines={setSelectedWines}
        />
      ) : (
        <></>
      )}

      {step == 1 ? (
        <ProfileCustomization
          profile={profile}
          onProfileChange={(changedProfile) => {
            setProfile({ ...changedProfile });
          }}
        />
      ) : (
        <></>
      )}
      {step == 2 ? (
        <TasteCustomization
          profile={profile}
          onProfileChange={(changedProfile) => {
            setProfile({ ...changedProfile });
          }}
        />
      ) : (
        <></>
      )}
    </CustomModal>
  );
};
