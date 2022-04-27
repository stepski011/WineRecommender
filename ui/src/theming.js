import { createTheme, Typography } from "@mui/material";
import { green, orange, purple, red } from "@mui/material/colors";
import { ThemeProvider } from "styled-components";

export const theme = createTheme({
  palette: {
    background: {
      default: "#f7f7fa",
    },
    primary: {
      main: "#81171b",
      dark: "#540804",
      light: "#ad2e24",
    },
    secondary: {
      main: "#ffdc9b",
    },
  },
  components: {
    MuiImageListItemBar: {
      styleOverrides: {
        root: { backgroundColor: "#ffffffe6" },
        titleWrap: { color: "#81171b" },
      },
    },
  },
});
