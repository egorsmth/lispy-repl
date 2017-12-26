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

    evaluate = (e) => {
        e.preventDefault();
        this.props.evaluate(this.state.code)
    }

    render() {
        const options = {
            lineNumbers: true
        }
        return <div>
            <CodeMirror
                value={this.state.code}
                options={{
                    lineNumbers: true
                }}
                onChange={this.updateCode}
            />
            <button onClick={this.evaluate}>Evaluate</button>
        </div>
    }
}