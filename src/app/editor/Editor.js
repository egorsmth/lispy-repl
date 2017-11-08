import React from 'react';
import {UnControlled as CodeMirror} from 'react-codemirror2'

class Editor extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            code: 'ccode'
        }
    }

    getInitialState() {
		return {
			code: "// Code",
		};
	}

    updateCode(newCode) {
		this.state ={
			code: newCode,
        };
    }

    render() {
        const options = {
            lineNumbers: true
        }
        return (
            <CodeMirror
                value='<h1>I ♥ react-codemirror2</h1>'
                options={{
                    mode: 'xml',
                    theme: 'material',
                    lineNumbers: true
                }}
                onChange={(editor, data, value) => {}}
            />
        );
    }
}

export default Editor