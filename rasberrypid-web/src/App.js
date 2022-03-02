import logo from './logo.svg';
import './App.css';
import Settings from './components/Settings'
import { ThemeProvider, createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <Settings />
    </ThemeProvider>
  );
}

export default App;
