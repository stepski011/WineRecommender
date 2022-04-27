import React, { useState } from "react";

import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  LinearScale,
} from "chart.js";
import "chartjs-plugin-dragdata";
import { theme } from "../../theming";
import Color from "color";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,

  Filler,
  Tooltip,
  Legend
);

export const TasteCustomization = (props) => {
  console.log(props.profile);
  let labels = props.profile.taste_data.map((elem) => elem.label);
  let datapoints = props.profile.taste_data.map((elem) => elem.percentage);

  const data = {
    labels: labels,
    datasets: [
      {
        label: "Your Taste",
        data: datapoints,
        backgroundColor: Color(theme.palette.primary.main).alpha(0.2).string(),
        borderColor: theme.palette.primary.main,
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      dragData: {
        round: 1,
        showTooltip: true,
        onDragEnd: function (e, datasetIndex, index, value) {
          let newProfile = { ...props.profile };
          newProfile.taste_data[index].percentage = value;
          props.onProfileChange(newProfile);
        },
      },
    },
    scales: {
      r: {
        angleLines: {
          display: false,
        },
        suggestedMin: 0,
        suggestedMax: 1,
      },
    },
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        alignContent: "center",
        marginInline: "auto",
      }}
    >
      <Radar data={data} options={options} />
    </div>
  );
};
