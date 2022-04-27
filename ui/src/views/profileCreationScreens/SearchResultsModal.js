import { CircularProgress } from "@mui/material";
import { Add } from "@mui/icons-material";
import React, { useContext, useEffect, useState } from "react";
import { SwaggerContext } from "../../App";
import { CustomModal } from "../../components/CustomModal";
import { CustomImageList } from "../../components/CustomImageList";
export const SearchResultModal = (props) => {
  const swagger = useContext(SwaggerContext);
  const [results, setResults] = useState(null);
  useEffect(
    () =>
      swagger.search_wines
        .search_wines_read({ criteria: props.searchString })
        .then((result) => {
          console.log(result.body.wines);
          setResults(result.body.wines);
        }),
    []
  );
  return (
    <CustomModal
      buttonDisabled={true}
      title={"Results for: " + props.searchString}
      onClose={() => {
        console.log("close");
        props.onClose();
      }}
    >
      {!results ? (
        <CircularProgress />
      ) : (
        <CustomImageList
          button={<Add />}
          data={results}
          id={"id"}
          pictureUrl={"picture_url"}
          label={"name"}
          cols={3}
          onClick={(elem) => props.onClose(elem)}
        />
      )}
    </CustomModal>
  );
};
