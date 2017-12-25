import React from 'react';
import CodeMirror from 'react-codemirror'

export default class Editor extends React.Component {
   
    constructor(props) {
        super(props);
        this.state = {
            code: 'cubbickb',
        };
    }

    updateCode = (newCode) => {
        this.setState({
            code: newCode,
        })
    }

    render() {
        const options = {
            lineNumbers: true
        }
        return (
            <CodeMirror
                value={this.state.code}
                options={{
                    lineNumbers: true
                }}
                onChange={this.updateCode}
            />
        );
    }
}