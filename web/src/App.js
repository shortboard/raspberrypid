import './App.css';
import Settings from './components/Settings'
import TempGraph from './components/TempGraph'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import React from 'react';
import { Container, CssBaseline, Stack } from '@mui/material';

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
      <Container>

        <Stack spacing={2}>
          <Settings />
          <TempGraph />
        </Stack>
        </Container>
        
      </ThemeProvider>
    </React.Fragment>
  );
}

export default App;
