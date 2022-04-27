import React, { Fragment } from "react";
import { MultiSelect } from "../../components/selectors/MultiSelect.js";
import { SearchMultiSelect } from "../../components/selectors/SearchMultiSelect.js";

export const ProfileCustomization = (props) => {
  console.log(props.profile.wine_data);
  return (
    <>
      {props.profile.wine_data.map((elem, index) => {
        let onChange = (change) => {
          let index = props.profile.wine_data.indexOf(elem);
          let newProfile = props.profile;
          let newElem = elem;
          newElem.options = change;
          newProfile.wine_data[index] = newElem;
          props.onProfileChange(newProfile);
        };

        if (elem.selection_type == "multiselect") {
          return (
            <Fragment key={index}>
              <MultiSelect
                label={elem.name}
                options={elem.options}
                onChange={onChange}
              />
            </Fragment>
          );
        } else if (elem.selection_type == "search_field") {
          return (
            <Fragment key={index}>
              <SearchMultiSelect
                options={elem.options}
                getOptionLabel={(elem) => elem.option}
                label={elem.name}
                onChange={onChange}
              />
            </Fragment>
          );
        }
      })}
    </>
  );
};
