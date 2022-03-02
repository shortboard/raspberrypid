import React, { useEffect, useState } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField'
import Container from '@mui/material/Container'



const Settings = () => {
    const [settings, setSettings] = useState(0)
    useEffect(() => {
        fetch("https://1f3ec752c651391946e67ce0165e8dc0.balena-devices.com/settings").then(response => {
            response.json().then(data => {
                setSettings(data);
            })
        })
    })
    return (
        <Container>
            <h1>Settings</h1>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 400 }} aria-label="settings-table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Setting</TableCell>
                            <TableCell>Value</TableCell>
                        </TableRow>
                    </TableHead>
                    { settings ? 
                        <TableBody>
                        <TableRow>
                            <TableCell>Brew Target Temp</TableCell>
                            <TableCell><TextField id="BrewTemp" defaultValue={settings.brew_target_temp} variant="standard" /></TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Steam Target Temp</TableCell>
                            <TableCell><TextField id="SteamTemp" defaultValue={settings.steam_target_temp} variant="standard" /></TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>P</TableCell>
                            <TableCell><TextField id="P" defaultValue={settings.p} variant="standard" /></TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>I</TableCell>
                            <TableCell><TextField id="I" defaultValue={settings.i} variant="standard" /></TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>D</TableCell>
                            <TableCell><TextField id="D" defaultValue={settings.d} variant="standard" /></TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Cycle Seconds</TableCell>
                            <TableCell><TextField id="CycleSeconds" defaultValue={settings.cycle_seconds} variant="standard" /></TableCell>
                        </TableRow>
                    </TableBody>
                        :
                        <TableBody>
                            <TableRow>
                                <TableCell>Loading...</TableCell>
                            </TableRow>
                        </TableBody>
                    }
                    
                </Table>
            </TableContainer>
        </Container>
        
    )
}


export default Settings;