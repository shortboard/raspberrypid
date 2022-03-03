import logo from './logo.svg';
import './App.css';
import Settings from './components/Settings'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import React from 'react';
import { CssBaseline } from '@mui/material';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
    <React.Fragment>
      
      <ThemeProvider theme={darkTheme}>
      <CssBaseline />
        <Settings />
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
