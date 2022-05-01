import React, { useRef, useState, useEffect } from "react";
import { Button, FormLabel } from '@mui/material';
import Box from '@mui/material/Box';
import TextareaAutosize from '@mui/material/TextareaAutosize';


const serverAddr = process.env.SERVER_ADDR || "localhost";
const serverPort = process.env.SERVER_PORT || 8000;



const defaultValues = {
    payLoad: "",
}

export const MainView = () => {

    const [formValues, setFormValues] = useState(defaultValues)

    const [results, setResults] = useState("")
    const [resultAST, setResultAST] = useState("")

    const handleInputChange = (e) => {
        console.log(e.target)
        const { id, value } = e.target;
        setFormValues({
            ...formValues,
            [id]: value,
        });
    }

    const run = () => {
        console.log(formValues.payLoad)
        const url = `http://${serverAddr}:${serverPort}/run`;
        fetch(url, {
            method: "POST",
            body: formValues.payLoad,
        })
            .then(res => res.json())
            .then(json => {
                console.log(json)
                setResults(json.results)
                setResultAST(json.ast)
            })

    }

    const clear = () => {
        setFormValues({
            ...formValues,
            payLoad: "",
        });
    }

    return (
        <div>
            <Box
                component="form"
                sx={{
                    '& > :not(style)': { m: 1, width: '25ch' },
                }}
                noValidate
                autoComplete="off"
            >

                <TextareaAutosize id="payLoad"
                    aria-label="empty textarea"
                    placeholder="Empty"
                    style={{ width: 200 }}

                    value={formValues.payLoad}
                    onChange={e => handleInputChange(e)}

                />


                <Button onClick={run}>Run</Button>
                <Button onClick={clear}>Clear</Button>

            </Box>

            <pre>
                <br />
                RESULTS: <br />
                <br />
                <div>
                    {results}
                </div>

                <div>
                    <br />
                    <br />
                    AST: <br />
                    <br />
                </div>
                <div>
                    {resultAST}
                </div>

                <div>

                </div>
            </pre>

        </div >
    );
}