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
import { Divider, Stack, Button, Card, CardHeader } from '@mui/material';



const Settings = () => {
    const [settings, setSettings] = useState(0)
    const [error, setError] = useState(0)
    useEffect(() => {
        fetch("https://192.168.20.62:9000/settings").then(response => {
            response.json().then(data => {
                setSettings(data);
            }).catch(error => {
                setError(error)
            })
        })
    }, [])

    const saveSettings = () => {
        fetch("https://192.168.20.62:9000/settings", {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        }).then(response => {
            response.json().then(data => {
                setSettings(data)
            })
        })
    }

    return (
        <Card>
            <CardHeader title="Silvia Settings" subheader="Modidy settings here"></CardHeader>
            <Stack spacing={2}>
                <TableContainer component={Paper}>
                <Divider />
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
                                <TableCell><TextField id="BrewTemp" defaultValue={settings.brew_target_temp} variant="standard" onChange={(event) => {setSettings({ ...settings, steam_target_temp: parseFloat(event.target.value)})}} /></TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Steam Target Temp</TableCell>
                                <TableCell><TextField id="SteamTemp" defaultValue={settings.steam_target_temp} variant="standard" onChange={(event) => {setSettings({ ...settings, steam_target_temp: parseFloat(event.target.value)})}} /></TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>P</TableCell>
                                <TableCell><TextField id="P" defaultValue={settings.p} variant="standard" onChange={(event) => {setSettings({ ...settings, steam_target_temp: parseFloat(event.target.value)})}} /></TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>I</TableCell>
                                <TableCell><TextField id="I" defaultValue={settings.i} variant="standard" onChange={(event) => {setSettings({ ...settings, steam_target_temp: parseFloat(event.target.value)})}} /></TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>D</TableCell>
                                <TableCell><TextField id="D" defaultValue={settings.d} variant="standard" onChange={(event) => {setSettings({ ...settings, steam_target_temp: parseFloat(event.target.value)})}} /></TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Cycle Seconds</TableCell>
                                <TableCell><TextField id="CycleSeconds" defaultValue={settings.cycle_seconds} variant="standard" onChange={(event) => {setSettings({ ...settings, steam_target_temp: parseFloat(event.target.value)})}} /></TableCell>
                            </TableRow>
                        </TableBody>
                            :
                            error ? 
                            <TableBody>
                                <TableRow>
                                    <TableCell>Error</TableCell>
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
                <Button variant="contained" onClick={saveSettings}>Save</Button>
            </Stack>
        </Card>
    )
}


export default Settings;